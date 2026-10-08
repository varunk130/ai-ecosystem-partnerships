---
name: partner-qbr-brief
description: 'Builds a one-page partner QBR brief from fit score, account overlap, and attribution, with a clear ask and a clear give. Use when: partner QBR, quarterly business review, partner review meeting, joint business plan check-in, partner exec briefing.'
---

# Partner QBR Brief

Walk into a partner review with one page: where the relationship stands, what it produced, and what each side commits to next.

## When to Use

- Preparing a quarterly business review with a partner
- Briefing an exec sponsor before a partner meeting
- Checking progress against a joint business plan

## What You'll Need

**Critical inputs (ask if not provided):**
- The partner's name
- Partner, account, and opportunity CSVs covering the review period

**Nice-to-have:**
- Last quarter's commitments from both sides
- Open escalations or integration blockers

## Process

### Step 1: Pull the three views

```bash
python -m partner_ecosystem score data/partners.csv --json
python -m partner_ecosystem overlap data/our_accounts.csv data/partner_accounts.csv --json
python -m partner_ecosystem attribution data/opportunities.csv --json
```

Filter each output to the partner under review.

### Step 2: State the position in one line

Tier, score, and the weakest dimension. If the tier changed since last quarter, say why.

### Step 3: Report what the partnership produced

Lead with sourced won revenue, then influenced, then open pipeline. Keep sourced and influenced separate; adding them overstates the result.

If the partner has fewer than five closed deals, report the counts instead of a win rate.

### Step 4: Close the loop on last quarter

List each prior commitment as done, slipped, or dropped, for both sides.

### Step 5: Make one ask and one give

Tie the ask to the weakest dimension. Tie the give to something the partner has said they need.

## Output Format

```markdown
# [Partner] QBR: [quarter]

**Position:** [tier] ([score]/100). Held back by [weakest dimension].

## Results
| Metric | This period |
|--------|-------------|
| Sourced won | |
| Influenced won | |
| Open pipeline | |
| Closed deals (won / lost) | |

## Last quarter's commitments
| Commitment | Owner | Status |
|------------|-------|--------|

## Top accounts to work together
| Account | Play | Next step | Owners |
|---------|------|-----------|--------|

## Our ask
## Our give
## Risks and blockers
```

## Guardrails

- Keep it to one page. Detail goes in an appendix.
- Do not quote the ecosystem-wide win-rate lift as this partner's result.
- Partner-attached deals win more often partly because partners join stronger deals. Present lift as a correlation.
