"""Command-line entry point: partner-eco <command>."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from .models import load_partners
from .scoring import score_partner
from .tiering import assign_tier


def format_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    """Render rows as a plain-text table with left-aligned, padded columns."""
    cells = [[str(value) for value in row] for row in rows]
    widths = [max(len(headers[i]), *(len(row[i]) for row in cells)) for i in range(len(headers))]
    lines = ["  ".join(header.ljust(width) for header, width in zip(headers, widths)).rstrip()]
    lines.append("  ".join("-" * width for width in widths))
    lines.extend("  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip() for row in cells)
    return "\n".join(lines)


def _emit(args: argparse.Namespace, records: list[dict], headers: Sequence[str]) -> None:
    if args.json:
        print(json.dumps(records, indent=2))
    else:
        print(format_table(headers, [[record[header] for header in headers] for record in records]))


def cmd_score(args: argparse.Namespace) -> int:
    records = []
    for partner in load_partners(args.partners):
        score = score_partner(partner)
        tier = assign_tier(score.total)
        records.append(
            {
                "partner": partner.name,
                "type": partner.partner_type,
                "score": score.total,
                "tier": tier.name,
                "weakest": score.weakest,
                "motion": tier.motion,
            }
        )
    records.sort(key=lambda record: record["score"], reverse=True)
    _emit(args, records, ["partner", "type", "score", "tier", "weakest", "motion"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="partner-eco", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    score = commands.add_parser("score", help="score and tier every partner")
    score.add_argument("partners", help="path to partners CSV")
    score.set_defaults(func=cmd_score)

    for command in commands.choices.values():
        command.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
