import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from partner_ecosystem.cli import main

DATA = Path(__file__).resolve().parent.parent / "data"
PARTNERS = str(DATA / "partners.csv")


def run(*argv):
    """Run the CLI and return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class ScoreCommandTests(unittest.TestCase):
    def test_json_marks_borderline_partners(self):
        code, out, _ = run("score", PARTNERS, "--json")
        self.assertEqual(code, 0)
        borderline = {record["partner"]: record["borderline"] for record in json.loads(out)}
        self.assertTrue(borderline["Brightline Consulting"])
        self.assertFalse(borderline["Kestrel AI"])

    def test_partner_filter_ignores_case(self):
        code, out, _ = run("score", PARTNERS, "--json", "--partner", "kestrel ai")
        self.assertEqual(code, 0)
        self.assertEqual([record["partner"] for record in json.loads(out)], ["Kestrel AI"])

    def test_custom_weights_change_the_ranking_input(self):
        _, default, _ = run("score", PARTNERS, "--json", "--partner", "Osprey Labs")
        _, heavy, _ = run(
            "score", PARTNERS, "--json", "--partner", "Osprey Labs", "--weights", str(DATA / "weights.pipeline-heavy.json")
        )
        self.assertLess(json.loads(heavy)[0]["score"], json.loads(default)[0]["score"])


class ErrorHandlingTests(unittest.TestCase):
    def test_unknown_partner(self):
        code, out, err = run("score", PARTNERS, "--partner", "Nobody Inc")
        self.assertEqual((code, out), (2, ""))
        self.assertIn("no partner named 'Nobody Inc'", err)

    def test_missing_file(self):
        code, _, err = run("score", "nope.csv")
        self.assertEqual(code, 2)
        self.assertIn("file not found: nope.csv", err)

    def test_missing_column(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as handle:
            handle.write("name\nExample\n")
        self.addCleanup(Path(handle.name).unlink)
        code, _, err = run("score", handle.name)
        self.assertEqual(code, 2)
        self.assertIn("missing the required column 'partner_type'", err)


if __name__ == "__main__":
    unittest.main()
