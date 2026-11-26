---
name: ecosystem-review
description: 'Runs a full partner ecosystem review end to end: research new partners, score and tier the portfolio, map shared accounts, attribute pipeline, and produce a one-page executive report with a ranked action list. Use when: partner ecosystem review, quarterly partner review, partner portfolio review, state of the ecosystem, partner program health, exec partner report.'
---

# Ecosystem Review

One run, one page: which partners earn investment, which shared accounts to work now, what partners delivered, and what to do this quarter.

## When to Use

- Quarterly or half-year partner program review
- Preparing a leadership update on partnerships
- After adding several new partners, to see where they land
- Before setting partner budgets or headcount

## What You'll Need

**Critical inputs (ask if not provided):**

- A folder with the four CSVs: `partners.csv`, `our_accounts.csv`, `partner_accounts.csv`, `opportunities.csv` (formats in `docs/HOW-TO-USE.md`). The sample folder `data/` works for a dry run.

**Nice-to-have:**

- Names or URLs of new partners to add before the review
- Custom scoring weights as JSON, if leadership weighs pipeline above ICP fit
- Last quarter's report, to call out what changed

## Process

### 1. Research new partners (optional)

For each new partner, run the `partner-research` skill and append its draft row to `partners.csv`. Mark rows with unknown fields so the review treats their scores as floors.

### 2. Run the analyses

```bash
python -m partner_ecosystem score DATA/partners.csv
python -m partner_ecosystem overlap DATA/our_accounts.csv DATA/partner_accounts.csv --opportunities DATA/opportunities.csv
python -m partner_ecosystem attribution DATA/opportunities.csv
```

Read the output before writing anything. Check for partners near a tier line (`borderline`), give/ask imbalance under the overlap table, and win rates built on very few closed deals.

### 3. Build the report

```bash
python -m partner_ecosystem report DATA --out report.html
```

The report ranks actions in this order: plays on open deals, give/ask balance, investment in Strategic partners by their weakest dimension, borderline partners to review, and Watchlist partners to move to self-serve.

### 4. Add judgment

The report is the evidence; the review needs a point of view. Write three to five sentences for leadership that:

- Name the one decision you need from them (budget, headcount, an exec sponsor)
- Say what changed since last quarter, if you have it
- Flag where the data is thin (few closed deals, unknown fields from research)

### 5. Hand off

- Strategic partners: `joint-business-plan` or `partner-qbr-brief`
- Top shared accounts: `co-sell-account-mapping` for owners and dates
- New integrations: `integration-launch-plan`

## Output

1. `report.html`: the one-page executive report
2. A short leadership note with the decision you need
3. The hand-off list: which skill to run next, for which partner

## Quality Checks

- [ ] Every number in the note matches the report
- [ ] Win rates with fewer than five closed deals are labeled as directional
- [ ] Borderline partners are reviewed before anyone changes their tier
- [ ] The leadership note asks for one clear decision
