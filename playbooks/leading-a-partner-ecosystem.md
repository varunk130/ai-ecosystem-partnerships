# Leading a Partner Ecosystem

One partnership is a relationship. An ecosystem is a system: it needs rules that still work when you are not in the room.

## 1. Decide what the ecosystem is for

Pick the primary job. It sets every later trade-off.

| Primary job | You optimize for | Leading metric |
|-------------|------------------|----------------|
| Reach | New segments and regions through partners | Partner-sourced pipeline |
| Product completeness | Integrations customers expect | Share of customers using one or more integrations |
| Delivery capacity | Partners who implement and support | Certified people, time to value |
| Credibility | Association with trusted platforms | Win rate on partner-attached deals |

Most ecosystems serve two of these. Naming a primary one tells the team what to do when they conflict.

## 2. Segment and tier

Tier on evidence, review on a schedule, and publish the criteria.

```bash
python -m partner_ecosystem score data/partners.csv
```

| Tier | What the partner gets | What you expect back |
|------|----------------------|----------------------|
| Strategic | Joint business plan, exec sponsor, named partner manager, roadmap input | Shared targets, exec access, certified team |
| Growth | Account mapping, co-marketing, quarterly review | Sourced pipeline, a referenceable joint win |
| Emerging | Enablement, sandbox, deal registration | First joint customers |
| Watchlist | Self-serve program and documentation | Nothing yet |

A tier is a two-way commitment. If a partner gets Strategic benefits without Strategic obligations, the tier means nothing to everyone else.

See [the scoring methodology](../docs/scoring-methodology.md) for weights and thresholds.

## 3. Set the operating cadence

| Cadence | Meeting | Output |
|---------|---------|--------|
| Weekly | Co-sell pipeline review per Strategic partner | Next step and owner on every shared deal |
| Monthly | Portfolio stand-up | Blockers, tier changes proposed |
| Quarterly | QBR per Strategic and Growth partner | One-page brief, one ask, one give |
| Twice a year | Portfolio review | Promote, hold, or exit each partner |
| Yearly | Joint business plan with Strategic partners | Targets, investments, executive sign-off |

## 4. Measure what partners change

Report sourced and influenced separately, and always against a baseline.

```bash
python -m partner_ecosystem attribution data/opportunities.csv
```

| Layer | Metric | Why |
|-------|--------|-----|
| Outcome | Sourced won revenue, influenced won revenue | What the ecosystem produced |
| Efficiency | Win rate with a partner attached against without | Whether partners improve deals |
| Health | Active partners, certified people, integration adoption | Whether next year's outcome is being built |
| Balance | Asks against gives per partner | Whether the relationship is sustainable |

Win-rate lift is a correlation. Partners tend to join deals that are already healthy, so present it with that caveat.

## 5. Make ownership explicit

| Decision | Owner | Consulted |
|----------|-------|-----------|
| Tier assignment | Head of partnerships | Sales, product |
| Integration depth | Product | Partnerships, engineering |
| Deal conflict between partners | Partnerships, by published rule | Sales leadership |
| Partner exit | Head of partnerships | Legal, customer success |

Channel conflict is handled by rules written before the conflict, not by whoever escalates loudest.

## 6. Prune

A portfolio that only grows gets worse. Each portfolio review should exit or downgrade someone, and say why. The time returns to partners who can use it.

## The first 90 days in a new ecosystem role

1. **Days 1 to 30:** score the existing portfolio, meet the top ten partners, find the three deals in flight
2. **Days 31 to 60:** publish tier criteria, run account mapping with the top three, agree the metrics with sales and finance
3. **Days 61 to 90:** sign one joint business plan, exit or downgrade the bottom of the list, run the first QBR in the new format
