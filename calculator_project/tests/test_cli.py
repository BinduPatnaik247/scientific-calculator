import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, "-m", "calc_app", *args], cwd=ROOT,
                          capture_output=True, text=True, timeout=5)


class CliTests(unittest.TestCase):
    def test_text_output(self):
        process = run("add", "2", "3")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, "5\n")

    def test_json_output(self):
        process = run("multiply", "2.5", "4", "--json")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)["result"], "10")

    def test_json_domain_error(self):
        process = run("divide", "1", "0", "--json")
        self.assertEqual(process.returncode, 2)
        self.assertIn("zero", json.loads(process.stdout)["error"])

    def test_text_domain_error(self):
        process = run("add", "oops", "2")
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, "")
        self.assertIn("Error:", process.stderr)
        self.assertNotIn("Traceback", process.stderr)

    def test_missing_operand(self):
        self.assertEqual(run("add", "1").returncode, 2)

    def test_unknown_command(self):
        self.assertEqual(run("oops").returncode, 2)

    def test_help(self):
        process = run("--help")
        self.assertEqual(process.returncode, 0)
        self.assertIn("divide", process.stdout)

    def test_version(self):
        self.assertEqual(run("--version").stdout.strip(), "1.0.0")
