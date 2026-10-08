"""Command-line entry point: partner-eco <command>."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from .attribution import attribute, load_opportunities, win_rate_lift
from .models import load_partners
from .overlap import load_our_accounts, load_partner_accounts, map_overlap
from .scoring import load_weights, score_partner
from .tiering import assign_tier, is_borderline


def _cell(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else ""
    return str(value)


def format_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    """Render rows as a plain-text table with left-aligned, padded columns."""
    cells = [[_cell(value) for value in row] for row in rows]
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


def _filter_partner(args: argparse.Namespace, records: list[dict]) -> list[dict]:
    """Keep only the requested partner's records, or all when no filter is set."""
    if not args.partner:
        return records
    wanted = args.partner.strip().casefold()
    matched = [record for record in records if record["partner"].casefold() == wanted]
    if not matched:
        raise ValueError(f"no partner named {args.partner!r} in the input")
    return matched


def cmd_score(args: argparse.Namespace) -> int:
    """Score and tier every partner, highest score first."""
    weights = load_weights(args.weights) if args.weights else None
    records = []
    for partner in load_partners(args.partners):
        score = score_partner(partner, weights)
        tier = assign_tier(score.total)
        records.append(
            {
                "partner": partner.name,
                "type": partner.partner_type,
                "score": score.total,
                "tier": tier.name,
                "borderline": is_borderline(score.total),
                "weakest": score.weakest,
                "motion": tier.motion,
            }
        )
    records.sort(key=lambda record: record["score"], reverse=True)
    records = _filter_partner(args, records)
    _emit(args, records, ["partner", "type", "score", "tier", "borderline", "weakest", "motion"])
    return 0


def cmd_overlap(args: argparse.Namespace) -> int:
    """List shared accounts with the play each one suggests."""
    overlaps = map_overlap(load_our_accounts(args.ours), load_partner_accounts(args.theirs))
    records = [
        {
            "partner": overlap.partner,
            "account": overlap.account,
            "ours": overlap.our_status,
            "theirs": overlap.partner_status,
            "play": overlap.play,
        }
        for overlap in sorted(overlaps, key=lambda overlap: (overlap.partner, overlap.play, overlap.account))
    ]
    records = _filter_partner(args, records)
    _emit(args, records, ["partner", "account", "ours", "theirs", "play"])
    return 0


def _percent(rate: float | None) -> str:
    return "n/a" if rate is None else f"{rate:.0%}"


def cmd_attribution(args: argparse.Namespace) -> int:
    """Report sourced and influenced revenue per partner, plus win-rate lift."""
    opportunities = load_opportunities(args.opportunities)
    records = [
        {
            "partner": entry.partner,
            "sourced_won": entry.sourced_won,
            "influenced_won": entry.influenced_won,
            "open_pipeline": entry.open_pipeline,
            "win_rate": entry.win_rate,
        }
        for entry in attribute(opportunities)
    ]
    records = _filter_partner(args, records)
    lift = win_rate_lift(opportunities)
    if args.json:
        print(json.dumps({"partners": records, "win_rate": lift}, indent=2))
        return 0
    headers = ["partner", "sourced_won", "influenced_won", "open_pipeline", "win_rate"]
    rows = [
        [r["partner"], f"{r['sourced_won']:,.0f}", f"{r['influenced_won']:,.0f}", f"{r['open_pipeline']:,.0f}", _percent(r["win_rate"])]
        for r in records
    ]
    print(format_table(headers, rows))
    print(
        f"\nWin rate with a partner attached: {_percent(lift['attached'])}"
        f" | without: {_percent(lift['unattached'])}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="partner-eco", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    score = commands.add_parser("score", help="score and tier every partner")
    score.add_argument("partners", help="path to partners CSV")
    score.add_argument("--weights", help="path to a JSON file of dimension weights")
    score.set_defaults(func=cmd_score)

    overlap = commands.add_parser("overlap", help="map shared accounts and suggest a play for each")
    overlap.add_argument("ours", help="path to our accounts CSV")
    overlap.add_argument("theirs", help="path to partner accounts CSV")
    overlap.set_defaults(func=cmd_overlap)

    attribution = commands.add_parser("attribution", help="sourced vs influenced revenue per partner")
    attribution.add_argument("opportunities", help="path to opportunities CSV")
    attribution.set_defaults(func=cmd_attribution)

    for command in commands.choices.values():
        command.add_argument("--json", action="store_true", help="emit JSON instead of a table")
        command.add_argument("--partner", help="only show this partner (case-insensitive)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as error:
        print(f"partner-eco: file not found: {error.filename}", file=sys.stderr)
    except KeyError as error:
        print(f"partner-eco: input is missing the required column {error.args[0]!r}", file=sys.stderr)
    except ValueError as error:
        print(f"partner-eco: {error}", file=sys.stderr)
    return 2
