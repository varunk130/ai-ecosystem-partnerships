"""Partner attribution: sourced vs influenced revenue and win-rate lift."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

STAGES = ("open", "won", "lost")
ROLES = ("sourced", "influenced", "none")


@dataclass(frozen=True)
class Opportunity:
    opp_id: str
    account: str
    amount: float
    stage: str
    partner: str
    role: str

    def __post_init__(self) -> None:
        if self.stage not in STAGES:
            raise ValueError(f"{self.opp_id}: unknown stage {self.stage!r}")
        if self.role not in ROLES:
            raise ValueError(f"{self.opp_id}: unknown role {self.role!r}")
        if (self.role == "none") != (self.partner == ""):
            raise ValueError(f"{self.opp_id}: partner and role must be set together")


@dataclass
class PartnerAttribution:
    partner: str
    sourced_won: float = 0.0
    influenced_won: float = 0.0
    open_pipeline: float = 0.0
    won: int = 0
    lost: int = 0

    @property
    def win_rate(self) -> float | None:
        return win_rate(self.won, self.lost)


def win_rate(won: int, lost: int) -> float | None:
    """Won share of closed deals, or None when nothing has closed."""
    closed = won + lost
    return won / closed if closed else None


def load_opportunities(path: str | Path) -> list[Opportunity]:
    """Load opportunities from a CSV file with a header row."""
    with open(path, newline="", encoding="utf-8") as handle:
        return [
            Opportunity(
                opp_id=row["opp_id"].strip(),
                account=row["account"].strip(),
                amount=float(row["amount"]),
                stage=row["stage"].strip().lower(),
                partner=row["partner"].strip(),
                role=row["role"].strip().lower(),
            )
            for row in csv.DictReader(handle)
        ]


def attribute(opportunities: list[Opportunity]) -> list[PartnerAttribution]:
    """Roll opportunities up per partner, largest won revenue first."""
    by_partner: dict[str, PartnerAttribution] = {}
    for opp in opportunities:
        if opp.role == "none":
            continue
        entry = by_partner.setdefault(opp.partner, PartnerAttribution(opp.partner))
        if opp.stage == "open":
            entry.open_pipeline += opp.amount
        elif opp.stage == "lost":
            entry.lost += 1
        else:
            entry.won += 1
            if opp.role == "sourced":
                entry.sourced_won += opp.amount
            else:
                entry.influenced_won += opp.amount
    return sorted(by_partner.values(), key=lambda entry: entry.sourced_won + entry.influenced_won, reverse=True)


def win_rate_lift(opportunities: list[Opportunity]) -> dict[str, float | None]:
    """Compare win rate on partner-attached deals with unattached deals."""
    counts = {True: [0, 0], False: [0, 0]}  # attached -> [won, lost]
    for opp in opportunities:
        if opp.stage != "open":
            counts[opp.role != "none"][opp.stage == "lost"] += 1
    attached = win_rate(*counts[True])
    unattached = win_rate(*counts[False])
    lift = None if attached is None or unattached is None else attached - unattached
    return {"attached": attached, "unattached": unattached, "lift": lift}
