"""Account mapping: find shared accounts and the play each one suggests."""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

OUR_STATUSES = ("customer", "open_opp", "prospect")
PARTNER_STATUSES = ("customer", "prospect")

# (our status, partner status) -> the play worth running on that account.
PLAYS = {
    ("open_opp", "customer"): "co-sell",
    ("prospect", "customer"): "intro request",
    ("customer", "customer"): "joint expansion",
    ("customer", "prospect"): "referral to partner",
    ("open_opp", "prospect"): "joint pursuit",
    ("prospect", "prospect"): "co-marketing",
}


# Plays where we need something from the partner, and where we bring them something.
ASK_PLAYS = ("co-sell", "intro request")
GIVE_PLAYS = ("referral to partner",)


@dataclass(frozen=True)
class Overlap:
    partner: str
    domain: str
    account: str
    our_status: str
    partner_status: str
    play: str


def normalize_domain(value: str) -> str:
    """Reduce a URL or hostname to a bare lowercase domain for matching."""
    domain = value.strip().lower()
    if "://" in domain:
        domain = domain.split("://", 1)[1]
    domain = domain.split("/", 1)[0].split(":", 1)[0]
    return domain.removeprefix("www.")


def _read(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_our_accounts(path: str | Path) -> dict[str, dict[str, str]]:
    """Load our account list keyed by normalized domain."""
    accounts = {}
    for row in _read(path):
        status = row["status"].strip().lower()
        if status not in OUR_STATUSES:
            raise ValueError(f"{row['name']}: unknown status {status!r}")
        accounts[normalize_domain(row["domain"])] = {"name": row["name"].strip(), "status": status}
    return accounts


def load_partner_accounts(path: str | Path) -> list[dict[str, str]]:
    """Load partner account rows with normalized domains."""
    rows = []
    for row in _read(path):
        status = row["status"].strip().lower()
        if status not in PARTNER_STATUSES:
            raise ValueError(f"{row['partner']}: unknown status {status!r}")
        rows.append({"partner": row["partner"].strip(), "domain": normalize_domain(row["domain"]), "status": status})
    return rows


def map_overlap(our_accounts: dict[str, dict[str, str]], partner_rows: list[dict[str, str]]) -> list[Overlap]:
    """Return one Overlap per partner account that also appears in our list."""
    overlaps = []
    for row in partner_rows:
        ours = our_accounts.get(row["domain"])
        if ours is None:
            continue
        overlaps.append(
            Overlap(
                partner=row["partner"],
                domain=row["domain"],
                account=ours["name"],
                our_status=ours["status"],
                partner_status=row["status"],
                play=PLAYS[(ours["status"], row["status"])],
            )
        )
    return overlaps


def summarize(overlaps: list[Overlap]) -> dict[str, Counter]:
    """Count plays per partner."""
    summary: dict[str, Counter] = {}
    for overlap in overlaps:
        summary.setdefault(overlap.partner, Counter())[overlap.play] += 1
    return summary


def give_ask_balance(overlaps: list[Overlap]) -> dict[str, dict[str, int]]:
    """Count what we ask of each partner against what we give them."""
    return {
        partner: {
            "asks": sum(plays[play] for play in ASK_PLAYS),
            "gives": sum(plays[play] for play in GIVE_PLAYS),
        }
        for partner, plays in summarize(overlaps).items()
    }
