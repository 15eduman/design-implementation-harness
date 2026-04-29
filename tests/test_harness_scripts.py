import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HarnessScriptTests(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_create_and_validate_report_strict_categories(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "qa-report.json"
            self.run_script("scripts/create_qa_report.py", str(report))
            result = self.run_script(
                "scripts/validate_qa_report.py",
                "--allow-draft",
                "--strict-categories",
                str(report),
            )
            self.assertIn("OK:", result.stdout)

    def test_build_agent_packet_out_does_not_pollute_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "packet.json"
            result = self.run_script("scripts/build_agent_packet.py", "visual_qa", "--out", str(out))
            self.assertEqual("", result.stdout)
            packet = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual("visual_qa", packet["role"])
            self.assertIn("Visual QA Agent Prompt", packet["prompt"])

    def test_build_agent_packet_system_is_not_duplicated(self):
        result = self.run_script("scripts/build_agent_packet.py", "system")
        packet = json.loads(result.stdout)
        self.assertEqual("system", packet["role"])
        self.assertEqual(1, packet["prompt"].count("# Agent System Prompt"))


if __name__ == "__main__":
    unittest.main()

