# Scoring Methodology

The fit score answers one question: given limited partner-team time, where does the next hour do the most good?

## Dimensions

Each dimension is normalized to 0-1, multiplied by its weight, and summed to a 0-100 score.

| Dimension | Weight | Normalization | Why it matters |
|-----------|--------|---------------|----------------|
| ICP fit | 30% | `icp_overlap` as given | Without shared buyers, nothing else converts |
| Pipeline | 25% | `(sourced + 0.5 × influenced) / 2,000,000`, capped at 1 | The outcome the relationship exists for |
| Integration | 20% | `integration_depth / 3` | A product reason to sell together |
| Traction | 15% | `joint_customers / 25`, capped at 1 | Proof it already works |
| Commitment | 10% | `0.6 × exec_sponsor + 0.4 × certified_people / 20` (capped) | Whether they will show up |

## Design choices

**Caps.** Pipeline, joint customers, and certified people are capped so one very large number cannot carry a partner with poor fit. A hyperscaler with enormous influenced pipeline still needs ICP overlap to rank first.

**Influenced counts half.** Influenced pipeline is real, but the bar for claiming it is lower than for sourced. Discounting it keeps the score from rewarding attribution hygiene over origination.

**Fit outweighs pipeline.** Pipeline is a lagging signal and new partners have none. Weighting fit highest lets a well-matched new partner reach Emerging or Growth before revenue arrives.

**Weakest dimension.** Every score reports the lowest-scoring dimension, unweighted. It is the most useful single line for the partner conversation.

## Tiers

| Tier | Score | Motion |
|------|-------|--------|
| Strategic | 75+ | Joint business plan, exec cadence, dedicated co-sell |
| Growth | 55-74.9 | Targeted account mapping and co-marketing |
| Emerging | 35-54.9 | Enablement and first joint wins |
| Watchlist | below 35 | Self-serve program, review quarterly |

A score within three points of a threshold is marked borderline in `score` output. Treat the tier as provisional and say what would tip it.

## Worked example

A partner with `icp_overlap` 0.5, integration depth 1, 5 joint customers, 100,000 sourced, 200,000 influenced, no exec sponsor, and 4 certified people:

| Dimension | Value | Weighted |
|-----------|-------|----------|
| ICP fit | 0.500 | 0.1500 |
| Pipeline | (100,000 + 100,000) / 2,000,000 = 0.100 | 0.0250 |
| Integration | 1 / 3 = 0.333 | 0.0667 |
| Traction | 5 / 25 = 0.200 | 0.0300 |
| Commitment | 0.4 × 4 / 20 = 0.080 | 0.0080 |
| **Total** | | **0.2797, score 28.0, Watchlist** |

This case is pinned in `tests/test_scoring.py`.

## Estimating ICP overlap

ICP fit carries the most weight, so write down how each `icp_overlap` value was reached. Three workable methods:

| Method | How | Bias to expect |
|--------|-----|----------------|
| Shared-customer sample | Take 30 to 50 of the partner's customers and count how many match your ICP | Small samples swing widely; the partner may pick flattering accounts |
| Public customer list | Match the logos and case studies on the partner's site against your ICP firmographics | Skews to large, referenceable brands and overstates enterprise fit |
| Partner self-report | Ask the partner for their customer mix by segment | Optimistic, and their segment definitions rarely match yours |

Use the same method for every partner in a review. A consistent bias still ranks partners correctly; mixed methods do not.

## Limits

- The caps and weights are opinionated defaults, not benchmarks. Tune them to your deal sizes and pass custom weights with `--weights` or to `score_partner`.
- `icp_overlap` is an estimate. Record how it was derived.
- Win-rate lift in the attribution view is a correlation. Partners tend to engage on deals that are already healthier.
