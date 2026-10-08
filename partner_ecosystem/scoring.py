"""Weighted partner fit scoring.

Each dimension is normalized to 0-1, then combined with WEIGHTS into a 0-100
score. Caps keep one outsized number from carrying a partner on its own.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import Partner

WEIGHTS = {
    "icp_fit": 0.30,
    "pipeline": 0.25,
    "integration": 0.20,
    "traction": 0.15,
    "commitment": 0.10,
}

JOINT_CUSTOMER_CAP = 25
PIPELINE_CAP = 2_000_000.0
CERTIFIED_CAP = 20
# Influenced pipeline is real but easier to claim, so it counts for half.
INFLUENCED_DISCOUNT = 0.5


@dataclass(frozen=True)
class PartnerScore:
    partner: str
    dimensions: dict[str, float]
    total: float

    @property
    def weakest(self) -> str:
        """The dimension holding the score back most."""
        return min(self.dimensions, key=self.dimensions.get)


def _capped(value: float, cap: float) -> float:
    return min(value / cap, 1.0)


def score_dimensions(partner: Partner) -> dict[str, float]:
    """Return each scoring dimension for a partner, normalized to 0-1."""
    weighted_pipeline = partner.pipeline_sourced + INFLUENCED_DISCOUNT * partner.pipeline_influenced
    commitment = 0.6 * partner.exec_sponsor + 0.4 * _capped(partner.certified_people, CERTIFIED_CAP)
    return {
        "icp_fit": partner.icp_overlap,
        "pipeline": _capped(weighted_pipeline, PIPELINE_CAP),
        "integration": partner.integration_depth / 3,
        "traction": _capped(partner.joint_customers, JOINT_CUSTOMER_CAP),
        "commitment": commitment,
    }


def score_partner(partner: Partner, weights: dict[str, float] | None = None) -> PartnerScore:
    """Score a partner from 0 to 100 using the given weights."""
    weights = weights or WEIGHTS
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1")
    dimensions = score_dimensions(partner)
    if set(weights) != set(dimensions):
        raise ValueError("weights must cover exactly the scoring dimensions")
    total = 100 * sum(weights[name] * value for name, value in dimensions.items())
    return PartnerScore(partner=partner.name, dimensions=dimensions, total=round(total, 1))
