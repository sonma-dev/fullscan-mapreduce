import copy
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from server import output_files
from server.specifications import SPECIFICATION_STAGES


DEFAULT_OUTPUT_DIR = output_files.OUTPUT_DIR


class OutputFileTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.directory = self.base / "res"
        output_patch = patch.object(output_files, "OUTPUT_DIR", self.directory)
        output_patch.start()
        self.addCleanup(output_patch.stop)
        clock_patch = patch.object(output_files, "datetime")
        clock = clock_patch.start()
        self.addCleanup(clock_patch.stop)
        clock.now.return_value = datetime(2026, 11, 9, 15, 4, 5, tzinfo=timezone.utc).astimezone(output_files.JST)
        self.clock = clock
        self.timestamp = "20261110000405"
        self.payload = {
            "file_name": "source.pdf",
            "request": "generate_specifications",
            "specifications": [
                {"step": stage.step, "key": stage.key, "content": f"# {stage.english_title}\n\nUnicode: 画面"}
                for stage in SPECIFICATION_STAGES
            ],
            "reply": "Combined specifications",
            "usage": {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
            "timing_ms": {"llm": 100, "total": 110},
        }

    def test_only_eight_markdown_files_are_saved_in_jst_run_directory(self):
        with patch.object(output_files.time, "perf_counter", return_value=100.125):
            result = output_files.save_output_files(self.payload, total_started_at=100.0)
        self.clock.now.assert_called_once_with(output_files.JST)
        files = result["output_files"]
        self.assertEqual(set(files), {"markdown"})
        self.assertEqual(result["timing_ms"]["total"], 125)
        self.assertEqual(result["usage"], self.payload["usage"])
        self.assertNotIn("output_files", self.payload)
        self.assertEqual(len(files["markdown"]), 8)
        directory = (self.base / files["markdown"][0]).parent
        self.assertEqual(directory.parent, self.directory)
        self.assertTrue(directory.name.startswith(f"{output_files.OUTPUT_PREFIX}_{self.timestamp}_"))
        for specification, filename in zip(self.payload["specifications"], files["markdown"]):
            path = self.base / filename
            self.assertEqual(path.parent, directory)
            self.assertEqual(path.name, f'{specification["step"]:02d}_{specification["key"]}.md')
            self.assertEqual(path.read_text(encoding="utf-8"), specification["content"] + "\n")
        self.assertEqual(Path(files["markdown"][-1]).name, "08_architecture_decision.md")
        self.assertEqual({path.suffix for path in directory.iterdir()}, {".md"})
        self.assertEqual(len(list(directory.iterdir())), 8)

    def test_same_second_exports_have_separate_directories(self):
        first = output_files.save_output_files(self.payload)
        second_payload = copy.deepcopy(self.payload)
        second_payload["specifications"][0]["content"] = "A different run"
        second = output_files.save_output_files(second_payload)
        first_path = self.base / first["output_files"]["markdown"][0]
        second_path = self.base / second["output_files"]["markdown"][0]
        self.assertNotEqual(first_path.parent, second_path.parent)
        self.assertEqual(first_path.name, second_path.name)
        self.assertEqual(first_path.read_text(encoding="utf-8"), self.payload["specifications"][0]["content"] + "\n")
        self.assertEqual(second_path.read_text(encoding="utf-8"), "A different run\n")

    def test_invalid_filename_components_are_rejected_before_writing(self):
        for changes in ({"key": "../escape"}, {"key": "bad/name"}, {"step": True}, {"step": 0}):
            with self.subTest(changes=changes):
                payload = copy.deepcopy(self.payload)
                payload["specifications"][0].update(changes)
                with self.assertRaisesRegex(ValueError, "filename components"):
                    output_files.save_output_files(payload)
                self.assertFalse(self.directory.exists())

    def test_duplicate_filenames_are_rejected_before_writing(self):
        payload = copy.deepcopy(self.payload)
        payload["specifications"].append(payload["specifications"][0])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            output_files.save_output_files(payload)
        self.assertFalse(self.directory.exists())

    def test_write_failure_removes_only_the_failed_export(self):
        first = output_files.save_output_files(self.payload)
        first_path = self.base / first["output_files"]["markdown"][0]
        with patch.object(Path, "write_text", side_effect=OSError("Disk full")):
            with self.assertRaisesRegex(OSError, "Disk full"):
                output_files.save_output_files(self.payload)
        self.assertEqual(list(self.directory.iterdir()), [first_path.parent])
        self.assertEqual(first_path.read_text(encoding="utf-8"), self.payload["specifications"][0]["content"] + "\n")

    def test_default_output_directory_is_at_repository_top(self):
        repository = next(parent for parent in Path(__file__).resolve().parents if (parent / "experiment").is_dir())
        self.assertEqual(DEFAULT_OUTPUT_DIR, repository / "res")

    def test_completed_markdown_is_reused_without_rewriting(self):
        export = output_files.OutputFiles()
        first_path = None
        for count in range(1, 9):
            payload = {**self.payload, "specifications": self.payload["specifications"][:count]}
            saved = export.save(payload, complete=False)
            self.assertEqual(saved["status"], "partial")
            self.assertEqual(len(list(export.directory.iterdir())), count)
            if first_path is None:
                first_path = self.base / saved["output_files"]["markdown"][0]
                first_path.write_text("Reviewed specification\n", encoding="utf-8")
            self.assertEqual(first_path.read_text(encoding="utf-8"), "Reviewed specification\n")
        with patch.object(Path, "write_text", side_effect=AssertionError("Completed files must not be rewritten")):
            final = export.save(self.payload)
        self.assertEqual(final["status"], "completed")
        self.assertEqual(final["output_files"], saved["output_files"])
        self.assertEqual(len(list(self.directory.iterdir())), 1)
        self.assertEqual(len(list(export.directory.iterdir())), 8)
        self.clock.now.assert_called_once_with(output_files.JST)

    def test_failed_commit_rolls_back_new_files_and_preserves_completed_stages(self):
        for completed in (0, 2):
            with self.subTest(completed=completed):
                export = output_files.OutputFiles()
                if completed:
                    export.save({**self.payload, "specifications": self.payload["specifications"][:completed]}, complete=False)
                before = {path.name: path.read_bytes() for path in export.directory.iterdir()} if completed else {}
                replace = Path.replace
                commits = []

                def fail_second_commit(source, target):
                    commits.append(Path(target))
                    if len(commits) == 2:
                        raise OSError("Markdown replacement failed")
                    return replace(source, target)

                with patch.object(Path, "replace", fail_second_commit):
                    with self.assertRaisesRegex(OSError, "Markdown replacement failed"):
                        export.save(self.payload)
                if completed:
                    self.assertEqual({path.name: path.read_bytes() for path in export.directory.iterdir()}, before)
                else:
                    self.assertIsNone(export.directory)
                    self.assertFalse(commits[0].parent.exists())
                final = export.save(self.payload)
                self.assertEqual(final["status"], "completed")
                self.assertEqual(len(list(export.directory.iterdir())), 8)


if __name__ == "__main__":
    unittest.main()
