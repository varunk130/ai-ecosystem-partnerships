import unittest
from pathlib import Path

from partner_ecosystem.models import Partner, load_partners
from partner_ecosystem.scoring import WEIGHTS, score_dimensions, score_partner
from partner_ecosystem.tiering import assign_tier

DATA = Path(__file__).resolve().parent.parent / "data"


def make_partner(**overrides):
    fields = dict(
        name="Example",
        partner_type="isv",
        region="NA",
        icp_overlap=0.5,
        integration_depth=1,
        joint_customers=5,
        pipeline_sourced=100_000,
        pipeline_influenced=200_000,
        exec_sponsor=False,
        certified_people=4,
    )
    fields.update(overrides)
    return Partner(**fields)


class ModelTests(unittest.TestCase):
    def test_sample_dataset_loads(self):
        partners = load_partners(DATA / "partners.csv")
        self.assertEqual(len(partners), 12)
        self.assertTrue(partners[0].exec_sponsor)

    def test_rejects_out_of_range_overlap(self):
        with self.assertRaises(ValueError):
            make_partner(icp_overlap=1.4)

    def test_rejects_unknown_type(self):
        with self.assertRaises(ValueError):
            make_partner(partner_type="friend")


class ScoringTests(unittest.TestCase):
    def test_perfect_partner_scores_100(self):
        partner = make_partner(
            icp_overlap=1.0,
            integration_depth=3,
            joint_customers=50,
            pipeline_sourced=5_000_000,
            exec_sponsor=True,
            certified_people=60,
        )
        self.assertEqual(score_partner(partner).total, 100.0)

    def test_empty_partner_scores_zero(self):
        partner = make_partner(
            icp_overlap=0.0,
            integration_depth=0,
            joint_customers=0,
            pipeline_sourced=0,
            pipeline_influenced=0,
            certified_people=0,
        )
        self.assertEqual(score_partner(partner).total, 0.0)

    def test_influenced_pipeline_counts_half(self):
        sourced = score_dimensions(make_partner(pipeline_sourced=400_000, pipeline_influenced=0))
        influenced = score_dimensions(make_partner(pipeline_sourced=0, pipeline_influenced=800_000))
        self.assertAlmostEqual(sourced["pipeline"], influenced["pipeline"])

    def test_known_score(self):
        # 0.30*0.5 + 0.25*0.1 + 0.20*(1/3) + 0.15*0.2 + 0.10*0.08 = 0.27967
        self.assertEqual(score_partner(make_partner()).total, 28.0)

    def test_weakest_dimension(self):
        self.assertEqual(score_partner(make_partner()).weakest, "commitment")

    def test_weights_must_sum_to_one(self):
        with self.assertRaises(ValueError):
            score_partner(make_partner(), {**WEIGHTS, "icp_fit": 0.9})


class TieringTests(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual(assign_tier(75).name, "Strategic")
        self.assertEqual(assign_tier(74.9).name, "Growth")
        self.assertEqual(assign_tier(55).name, "Growth")
        self.assertEqual(assign_tier(35).name, "Emerging")
        self.assertEqual(assign_tier(0).name, "Watchlist")

    def test_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            assign_tier(101)


if __name__ == "__main__":
    unittest.main()
