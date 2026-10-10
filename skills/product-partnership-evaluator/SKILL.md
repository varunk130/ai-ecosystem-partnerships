---
name: product-partnership-evaluator
description: 'Evaluates a proposed product partnership: build, buy, or partner, the right integration depth, a one-page scope, and the commercial model. Use when: product partnership, integration partnership, build vs buy vs partner, technology alliance, should we integrate with, OEM or embedded partnership, ISV integration request.'
---

# Product Partnership Evaluator

Decide whether a product partnership is worth doing, and how deep to go, before anyone signs or builds.

## When to Use

- A partner or customer asks for an integration
- Choosing between building a capability, acquiring it, or partnering for it
- Deciding whether to move an existing integration to a deeper level
- Preparing a recommendation for product and partnership leadership

## What You'll Need

**Critical inputs (ask if not provided):**

- The customer problem the partnership would solve
- The proposed partner and what their product does
- How many customers you share today, or an estimate

**Nice-to-have:**

- Customer requests or lost-deal notes that mention the partner
- The partner's row in `data/partners.csv`
- Roadmap capacity for the next two quarters

## Process

### Step 1: State the customer job

Write one sentence: who the customer is, what they are trying to finish, and what is slow or broken today. If you cannot, stop and gather evidence first.

### Step 2: Build, buy, or partner

Score each option against the same five questions.

| Question | Build | Buy | Partner |
|----------|-------|-----|---------|
| Core to why customers choose us? | | | |
| Expertise and roadmap room? | | | |
| Customer already has a preferred tool? | | | |
| Time to deliver? | | | |
| What we give up? | | | |

Recommend partnering when the capability is adjacent, the customer already has a vendor, and speed matters more than control.

### Step 3: Choose the integration depth

| Depth | Go here when |
|-------|--------------|
| 1. Listed | Shared customers are asking, usage is unproven |
| 2. Certified | Joint customers adopt the listed integration without help |
| 3. Embedded | Joint users show measurable lift in activation or retention |

Recommend one level above where the integration is today, never two.

### Step 4: Write the one-page scope

Cover the customer job, data flow, identity and permissions, failure behavior, support model, and one success metric with a target and review date.

### Step 5: Recommend the commercial model

Pick one of: no money changes hands, referral fee, revenue share or resale, OEM or embedded license. State what you are trading for it and the exit terms.

### Step 6: Name the risks

List dependency, channel conflict with existing partners, competitive overlap, and support load. Give each a mitigation or accept it explicitly.

## Output Format

```markdown
# Product Partnership Evaluation: [partner]

**Recommendation:** [build / buy / partner / do nothing], at depth [1-3]

## Customer job
## Build, buy, or partner
| Question | Build | Buy | Partner |
|----------|-------|-----|---------|

## Scope
| Element | Decision |
|---------|----------|

## Commercial model
## Evidence
- Shared customers: [n]
- Requests or lost deals citing this: [n]

## Risks and mitigations
## Decision needed and by when
```

## Guardrails

- Evidence of demand comes before brand appeal. A famous partner with no shared customers is not a priority.
- Do not recommend embedded depth without usage data from a shallower integration.
- Say "do nothing" when that is the answer.
- Flag any conflict with an existing partner; do not leave it for them to discover.
