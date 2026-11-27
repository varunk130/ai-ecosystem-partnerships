"""Build a one-page executive report on the whole partner ecosystem.

The report runs every analysis in the package (score and tier, account
overlap, attribution) and turns the results into a ranked action list with
charts. The output is a single self-contained HTML file with no external
assets, so it can be emailed, attached, or opened offline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path

from .attribution import Opportunity, PartnerAttribution, attribute, open_amount_by_domain, win_rate_lift
from .models import Partner
from .overlap import Overlap, give_ask_balance, rank_overlaps, PLAY_PRIORITY
from .scoring import WEIGHTS, score_partner
from .tiering import BORDERLINE_MARGIN, TIERS, assign_tier, is_borderline

# What to do about the dimension that holds a partner back most.
FIXES = {
    "icp_fit": "focus joint targeting on accounts inside our ICP",
    "pipeline": "agree a joint pipeline target and review it monthly",
    "integration": "build or certify the integration",
    "traction": "land and reference the first joint customers",
    "commitment": "secure an exec sponsor and certify their team",
}
DIMENSION_LABELS = {
    "icp_fit": "ICP fit",
    "pipeline": "Pipeline",
    "integration": "Integration",
    "traction": "Traction",
    "commitment": "Commitment",
}
LIVE_PLAYS = ("co-sell", "joint pursuit")


@dataclass(frozen=True)
class ScoredPartner:
    name: str
    partner_type: str
    score: float
    tier: str
    borderline: bool
    weakest: str


@dataclass(frozen=True)
class Ecosystem:
    """Every analysis result the report needs, computed once."""

    partners: list[ScoredPartner]
    plays: list[Overlap]
    open_amounts: dict[str, float]
    attribution: list[PartnerAttribution]
    win_rates: dict[str, float | None]
    balance: dict[str, dict[str, int]]
    opportunity_count: int
    weights: dict[str, float]


def analyze(
    partners: list[Partner],
    overlaps: list[Overlap],
    opportunities: list[Opportunity],
    weights: dict[str, float] | None = None,
) -> Ecosystem:
    """Run scoring, tiering, overlap ranking, and attribution together."""
    scored = []
    for partner in partners:
        score = score_partner(partner, weights)
        scored.append(
            ScoredPartner(
                name=partner.name,
                partner_type=partner.partner_type,
                score=score.total,
                tier=assign_tier(score.total).name,
                borderline=is_borderline(score.total),
                weakest=score.weakest,
            )
        )
    scored.sort(key=lambda p: p.score, reverse=True)
    amounts = open_amount_by_domain(opportunities)
    plays = sorted(
        rank_overlaps(overlaps, amounts),
        key=lambda o: (PLAY_PRIORITY.index(o.play), -amounts.get(o.domain, 0.0), o.partner, o.account),
    )
    return Ecosystem(
        partners=scored,
        plays=plays,
        open_amounts=amounts,
        attribution=attribute(opportunities),
        win_rates=win_rate_lift(opportunities),
        balance=give_ask_balance(overlaps),
        opportunity_count=len(opportunities),
        weights=weights or WEIGHTS,
    )


def money(value: float) -> str:
    """Format dollars as $1.2M, $410K, or $900."""
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M".replace(".0M", "M")
    if abs(value) >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:.0f}"


def _pct(rate: float | None) -> str:
    return "n/a" if rate is None else f"{rate:.0%}"


def _names(names: list[str]) -> str:
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]


def recommendations(eco: Ecosystem) -> list[tuple[str, str]]:
    """Return (headline, detail) actions, most urgent first."""
    actions = []
    live = [o for o in eco.plays if o.play in LIVE_PLAYS]
    if live:
        total = sum(eco.open_amounts.get(o.domain, 0.0) for o in {o.domain: o for o in live}.values())
        top = live[0]
        actions.append(
            (
                f"Run {len(live)} partner plays on {money(total)} of open deals",
                f"Start with {top.partner} on {top.account} ({money(eco.open_amounts.get(top.domain, 0.0))}, {top.play}).",
            )
        )
    owing = sorted(p for p, c in eco.balance.items() if c["asks"] >= c["gives"] + 2)
    if owing:
        actions.append(
            (
                f"Give before the next ask to {_names(owing)}",
                "We ask these partners for help on more accounts than we send them. Refer them a deal before the next co-sell request.",
            )
        )
    strategic = [p for p in eco.partners if p.tier == TIERS[0].name]
    if strategic:
        by_fix: dict[str, list[str]] = {}
        for p in strategic:
            by_fix.setdefault(FIXES[p.weakest], []).append(p.name)
        fixes = "; ".join(f"{_names(names)}: {fix}" for fix, names in by_fix.items())
        actions.append((f"Invest in the {len(strategic)} Strategic partners where they are weakest", fixes + "."))
    borderline = [p.name for p in eco.partners if p.borderline]
    if borderline:
        actions.append(
            (
                f"Review {len(borderline)} borderline partners before changing tiers",
                f"{_names(borderline)} sit within {BORDERLINE_MARGIN:g} points of a tier line, so small data changes could move them.",
            )
        )
    watch = [p.name for p in eco.partners if p.tier == TIERS[-1].name]
    if watch:
        actions.append(
            (
                f"Move {len(watch)} Watchlist partners to the self-serve program",
                f"{_names(watch)}: keep them listed, stop dedicated time, and review next quarter.",
            )
        )
    return actions


# Chart geometry. Charts are SVG drawn on a fixed viewBox and scaled to width.
_W = 760
_LABEL = 190
_RIGHT = 60


def _portfolio_chart(eco: Ecosystem) -> str:
    row, gap = 26, 8
    top = 26
    plot = _W - _LABEL - _RIGHT
    height = top + len(eco.partners) * (row + gap)
    x = lambda score: _LABEL + plot * score / 100  # noqa: E731
    parts = [f'<svg viewBox="0 0 {_W} {height}" role="img" aria-label="Partner fit scores by tier">']
    for tier in TIERS[:-1]:
        parts.append(
            f'<line class="threshold" x1="{x(tier.min_score):.1f}" x2="{x(tier.min_score):.1f}" y1="{top - 6}" y2="{height}"/>'
            f'<text class="axis-label" x="{x(tier.min_score):.1f}" y="{top - 12}" text-anchor="middle">{tier.min_score:g}</text>'
        )
    for i, p in enumerate(eco.partners):
        y = top + i * (row + gap)
        tier_index = [t.name for t in TIERS].index(p.tier)
        flag = " · borderline" if p.borderline else ""
        parts.append(
            f'<g><title>{escape(p.name)}: {p.score:g} ({p.tier}{flag}); weakest: {DIMENSION_LABELS[p.weakest]}</title>'
            f'<text class="row-label" x="{_LABEL - 12}" y="{y + row / 2 + 4}" text-anchor="end">{escape(p.name)}</text>'
            f'<rect class="tier-{tier_index}" x="{_LABEL}" y="{y}" width="{max(x(p.score) - _LABEL, 2):.1f}" height="{row}" rx="4"/>'
            f'<text class="value" x="{x(p.score) + 8:.1f}" y="{y + row / 2 + 4}">{p.score:g}{" ◆" if p.borderline else ""}</text></g>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _attribution_chart(eco: Ecosystem) -> str:
    rows = eco.attribution
    if not rows:
        return '<p class="muted">No partner-attached opportunities in the input.</p>'
    width, label, row, gap, top = 480, 150, 26, 10, 4
    plot = width - label - 70
    peak = max(r.sourced_won + r.influenced_won for r in rows) or 1
    height = top + len(rows) * (row + gap)
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Won revenue by partner, sourced and influenced">']
    for i, r in enumerate(rows):
        y = top + i * (row + gap)
        sw = plot * r.sourced_won / peak
        iw = plot * r.influenced_won / peak
        total = r.sourced_won + r.influenced_won
        parts.append(
            f'<g><title>{escape(r.partner)}: {money(r.sourced_won)} sourced, {money(r.influenced_won)} influenced</title>'
            f'<text class="row-label" x="{label - 12}" y="{y + row / 2 + 4}" text-anchor="end">{escape(r.partner)}</text>'
        )
        if sw:
            parts.append(f'<rect class="sourced" x="{label}" y="{y}" width="{sw:.1f}" height="{row}" rx="4"/>')
        if iw:
            gap_px = 2 if sw else 0
            parts.append(f'<rect class="influenced" x="{label + sw + gap_px:.1f}" y="{y}" width="{max(iw - gap_px, 2):.1f}" height="{row}" rx="4"/>')
        parts.append(f'<text class="value" x="{label + sw + iw + 8:.1f}" y="{y + row / 2 + 4}">{money(total)}</text></g>')
    parts.append("</svg>")
    return "".join(parts)


def _win_rate_chart(eco: Ecosystem) -> str:
    attached, unattached = eco.win_rates["attached"], eco.win_rates["unattached"]
    if attached is None or unattached is None:
        return '<p class="muted">Not enough closed deals to compare win rates.</p>'
    row, gap, label, plot = 26, 10, 110, 170
    parts = ['<svg viewBox="0 0 330 72" role="img" aria-label="Win rate with and without a partner">']
    for i, (name, rate, cls) in enumerate((("With a partner", attached, "sourced"), ("Without", unattached, "neutral"))):
        y = i * (row + gap)
        parts.append(
            f'<text class="row-label" x="{label - 12}" y="{y + row / 2 + 4}" text-anchor="end">{name}</text>'
            f'<rect class="{cls}" x="{label}" y="{y}" width="{max(plot * rate, 2):.1f}" height="{row}" rx="4"/>'
            f'<text class="value" x="{label + plot * rate + 8:.1f}" y="{y + row / 2 + 4}">{rate:.0%}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _tier_legend() -> str:
    items = "".join(
        f'<span><i class="sw tier-{i}"></i>{t.name} {"≥ " + format(t.min_score, "g") if t.min_score else "&lt; " + format(TIERS[i - 1].min_score, "g")}</span>'
        for i, t in enumerate(TIERS)
    )
    return f'<div class="legend">{items}<span>◆ borderline (within {BORDERLINE_MARGIN:g} points of a line)</span></div>'


def _plays_table(eco: Ecosystem, limit: int = 8) -> str:
    if not eco.plays:
        return '<p class="muted">No shared accounts found.</p>'
    rows = "".join(
        "<tr>"
        f"<td>{escape(o.account)}</td>"
        f"<td>{escape(o.partner)}</td>"
        f'<td><span class="pill{" live" if o.play in LIVE_PLAYS else ""}">{escape(o.play)}</span></td>'
        f'<td class="muted">{o.our_status.replace("_", " ")} / {o.partner_status}</td>'
        f'<td class="num">{money(eco.open_amounts[o.domain]) if eco.open_amounts.get(o.domain) else "—"}</td>'
        "</tr>"
        for o in eco.plays[:limit]
    )
    more = len(eco.plays) - limit
    foot = f'<p class="muted small">Plus {more} more in <code>partner-eco overlap</code>.</p>' if more > 0 else ""
    return (
        '<table><thead><tr><th>Account</th><th>Partner</th><th>Play</th><th>Us / them</th>'
        f'<th class="num">Open deal</th></tr></thead><tbody>{rows}</tbody></table>{foot}'
    )


CSS = """
:root{--bg:#f6f6f4;--card:#fff;--ink:#1c1c1a;--ink2:#55554f;--muted:#7a7a73;--line:#e6e5e0;
--accent:#3b2fb5;--accent-soft:#eeedfc;--t0:#3b2fb5;--t1:#6a5fe0;--t2:#a29bf0;--t3:#d6d3f7;
--sourced:#2a78d6;--influenced:#eb6834;--neutral:#b9b8b0;--live:#e7f0fc;--live-ink:#1d5bb0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121211;--card:#1c1c1b;--ink:#eeeeea;
--ink2:#c3c3bc;--muted:#96968e;--line:#2f2f2c;--accent:#b9b2fa;--accent-soft:#25233d;--t0:#b9b2fa;--t1:#8a7ef0;
--t2:#5b4bd0;--t3:#3a3270;--sourced:#3d8ff0;--influenced:#d9692f;--neutral:#5c5c56;--live:#1b2a40;--live-ink:#9cc4f5}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
.page{max-width:920px;margin:0 auto;padding:40px 20px 56px}
.kicker{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
h1{font-size:28px;line-height:1.25;margin:8px 0 10px;letter-spacing:-.01em}
h2{font-size:18px;margin:0 0 4px}
.sub{color:var(--ink2);margin:0}
.muted{color:var(--muted)}.small{font-size:13px}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:24px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.kpi .v{font-size:26px;font-weight:700;letter-spacing:-.02em}
.kpi .k{font-size:13px;color:var(--ink2)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 24px;margin-top:16px}
.card > p.sub{margin-bottom:16px}
ol.actions{margin:14px 0 0;padding:0;list-style:none;counter-reset:a}
ol.actions li{counter-increment:a;display:grid;grid-template-columns:30px 1fr;gap:10px;padding:12px 0;border-top:1px solid var(--line)}
ol.actions li:first-child{border-top:0}
ol.actions li::before{content:counter(a);width:26px;height:26px;border-radius:8px;background:var(--accent-soft);color:var(--accent);
font-weight:700;display:grid;place-items:center;font-size:13px}
ol.actions strong{display:block}
ol.actions span{color:var(--ink2);font-size:14px}
svg{width:100%;height:auto;display:block;overflow:visible}
svg text{font:13px -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
.row-label{fill:var(--ink)}.value{fill:var(--ink2);font-weight:600}.axis-label{fill:var(--muted);font-size:11px}
.threshold{stroke:var(--line);stroke-width:1.5;stroke-dasharray:3 4}
.tier-0{fill:var(--t0);background:var(--t0)}.tier-1{fill:var(--t1);background:var(--t1)}
.tier-2{fill:var(--t2);background:var(--t2)}.tier-3{fill:var(--t3);background:var(--t3)}
.sourced{fill:var(--sourced);background:var(--sourced)}.influenced{fill:var(--influenced);background:var(--influenced)}
.neutral{fill:var(--neutral);background:var(--neutral)}
g:hover rect{opacity:.85}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:12.5px;color:var(--ink2);margin-top:14px}
.legend span{display:inline-flex;align-items:center;gap:6px}
.sw{width:12px;height:12px;border-radius:3px;display:inline-block}
.grid2{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:28px;align-items:start}
h3{font-size:13px;margin:0 0 10px;color:var(--ink2);font-weight:600}
table{width:100%;border-collapse:collapse;font-size:14px}
th{text-align:left;font-size:12px;font-weight:600;color:var(--muted);border-bottom:1px solid var(--line);padding:6px 8px}
td{border-bottom:1px solid var(--line);padding:9px 8px}
tr:last-child td{border-bottom:0}
.num{text-align:right;font-variant-numeric:tabular-nums}
.pill{display:inline-block;font-size:12px;padding:2px 9px;border-radius:999px;background:var(--bg);color:var(--ink2);white-space:nowrap}
.pill.live{background:var(--live);color:var(--live-ink);font-weight:600}
.table-wrap{overflow-x:auto}
footer{margin-top:22px;font-size:12.5px;color:var(--muted)}
code{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace}
@media (max-width:720px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.grid2{grid-template-columns:minmax(0,1fr)}
h1{font-size:23px}.kpi .v{font-size:22px}.card{padding:18px 16px}}
@media print{body{background:#fff}.card,.kpi{break-inside:avoid}}
"""


def render_html(eco: Ecosystem, title: str = "Partner ecosystem review", as_of: date | None = None) -> str:
    """Render the full report as one HTML document."""
    as_of = as_of or date.today()
    sourced = sum(r.sourced_won for r in eco.attribution)
    influenced = sum(r.influenced_won for r in eco.attribution)
    open_pipeline = sum(r.open_pipeline for r in eco.attribution)
    rates = eco.win_rates
    lift = rates["lift"]
    strategic = sum(p.tier == TIERS[0].name for p in eco.partners)
    live = [o for o in eco.plays if o.play in LIVE_PLAYS]

    headline = f"Partners helped win {money(sourced + influenced)}"
    if lift is not None:
        headline += f" and lift win rate by {round(lift * 100)} points"
    headline += "."
    if live:
        headline += f" {len(live)} plays on shared accounts can move open deals now."

    kpis = [
        (money(sourced + influenced), f"won with partners ({money(sourced)} sourced, {money(influenced)} influenced)"),
        (money(open_pipeline), "open pipeline with a partner attached"),
        (
            f"{_pct(rates['attached'])} vs. {_pct(rates['unattached'])}",
            "win rate with a partner vs. without",
        ),
        (f"{strategic} of {len(eco.partners)}", "partners earn Strategic investment"),
    ]
    kpi_html = "".join(f'<div class="kpi"><div class="v">{v}</div><div class="k">{escape(k)}</div></div>' for v, k in kpis)
    actions = "".join(f"<li><div><strong>{escape(h)}</strong><span>{escape(d)}</span></div></li>" for h, d in recommendations(eco))
    weights = ", ".join(f"{DIMENSION_LABELS[k]} {v:.0%}" for k, v in eco.weights.items())
    tier_lines = ", ".join(f"{t.name} {t.min_score:g}" for t in TIERS[:-1])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<main class="page">
  <div class="kicker">{escape(title)} · {as_of:%B} {as_of.day}, {as_of.year}</div>
  <h1>{escape(headline)}</h1>
  <p class="sub">{len(eco.partners)} partners scored, {len(eco.plays)} shared accounts mapped, {eco.opportunity_count} opportunities attributed.</p>

  <section class="kpis">{kpi_html}</section>

  <section class="card">
    <h2>What to do this quarter</h2>
    <p class="sub">Ranked by urgency: live deals first, then relationships, then portfolio moves.</p>
    <ol class="actions">{actions}</ol>
  </section>

  <section class="card">
    <h2>Portfolio: who earns investment</h2>
    <p class="sub">Fit score from 0 to 100. The tier sets the motion each partner gets.</p>
    {_portfolio_chart(eco)}
    {_tier_legend()}
  </section>

  <section class="card">
    <h2>Co-sell plays on shared accounts</h2>
    <p class="sub">Accounts both companies touch, with the play each one calls for. Highlighted plays are on open deals.</p>
    <div class="table-wrap">{_plays_table(eco)}</div>
  </section>

  <section class="card">
    <h2>What partners delivered</h2>
    <p class="sub">Won revenue by partner, and how often deals close with a partner attached.</p>
    <div class="grid2">
      <div>
        <h3>Won revenue</h3>
        {_attribution_chart(eco)}
        <div class="legend"><span><i class="sw sourced"></i>Sourced</span><span><i class="sw influenced"></i>Influenced</span></div>
      </div>
      <div>
        <h3>Win rate on closed deals</h3>
        {_win_rate_chart(eco)}
      </div>
    </div>
  </section>

  <footer>
    Method: fit score weights are {weights}; influenced pipeline counts at half. Tiers start at
    {tier_lines}. Generated by <code>partner-eco report</code>.
  </footer>
</main>
</body>
</html>
"""


def write_report(eco: Ecosystem, path: str | Path, **kwargs: object) -> Path:
    """Write the report and return its path."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_html(eco, **kwargs), encoding="utf-8")  # type: ignore[arg-type]
    return out
