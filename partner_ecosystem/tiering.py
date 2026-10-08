"""Turn a fit score into a tier and the motion that tier earns."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Tier:
    name: str
    min_score: float
    motion: str


# Ordered highest first; assign_tier returns the first tier the score clears.
TIERS = (
    Tier("Strategic", 75, "Joint business plan, exec cadence, dedicated co-sell"),
    Tier("Growth", 55, "Targeted account mapping and co-marketing"),
    Tier("Emerging", 35, "Enablement and first joint wins"),
    Tier("Watchlist", 0, "Self-serve program, review quarterly"),
)


def assign_tier(score: float) -> Tier:
    """Return the tier for a 0-100 fit score."""
    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")
    for tier in TIERS:
        if score >= tier.min_score:
            return tier
    raise AssertionError("TIERS must end with a zero-floor tier")
