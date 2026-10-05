---
name: partner-fit-scorecard
description: 'Scores and tiers a partner portfolio on ICP fit, pipeline, integration depth, traction, and commitment, then recommends a motion per tier. Use when: partner scoring, partner tiering, partner prioritisation, portfolio review, which partners to invest in, partner programme design.'
---

# Partner Fit Scorecard

Rank a partner portfolio on evidence so investment follows fit, not the loudest relationship.

## When to Use
- Annual or quarterly partner portfolio review
- Deciding which partners get a joint business plan
- Designing or resetting programme tiers
- Onboarding a new partner and setting expectations

## What You'll Need
**Critical inputs (ask if not provided):**
- A partner list with the columns in `data/partners.csv`
- The period the pipeline numbers cover (default: trailing 12 months)

**Nice-to-have:**
- Your ICP definition, to sanity-check `icp_overlap`
- Any weights the team has already agreed

## Process

### Step 1: Validate the data
Run the loader before scoring. It rejects out-of-range values, so fix the source rather than the score.

```bash
python -m partner_ecosystem score data/partners.csv
```

### Step 2: Read the score with its weakest dimension
The `weakest` column names the dimension holding each partner back. That is the conversation to have with them.

| Weakest dimension | What it usually means | First move |
|-------------------|----------------------|------------|
| `icp_fit` | They sell to a different buyer | Narrow to the segment that overlaps |
| `pipeline` | Relationship without revenue | Run account mapping, agree three target accounts |
| `integration` | No product reason to co-sell | Scope a certified integration |
| `traction` | Few joint customers | Find one referenceable joint win |
| `commitment` | No sponsor, no trained people | Ask for an exec sponsor and an enablement cohort |

### Step 3: Assign the motion
Use the tier to set what the partner gets, and say so explicitly. A Growth partner asking for Strategic treatment should hear which dimension to move.

### Step 4: Challenge the result
Before sharing, check for:
- A partner within three points of a tier boundary: note it as borderline
- A high score carried by influenced pipeline alone
- A new partner penalised for traction they have not had time to build

## Output Format

```markdown
## Partner Portfolio Review: [period]

| Partner | Score | Tier | Weakest | Next step | Owner |
|---------|-------|------|---------|-----------|-------|

### Moves this quarter
- Promote: [partner], because [dimension] moved from [x] to [y]
- Invest: [partner], to fix [weakest dimension]
- Deprioritise: [partner], because [reason]

### Borderline calls
- [partner]: [score], [what would tip it]
```

## Guardrails
- Do not change weights to make a favoured partner rank higher. Change them only with a stated reason and re-score everyone.
- A score is a starting point for a decision, not the decision.
- Never present synthetic sample data as real partner performance.
