"""Partner data model and CSV loading."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

PARTNER_TYPES = ("isv", "si", "reseller", "cloud", "agency")

_TRUE = {"1", "true", "yes", "y"}


@dataclass(frozen=True)
class Partner:
    """One partner and the signals used to judge the relationship."""

    name: str
    partner_type: str
    region: str
    icp_overlap: float  # share of their customers inside our ICP, 0-1
    integration_depth: int  # 0 none, 1 listed, 2 certified, 3 embedded
    joint_customers: int
    pipeline_sourced: float  # trailing-12-month, USD
    pipeline_influenced: float  # trailing-12-month, USD
    exec_sponsor: bool
    certified_people: int

    def __post_init__(self) -> None:
        if self.partner_type not in PARTNER_TYPES:
            raise ValueError(f"{self.name}: unknown partner type {self.partner_type!r}")
        if not 0.0 <= self.icp_overlap <= 1.0:
            raise ValueError(f"{self.name}: icp_overlap must be between 0 and 1")
        if not 0 <= self.integration_depth <= 3:
            raise ValueError(f"{self.name}: integration_depth must be between 0 and 3")
        for field in ("joint_customers", "pipeline_sourced", "pipeline_influenced", "certified_people"):
            if getattr(self, field) < 0:
                raise ValueError(f"{self.name}: {field} cannot be negative")


def partner_from_row(row: dict[str, str]) -> Partner:
    """Build a Partner from one CSV row of strings."""
    return Partner(
        name=row["name"].strip(),
        partner_type=row["partner_type"].strip().lower(),
        region=row["region"].strip(),
        icp_overlap=float(row["icp_overlap"]),
        integration_depth=int(row["integration_depth"]),
        joint_customers=int(row["joint_customers"]),
        pipeline_sourced=float(row["pipeline_sourced"]),
        pipeline_influenced=float(row["pipeline_influenced"]),
        exec_sponsor=row["exec_sponsor"].strip().lower() in _TRUE,
        certified_people=int(row["certified_people"]),
    )


def load_partners(path: str | Path) -> list[Partner]:
    """Load partners from a CSV file with a header row."""
    with open(path, newline="", encoding="utf-8") as handle:
        return [partner_from_row(row) for row in csv.DictReader(handle)]
