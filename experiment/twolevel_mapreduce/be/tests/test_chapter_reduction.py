import asyncio
import copy
import unittest

from server.chapter_reduction import finding_ids, reduce_chapter
from server.evidence import EvidenceError, adjudication_record, encode


def scan(index, count=1):
    return {"chunk_id": index, "covered_units": [index], "gaps": [f"Gap from chunk {index}"],
            "findings": [{"id": f"c{index}:f{number}", "statement": "Restriction", "sources": ["source " * 100]} for number in range(count)]}


class ChapterReductionTests(unittest.IsolatedAsyncioTestCase):
    async def test_batches_overlap_and_final_input_and_history_keep_source_order(self):
        children = [scan(index) for index in range(1, 7)]
        started = set()
        completed = []
        ready = asyncio.Event()
        release = {index: asyncio.Event() for index in range(1, 7)}
        finished = {index: asyncio.Event() for index in range(1, 7)}

        async def invoke(payload, identifiers, compact):
            aggregation = payload["aggregation"]
            if aggregation["mode"] == "batch":
                self.assertEqual(aggregation["round"], 0)
                index = aggregation["batch"]
                started.add(index)
                if len(started) == 6:
                    ready.set()
                await release[index].wait()
                completed.append(index)
                finished[index].set()
            else:
                self.assertEqual(completed, [6, 5, 4, 3, 2, 1])
                self.assertEqual([sorted(finding_ids([child])) for child in payload["children"]],
                                 [[f"c{index}:f0"] for index in range(1, 7)])
            return {"decisions": [{"finding_ids": sorted(identifiers)}]}

        task = asyncio.create_task(reduce_chapter(children, payload_base={}, fits=lambda p: True,
                                                  invoke=invoke, batch_bytes=1000, max_rounds=8))
        try:
            await asyncio.wait_for(ready.wait(), 5)
            for index in range(6, 0, -1):
                release[index].set()
                await asyncio.wait_for(finished[index].wait(), 5)
            outcome, history = await asyncio.wait_for(task, 5)
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        self.assertEqual([item["batch"] for item in history[:-1]], list(range(1, 7)))
        self.assertEqual(history[-1]["mode"], "final")
        self.assertEqual(finding_ids([{"outcome": outcome}]), finding_ids(children))

    async def test_every_round_is_concurrent_and_waits_for_the_previous_round(self):
        active, peaks, completed = {}, {}, {}

        async def invoke(payload, identifiers, compact):
            aggregation = payload["aggregation"]
            round_number = aggregation["round"]
            self.assertFalse(any(count for previous, count in active.items() if previous != round_number))
            if round_number:
                self.assertEqual(completed[round_number - 1], 6)
            if aggregation["mode"] == "batch":
                active[round_number] = active.get(round_number, 0) + 1
                peaks[round_number] = max(peaks.get(round_number, 0), active[round_number])
                await asyncio.sleep(0)
                active[round_number] -= 1
                completed[round_number] = completed.get(round_number, 0) + 1
            return {"summary": "x" * (600 if round_number == 0 else 1),
                    "decisions": [{"finding_ids": sorted(identifiers)}]}

        _, history = await reduce_chapter([scan(index) for index in range(1, 7)], payload_base={},
                                          fits=lambda p: True, invoke=invoke, batch_bytes=1000, max_rounds=8)
        self.assertEqual(peaks, {0: 6, 1: 6})
        self.assertEqual(history[-1]["mode"], "final")
        self.assertEqual(history[-1]["round"], 2)

    async def test_failed_batch_cancels_and_awaits_siblings_before_propagating(self):
        started, stopped = set(), set()
        ready = asyncio.Event()

        async def invoke(payload, identifiers, compact):
            self.assertEqual(payload["aggregation"]["mode"], "batch")
            index = payload["aggregation"]["batch"]
            started.add(index)
            if len(started) == 3:
                ready.set()
            try:
                await ready.wait()
                if index == 1:
                    raise EvidenceError("Batch validation failed")
                await asyncio.Event().wait()
            finally:
                stopped.add(index)

        with self.assertRaises(ExceptionGroup) as raised:
            await asyncio.wait_for(reduce_chapter([scan(index) for index in range(1, 4)],
                payload_base={}, fits=lambda p: True, invoke=invoke, batch_bytes=1000, max_rounds=8), 5)
        self.assertEqual(started, {1, 2, 3})
        self.assertEqual(stopped, started)
        self.assertEqual(str(raised.exception.exceptions[0]), "Batch validation failed")

    async def test_caller_cancellation_stops_all_active_batches(self):
        started, stopped = set(), set()
        ready = asyncio.Event()

        async def invoke(payload, identifiers, compact):
            index = payload["aggregation"]["batch"]
            started.add(index)
            if len(started) == 3:
                ready.set()
            try:
                await asyncio.Event().wait()
            finally:
                stopped.add(index)

        task = asyncio.create_task(reduce_chapter([scan(index) for index in range(1, 4)],
            payload_base={}, fits=lambda p: True, invoke=invoke, batch_bytes=1000, max_rounds=8))
        try:
            await asyncio.wait_for(ready.wait(), 5)
        finally:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, 5)
        self.assertEqual(stopped, {1, 2, 3})

    async def test_multiple_batches_retain_ids_and_finish_with_cross_batch_judgment(self):
        children = [scan(i) for i in range(1, 7)]
        original = copy.deepcopy(children)
        calls = []

        async def invoke(payload, identifiers, compact):
            calls.append(copy.deepcopy(payload))
            self.assertEqual(identifiers, finding_ids(payload["children"]))
            value = {"summary": "Scoped restrictions", "decisions": [{"finding_ids": sorted(identifiers),
                     "verdict": "qualified", "statement": "Scoped requirement", "rationale": "Exceptions apply"}],
                     "relations": [], "gaps": []}
            return adjudication_record(value, identifiers)

        outcome, history = await reduce_chapter(children, payload_base={"jurisdiction": {"id": "chapter-1"}},
            fits=lambda payload: len(encode(payload)) < 4000, invoke=invoke, batch_bytes=1800, max_rounds=8)
        self.assertEqual(children, original)
        self.assertEqual(finding_ids([{"outcome": outcome}]), finding_ids(children))
        self.assertGreater(len(history), 2)
        self.assertEqual(calls[-1]["aggregation"]["mode"], "final")
        self.assertEqual(calls[-1]["aggregation"]["input_kind"], "judgments")
        self.assertTrue(all(payload["jurisdiction"]["id"] == "chapter-1" for payload in calls))

    async def test_one_large_scan_is_partitioned_without_losing_findings_or_gaps(self):
        children = [scan(1, count=6)]
        seen_ids, seen_gaps = set(), []

        async def invoke(payload, identifiers, compact):
            if payload["aggregation"]["input_kind"] == "findings":
                seen_ids.update(identifiers)
                seen_gaps.extend(gap for child in payload["children"] for gap in child["gaps"])
            return {"summary": "Summary", "decisions": [{"finding_ids": sorted(identifiers)}] if identifiers else [], "relations": [], "gaps": []}

        outcome, history = await reduce_chapter(children, payload_base={}, fits=lambda p: len(encode(p)) < 2500,
                                                invoke=invoke, batch_bytes=1400, max_rounds=8)
        self.assertEqual(seen_ids, finding_ids(children))
        self.assertEqual(seen_gaps, children[0]["gaps"])
        self.assertEqual(finding_ids([{"outcome": outcome}]), seen_ids)

    async def test_fixed_context_failure_stops_before_any_call(self):
        async def invoke(*args):
            self.fail("No request should be submitted")
        with self.assertRaisesRegex(EvidenceError, "before any evidence"):
            await reduce_chapter([scan(1)], payload_base={}, fits=lambda p: False,
                                 invoke=invoke, batch_bytes=1000, max_rounds=8)

    async def test_lost_ids_and_nonshrinking_results_fail(self):
        async def drop(payload, identifiers, compact):
            return {"summary": "Dropped", "decisions": [], "relations": [], "gaps": []}
        with self.assertRaisesRegex(EvidenceError, "lost evidence"):
            await reduce_chapter([scan(1), scan(2)], payload_base={}, fits=lambda p: True,
                                 invoke=drop, batch_bytes=500, max_rounds=8)
        async def grow(payload, identifiers, compact):
            return {"summary": "x" * (len(encode(payload)) + 100), "decisions": [{"finding_ids": sorted(identifiers)}], "relations": [], "gaps": []}
        with self.assertRaisesRegex(EvidenceError, "no compression progress"):
            await reduce_chapter([scan(1), scan(2)], payload_base={}, fits=lambda p: True,
                                 invoke=grow, batch_bytes=500, max_rounds=8)


if __name__ == "__main__":
    unittest.main()
