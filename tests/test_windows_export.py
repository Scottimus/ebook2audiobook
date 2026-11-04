"""Exercise the real finalize function with mocked synthesis and session storage."""
import ast
import contextlib
import io
import os
from pathlib import Path
from types import SimpleNamespace
import unittest


class ExportRegressionTests(unittest.TestCase):
    def run_finalize(self, directory=False, exports=None):
        source = Path(__file__).resolve().parents[1] / "lib/core.py"
        node = next(node for node in ast.parse(source.read_text(encoding="utf-8")).body
                    if isinstance(node, ast.FunctionDef) and node.name == "finalize_audiobook")
        session = {"id": "sample", "status": "edit", "blocks_current": {"blocks": []},
                   "cancellation_requested": False, "ebook": "sample.txt",
                   "ebook_mode": "directory" if directory else "single",
                   "ebook_src": "sample.txt", "ebook_list": ["sample.txt", "next.txt"]}
        alerts = []

        def reset(*args, **kwargs):
            session["audiobook"] = None
            session["audiobooks_dir"] = None

        namespace = {"context": SimpleNamespace(get_session=lambda key: session),
                     "status_tags": {key: key.lower() for key in ("END", "EDIT", "CONVERTING", "DISCONNECTED")},
                     "ebook_modes": {key: key.lower() for key in ("DIRECTORY", "SINGLE", "TEXT")},
                     "convert_chapters2audio": lambda key: True,
                     "combine_audio_chapters": lambda key: exports,
                     "reset_ebook_session": reset, "os": os,
                     "show_alert": lambda key, alert: alerts.append(alert),
                     "DependencyError": lambda error: None, "exception_alert": lambda *args: None}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)
        with contextlib.redirect_stdout(io.StringIO()):
            result = namespace["finalize_audiobook"]("sample")
        return result, session, alerts

    def test_single_export_survives_session_reset(self):
        result, session, alerts = self.run_finalize(exports=["output/sample.wav"])
        self.assertTrue(result[1])
        self.assertEqual(session["audiobook"], "output/sample.wav")
        self.assertEqual(session["audiobooks_dir"], "output")
        self.assertIn("Saved to: output/sample.wav", alerts[-1]["msg"])

    def test_directory_export_preserves_last_output(self):
        result, session, alerts = self.run_finalize(directory=True, exports=["output/sample.wav"])
        self.assertTrue(result[1])
        self.assertEqual(session["audiobook"], "output/sample.wav")
        self.assertIn("1 ebook(s)", alerts[-1]["msg"])

    def test_empty_export_fails(self):
        result, session, alerts = self.run_finalize(exports=[])
        self.assertFalse(result[1])


if __name__ == "__main__":
    unittest.main()
