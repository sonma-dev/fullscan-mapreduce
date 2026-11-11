import asyncio
import unittest
from collections import Counter
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from plugins.talks_with_responses import talks_with_responses as responses_plugin
from server import chat
from server.concurrency import level_concurrency_limits
from server.models import AppServices
from test_file_chunks import make_deck
from test_map_requests import ControlledResponses


def settings(level1="", level2="", legacy=""):
    return {
        "LLM_MAX_PARALLEL_LEVEL1_REQUESTS": str(level1),
        "LLM_MAX_PARALLEL_LEVEL2_REQUESTS": str(level2),
        "LLM_MAX_PARALLEL_CHUNK_REQUESTS": str(legacy),
    }


class LevelConcurrencySettingsTests(unittest.TestCase):
    def test_defaults_legacy_fallback_and_independent_overrides(self):
        cases = [
            (settings(), (16, 16)),
            (settings(16, 16, legacy=8), (16, 16)),
            (settings(legacy=2), (2, 2)),
            (settings(3, legacy=2), (3, 2)),
            (settings(level2=5, legacy=2), (2, 5)),
            (settings(3, 5, legacy=1), (3, 5)),
            (settings(" ", 5, legacy=2), (2, 5)),
        ]
        for environment, expected in cases:
            with self.subTest(environment=environment), patch.dict("os.environ", environment):
                self.assertEqual(level_concurrency_limits(), expected)

    def test_each_limit_is_clamped_independently(self):
        for environment, expected in [(settings(0, 20), (1, 16)), (settings(20, -1), (16, 1)),
                                      (settings(legacy=20), (16, 16))]:
            with self.subTest(environment=environment), patch.dict("os.environ", environment):
                self.assertEqual(level_concurrency_limits(), expected)

    def test_invalid_level_setting_falls_back_without_changing_the_other_level(self):
        for environment, expected in [(settings("invalid", 5, legacy=2), (2, 5)),
                                      (settings(3, "invalid", legacy=2), (3, 2)),
                                      (settings(legacy="invalid"), (16, 16))]:
            with self.subTest(environment=environment), patch.dict("os.environ", environment):
                with self.assertLogs("server.utils", level="WARNING"):
                    self.assertEqual(level_concurrency_limits(), expected)


class LevelConcurrencyTests(unittest.IsolatedAsyncioTestCase):
    async def test_hierarchy_limits_are_independent_and_shared_across_chapters_and_batches(self):
        for level1, level2, count in [(3, 1, 4), (1, 3, 4), (16, 16, 32)]:
            with self.subTest(level1=level1, level2=level2):
                active, peaks = Counter(), Counter()
                expected = {"onelevel_context": min(level1, count // 2), "onelevel_reduce": level1, "map": level2}
                ready = {phase: asyncio.Event() for phase in expected}

                async def before(phase, step, payload):
                    active[phase] += 1
                    peaks[phase] = max(peaks[phase], active[phase])
                    if phase in expected and step == 1:
                        if active[phase] == expected[phase]:
                            ready[phase].set()
                        # Require actual overlap when configured, rather than
                        # passing merely because the measured peak was small.
                        await ready[phase].wait()
                    await asyncio.sleep(0.01)

                def after(phase, step, payload):
                    active[phase] -= 1

                def expand(phase, payload, value):
                    if phase == "map":
                        value["findings"][0]["sources"][0]["quote"] += " Original evidence detail." * 200
                    return value

                fake = ControlledResponses(self, before, after, mutate=expand)
                environment = {**settings(level1, level2, legacy=1),
                               "FILE_CHUNK_MAX_SLIDES": "1", "LLM_CHAPTER_BATCH_MAX_BYTES": "6500"}
                with patch.dict("os.environ", environment), self.assertLogs("server", level="INFO") as logs:
                    result = await asyncio.wait_for(chat.generate_specifications(
                        AppServices(responses=fake), make_deck(count), "sample.pptx"), 60)
                self.assertEqual({phase: peaks[phase] for phase in expected}, expected)
                self.assertTrue(all(count == 0 for count in active.values()))
                self.assertTrue(all(peaks[phase] == 1 for phase in
                                    ("global_context", "root_context", "root_reduce", "root_approval")))
                self.assertTrue(any(f"level1_max_parallel={level1} level2_max_parallel={level2}" in line
                                    for line in logs.output))
                self.assertEqual(len(result["specifications"]), 8)
                self.assertEqual(result["usage"]["total_tokens"], len(fake.calls) * 12)
                for stage in result["hierarchy"]["stages"]:
                    nodes = stage["attempts"][0]["nodes"]
                    self.assertEqual(len(nodes), count // 2)
                    for node in nodes:
                        calls = node["aggregation_calls"]
                        self.assertEqual([call["mode"] for call in calls], ["batch", "batch", "final"])
                        self.assertEqual([call["batch"] for call in calls[:2]], [1, 2])

    async def test_responses_client_does_not_throttle_explicit_limits_to_the_legacy_value(self):
        for level1, level2 in [(3, 1), (1, 3), (16, 1), (1, 16), (16, 16)]:
            with self.subTest(level1=level1, level2=level2):
                active = peak = 0
                ready, release = asyncio.Event(), asyncio.Event()
                capacity = max(level1, level2)
                client = SimpleNamespace(close=AsyncMock())

                async def respond(*args):
                    nonlocal active, peak
                    active += 1
                    peak = max(peak, active)
                    if active == capacity:
                        ready.set()
                    try:
                        await release.wait()
                        return "response"
                    finally:
                        active -= 1

                with patch.dict("os.environ", settings(level1, level2, legacy=1)), patch.object(
                    responses_plugin, "AsyncAzureOpenAI", return_value=client,
                ):
                    plugin = responses_plugin.TalksWithResponses(
                        "https://example.openai.azure.com", lambda: "test-key", "test-model", "api_key")
                with patch.object(plugin, "_create_response", side_effect=respond):
                    tasks = [asyncio.create_task(plugin.create_response("query", "instructions"))
                             for _ in range(capacity + 2)]
                    try:
                        await asyncio.wait_for(ready.wait(), 5)
                        await asyncio.sleep(0)
                        self.assertEqual(peak, capacity)
                        release.set()
                        self.assertEqual(await asyncio.wait_for(asyncio.gather(*tasks), 5),
                                         ["response"] * len(tasks))
                    finally:
                        for task in tasks:
                            task.cancel()
                        await asyncio.gather(*tasks, return_exceptions=True)
                        await plugin.close()
                self.assertEqual(active, 0)
                self.assertEqual(peak, capacity)


if __name__ == "__main__":
    unittest.main()
