import unittest
from pathlib import Path

from partner_ecosystem.overlap import (
    PLAY_PRIORITY,
    PLAYS,
    Overlap,
    give_ask_balance,
    load_our_accounts,
    load_partner_accounts,
    map_overlap,
    normalize_domain,
    rank_overlaps,
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

    def test_sample_data_give_ask_balance(self):
        balance = give_ask_balance(
            map_overlap(
                load_our_accounts(DATA / "our_accounts.csv"),
                load_partner_accounts(DATA / "partner_accounts.csv"),
            )
        )
        self.assertEqual(balance["Brightline Consulting"], {"asks": 1, "gives": 1})
        self.assertEqual(balance["Halcyon Cloud"], {"asks": 2, "gives": 0})


class RankOverlapsTests(unittest.TestCase):
    def overlap(self, domain, play, partner="P"):
        return Overlap(partner, domain, domain.split(".")[0].upper(), "open_opp", "customer", play)

    def test_every_play_has_a_priority(self):
        self.assertEqual(set(PLAY_PRIORITY), set(PLAYS.values()))

    def test_larger_open_amount_comes_first_within_a_play(self):
        overlaps = [self.overlap("small.example", "co-sell"), self.overlap("big.example", "co-sell")]
        ranked = rank_overlaps(overlaps, {"small.example": 10, "big.example": 500})
        self.assertEqual([overlap.domain for overlap in ranked], ["big.example", "small.example"])

    def test_play_priority_beats_amount(self):
        overlaps = [self.overlap("a.example", "co-marketing"), self.overlap("b.example", "co-sell")]
        ranked = rank_overlaps(overlaps, {"a.example": 999})
        self.assertEqual([overlap.play for overlap in ranked], ["co-sell", "co-marketing"])

    def test_partners_stay_grouped(self):
        overlaps = [self.overlap("a.example", "co-sell", "Zed"), self.overlap("b.example", "co-marketing", "Abe")]
        self.assertEqual([overlap.partner for overlap in rank_overlaps(overlaps, {})], ["Abe", "Zed"])


if __name__ == "__main__":
    unittest.main()
