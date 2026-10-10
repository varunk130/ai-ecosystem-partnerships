import unittest
from pathlib import Path

from partner_ecosystem.attribution import Opportunity, attribute, load_opportunities, win_rate_lift

DATA = Path(__file__).resolve().parent.parent / "data"


def opp(opp_id, amount, stage, partner="", role="none"):
    return Opportunity(opp_id, "Account", amount, stage, partner, role)


class OpportunityTests(unittest.TestCase):
    def test_role_requires_partner(self):
        with self.assertRaises(ValueError):
            opp("O-1", 100, "won", partner="", role="sourced")

    def test_partner_requires_role(self):
        with self.assertRaises(ValueError):
            opp("O-1", 100, "won", partner="P", role="none")


class LoadOpportunitiesTests(unittest.TestCase):
    def test_sample_data_has_normalized_domains(self):
        opportunities = load_opportunities(DATA / "opportunities.csv")
        self.assertEqual(opportunities[0].domain, "acmefreight.example")

    def test_domain_defaults_to_empty(self):
        self.assertEqual(opp("O-1", 10, "open").domain, "")


class AttributeTests(unittest.TestCase):
    def test_splits_sourced_and_influenced_won_revenue(self):
        result = attribute(
            [
                opp("O-1", 100, "won", "P", "sourced"),
                opp("O-2", 40, "won", "P", "influenced"),
                opp("O-3", 70, "open", "P", "sourced"),
                opp("O-4", 90, "lost", "P", "influenced"),
                opp("O-5", 500, "won"),
            ]
        )
        self.assertEqual(len(result), 1)
        entry = result[0]
        self.assertEqual((entry.sourced_won, entry.influenced_won, entry.open_pipeline), (100, 40, 70))
        self.assertAlmostEqual(entry.win_rate, 2 / 3)

    def test_win_rate_is_none_without_closed_deals(self):
        self.assertIsNone(attribute([opp("O-1", 10, "open", "P", "sourced")])[0].win_rate)

    def test_sample_data_ranking(self):
        result = attribute(load_opportunities(DATA / "opportunities.csv"))
        self.assertEqual([entry.partner for entry in result], ["Halcyon Cloud", "Northwind Data", "Brightline Consulting"])
        self.assertEqual(result[0].sourced_won, 150000)
        self.assertEqual(result[0].influenced_won, 320000)


class WinRateLiftTests(unittest.TestCase):
    def test_sample_data_lift(self):
        lift = win_rate_lift(load_opportunities(DATA / "opportunities.csv"))
        self.assertAlmostEqual(lift["attached"], 5 / 7)
        self.assertAlmostEqual(lift["unattached"], 2 / 5)
        self.assertAlmostEqual(lift["lift"], 5 / 7 - 2 / 5)

    def test_lift_is_none_when_a_side_has_no_closed_deals(self):
        self.assertIsNone(win_rate_lift([opp("O-1", 10, "won", "P", "sourced")])["lift"])


if __name__ == "__main__":
    unittest.main()
