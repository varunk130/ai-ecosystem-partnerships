---
name: co-sell-account-mapping
description: 'Maps account overlap between your account list and a partner''s, then assigns a play to each shared account and builds a co-sell action list. Use when: account mapping, co-sell, partner overlap, joint pipeline, target account list with a partner, intro requests, partner pipeline review.'
---

# Co-Sell Account Mapping

Turn two account lists into a short, owned list of actions with a partner.

## When to Use
- Before a partner pipeline review or QBR
- Kicking off co-sell with a newly signed partner
- Building a joint target account list for a campaign
- Deciding where a partner intro would unblock a stalled deal

## What You'll Need
**Critical inputs (ask if not provided):**
- Your accounts: `domain,name,status` where status is `customer`, `open_opp`, or `prospect`
- Partner accounts: `partner,domain,status` where status is `customer` or `prospect`

**Nice-to-have:**
- Open opportunity amounts and stages, to rank the co-sell list
- Account owners on both sides

**Before you start:** confirm both sides have agreed to share these lists. Share the minimum fields needed.

## Process

### Step 1: Map the overlap

```bash
python -m partner_ecosystem overlap data/our_accounts.csv data/partner_accounts.csv
```

Domains are normalised first, so `https://www.Acme.com/` matches `acme.com`. Subdomains other than `www` are kept distinct.

### Step 2: Read the play for each account

| Our status | Partner status | Play | Why |
|------------|---------------|------|-----|
| open_opp | customer | co-sell | They have the relationship we need now |
| prospect | customer | intro request | Warm path into a cold account |
| customer | customer | joint expansion | Proof point and a bigger combined footprint |
| customer | prospect | referral to partner | We can give before we ask |
| open_opp | prospect | joint pursuit | Stronger together in an active evaluation |
| prospect | prospect | co-marketing | Neither side is in; build demand together |

### Step 3: Prioritise
Work co-sell first, ranked by opportunity amount and stage. Cap the list at what both teams can actually work: five to ten accounts per partner per quarter.

### Step 4: Balance the exchange
Count what you are asking for (co-sell, intro request) against what you are giving (referral to partner). A one-sided list will not get worked.

## Output Format

```markdown
## Account Mapping: [partner], [date]

**Overlap:** [n] shared accounts out of [n] ours / [n] theirs

### Co-sell now
| Account | Our stage | Amount | Ask of partner | Our owner | Their owner |
|---------|-----------|--------|----------------|-----------|-------------|

### Intro requests
### Referrals we can give
### Joint expansion and case study candidates

**Give/ask balance:** [n] asks, [n] gives
```

## Guardrails
- Do not share account data outside the agreed scope or with other partners.
- An unmatched account is not evidence of no relationship; domains differ across subsidiaries.
- Do not contact a partner's customer without the partner's account owner agreeing first.
