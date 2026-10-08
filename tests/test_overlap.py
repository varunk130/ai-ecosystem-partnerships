import unittest
from pathlib import Path

from partner_ecosystem.overlap import (
    load_our_accounts,
    load_partner_accounts,
    map_overlap,
    normalize_domain,
    summarize,
)

DATA = Path(__file__).resolve().parent.parent / "data"


class NormalizeDomainTests(unittest.TestCase):
    def test_strips_scheme_www_path_and_case(self):
        self.assertEqual(normalize_domain("https://WWW.Example.com/pricing?x=1"), "example.com")

    def test_strips_port_and_whitespace(self):
        self.assertEqual(normalize_domain("  example.com:8443 "), "example.com")

    def test_keeps_other_subdomains(self):
        self.assertEqual(normalize_domain("app.example.com"), "app.example.com")


class MapOverlapTests(unittest.TestCase):
    def setUp(self):
        self.ours = {
            "a.example": {"name": "A", "status": "open_opp"},
            "b.example": {"name": "B", "status": "prospect"},
        }

    def test_assigns_play_from_both_statuses(self):
        rows = [
            {"partner": "P", "domain": "a.example", "status": "customer"},
            {"partner": "P", "domain": "b.example", "status": "prospect"},
        ]
        plays = [overlap.play for overlap in map_overlap(self.ours, rows)]
        self.assertEqual(plays, ["co-sell", "co-marketing"])

    def test_ignores_accounts_we_do_not_track(self):
        rows = [{"partner": "P", "domain": "z.example", "status": "customer"}]
        self.assertEqual(map_overlap(self.ours, rows), [])

    def test_sample_data_summary(self):
        overlaps = map_overlap(
            load_our_accounts(DATA / "our_accounts.csv"),
            load_partner_accounts(DATA / "partner_accounts.csv"),
        )
        self.assertEqual(len(overlaps), 11)
        summary = summarize(overlaps)
        self.assertEqual(summary["Northwind Data"]["co-sell"], 1)
        self.assertEqual(summary["Halcyon Cloud"]["joint expansion"], 1)
        self.assertEqual(summary["Brightline Consulting"]["co-sell"], 1)


if __name__ == "__main__":
    unittest.main()
