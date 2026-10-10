---
name: integration-launch-plan
description: 'Plans the joint launch of a partner integration: readiness checks, enablement for both field teams, launch customers, messaging, and a 90-day adoption review. Use when: integration launch, partner launch, joint go-to-market, co-launch, announcing an integration, partner GTM plan, marketplace listing launch.'
---

# Integration Launch Plan

Launch a partner integration so that customers find it, field teams can explain it, and someone checks whether it is used.

## When to Use

- An integration is within a quarter of general availability
- Moving an integration from listed to certified
- Publishing a marketplace or directory listing
- Relaunching an integration with low adoption

## What You'll Need

**Critical inputs (ask if not provided):**

- What the integration does, in the customer's words
- Target launch date and who owns it on each side
- Customers already using it, including beta users

**Nice-to-have:**

- The one-page scope from `product-partnership-evaluator`
- Shared accounts from `partner-eco overlap`
- Each side's launch calendar, to avoid collisions

## Process

### Step 1: Check readiness

Do not set a date until each line has an owner.

| Area | Ready when |
|------|-----------|
| Product | Tested by both sides, failure behavior defined |
| Documentation | Setup guide published on both sites |
| Support | First-line owner and escalation path agreed |
| Legal | Announcement, logo use, and customer quotes approved |
| Customers | Three named joint customers live |

### Step 2: Write the message once

One sentence on the customer job, three proof points, one call to action. Both companies use the same sentence.

### Step 3: Enable both field teams

Sellers and customer success on both sides need a two-sentence pitch, the ideal customer for it, a demo they can run, and who to call. Enablement happens before the announcement, not after.

### Step 4: Pick the launch accounts

```bash
python -m partner_ecosystem overlap data/our_accounts.csv data/partner_accounts.csv --partner "Northwind Data"
```

Start with joint expansion accounts, where both sides already have the customer. They adopt fastest and become references.

### Step 5: Sequence the launch

| When | Activity |
|------|----------|
| Four weeks before | Field enablement, launch customers confirmed |
| Two weeks before | Documentation live, support briefed |
| Launch day | Announcement from both companies, in-product notice |
| Weeks 1 to 4 | Outreach to launch accounts, first customer story |
| Day 90 | Adoption review and the deepen, hold, or retire decision |

### Step 6: Define the adoption review

Name one success metric, its target, its owner, and the review date before launch day.

## Output Format

```markdown
# Integration Launch Plan: [integration], [date]

**Message:** [one sentence]

## Readiness
| Area | Owner | Status |
|------|-------|--------|

## Enablement
| Audience | Asset | Owner | Date |
|----------|-------|-------|------|

## Launch accounts
| Account | Our owner | Their owner | Next step |
|---------|-----------|-------------|-----------|

## Timeline
## Success metric
- Metric:
- Target:
- Review date:
```

## Guardrails

- Do not announce before three joint customers are live.
- Never use a customer name or quote without written approval from that customer.
- Launch date is not the success metric. Usage is.
- If adoption is low at 90 days, recommend hold or retire rather than another announcement.

## Related

- [Product partnerships playbook](https://github.com/varunk130/ai-ecosystem-partnerships/blob/main/playbooks/product-partnerships.md): integration depth and the 90-day review
- [Co-sell playbook](https://github.com/varunk130/ai-ecosystem-partnerships/blob/main/playbooks/co-sell.md): working the launch accounts with the partner's field team
