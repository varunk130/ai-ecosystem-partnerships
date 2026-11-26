import contextlib
import io
import tempfile
import unittest
from datetime import date
from pathlib import Path

from partner_ecosystem.attribution import load_opportunities
from partner_ecosystem.cli import main
from partner_ecosystem.models import load_partners
from partner_ecosystem.overlap import load_our_accounts, load_partner_accounts, map_overlap
from partner_ecosystem.report import analyze, money, recommendations, render_html

DATA = Path(__file__).resolve().parent.parent / "data"


def sample():
    return analyze(
        load_partners(DATA / "partners.csv"),
        map_overlap(load_our_accounts(DATA / "our_accounts.csv"), load_partner_accounts(DATA / "partner_accounts.csv")),
        load_opportunities(DATA / "opportunities.csv"),
    )


class MoneyTests(unittest.TestCase):
    def test_formats_each_scale(self):
        self.assertEqual(money(980_000), "$980K")
        self.assertEqual(money(1_000_000), "$1M")
        self.assertEqual(money(1_250_000), "$1.2M")
        self.assertEqual(money(900), "$900")


class AnalyzeTests(unittest.TestCase):
    def test_partners_are_ranked_by_score(self):
        scores = [p.score for p in sample().partners]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_live_plays_come_first_largest_deal_first(self):
        plays = sample().plays
        self.assertEqual((plays[0].account, plays[0].partner, plays[0].play), ("Dovetail Bank", "Halcyon Cloud", "co-sell"))


class RecommendationTests(unittest.TestCase):
    def test_actions_cover_deals_balance_and_portfolio(self):
        headlines = [headline for headline, _ in recommendations(sample())]
        # Harborline Logistics has two live plays; its open amount counts once.
        self.assertEqual(headlines[0], "Run 4 partner plays on $925K of open deals")
        self.assertEqual(headlines[1], "Give before the next ask to Halcyon Cloud and Northwind Data")
        self.assertIn("Review 5 borderline partners before changing tiers", headlines)
        self.assertIn("Move 4 Watchlist partners to the self-serve program", headlines)

    def test_strategic_partners_with_the_same_gap_are_grouped(self):
        detail = dict(recommendations(sample()))["Invest in the 3 Strategic partners where they are weakest"]
        self.assertTrue(detail.startswith("Northwind Data and Halcyon Cloud: focus joint targeting"))


class RenderTests(unittest.TestCase):
    def test_headline_and_sections(self):
        html = render_html(sample(), as_of=date(2026, 11, 26))
        self.assertIn("Partners helped win $980K and lift win rate by 31 points.", html)
        self.assertIn("November 26, 2026", html)
        for section in ("What to do this quarter", "Portfolio: who earns investment", "Co-sell plays on shared accounts", "What partners delivered"):
            self.assertIn(section, html)

    def test_partner_names_are_escaped(self):
        self.assertIn("Lumen &amp; Vale", render_html(sample()))
        self.assertNotIn("Lumen & Vale", render_html(sample()))

    def test_page_is_self_contained(self):
        html = render_html(sample())
        self.assertNotIn("<script", html)
        self.assertNotIn("http", html)


class WeightsTests(unittest.TestCase):
    def test_footer_shows_the_weights_used(self):
        heavy = {"icp_fit": 0.2, "pipeline": 0.4, "integration": 0.2, "traction": 0.1, "commitment": 0.1}
        eco = analyze(
            load_partners(DATA / "partners.csv"),
            map_overlap(load_our_accounts(DATA / "our_accounts.csv"), load_partner_accounts(DATA / "partner_accounts.csv")),
            load_opportunities(DATA / "opportunities.csv"),
            heavy,
        )
        self.assertIn("Pipeline 40%", render_html(eco))


class ReportCommandTests(unittest.TestCase):
    def test_writes_the_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nested" / "review.html"
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = main(["report", str(DATA), "--out", str(out)])
            self.assertEqual(code, 0)
            self.assertIn("What to do this quarter", out.read_text(encoding="utf-8"))
            self.assertIn(str(out), buffer.getvalue())

    def test_missing_folder_is_a_clean_error(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = main(["report", "no-such-folder"])
        self.assertEqual(code, 2)
        self.assertIn("file not found", err.getvalue())


if __name__ == "__main__":
    unittest.main()
