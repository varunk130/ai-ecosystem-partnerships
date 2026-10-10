# Product Partnerships

A product partnership exists when a customer gets more from two products used together than from either alone. Everything else, including co-marketing and co-sell, depends on that being true.

## 1. Build, buy, or partner

Start from the customer problem, not the partner.

| Question | Build | Buy | Partner |
|----------|-------|-----|---------|
| Is it core to why customers choose us? | Yes | Sometimes | No |
| Do we have the expertise and the roadmap room? | Yes | No | No |
| Does the customer already own a tool for it? | Rarely | Rarely | Usually |
| How fast do we need it? | Quarters | Months, plus integration | Weeks to a quarter |
| What do we give up? | Roadmap capacity | Capital and focus | Control of the experience |

Partner when the capability is adjacent to your core, the customer already has a preferred vendor, and speed matters more than control.

## 2. Pick the integration depth

Depth should match evidence of demand, not enthusiasm on a call.

| Depth | What it is | Evidence needed first | Typical owner |
|-------|-----------|-----------------------|---------------|
| 1. Listed | Directory entry, shared docs, a connector the partner built | Ten or more shared customers asking | Partner manager |
| 2. Certified | Tested integration, supported by both sides, named in onboarding | Joint customers adopting it without hand-holding | Partner manager and a product manager |
| 3. Embedded | The partner's capability appears inside your product, or yours in theirs | Measurable lift in activation or retention for joint users | Product, with an exec sponsor |

These levels map to `integration_depth` in `data/partners.csv`.

Move up one level at a time. Each step should be earned by usage at the level below.

## 3. Scope the integration

Write the scope on one page before engineering starts.

- **Customer job:** the task a joint customer finishes faster or better
- **Data flow:** what moves, in which direction, and who is the system of record
- **Identity and permissions:** how the user authenticates and what each side can see
- **Failure behavior:** what the customer sees when the other side is down
- **Support model:** who takes the first ticket and how escalation works
- **Success metric:** one number, with a target and a review date

If the two teams cannot agree on the customer job in one sentence, stop there.

## 4. Agree the commercial shape

Keep the first agreement simple and time-boxed.

| Model | Use when | Watch for |
|-------|----------|-----------|
| No money changes hands | Both sides gain retention or reach | Nobody is accountable for adoption |
| Referral fee | One side clearly originates demand | Disputes over who sourced the deal |
| Revenue share or resale | The partner's product is sold on your paper | Margin, support cost, renewals |
| OEM or embedded license | Their capability ships inside your product | Dependency, pricing changes, exit terms |

Always settle data rights, exit terms, and what happens to joint customers if the partnership ends.

## 5. Launch it like a product

An integration nobody is told about does not get used. See the `integration-launch-plan` skill.

- Sales and customer success on both sides can explain it in two sentences
- Three named joint customers are live before the announcement
- The success metric from the scope has an owner and a 90-day review

## 6. Review and decide

At 90 days, make one of three calls: deepen, hold, or retire. Retiring an unused integration is a good outcome; it returns maintenance time to things customers use.

## Common mistakes

- Signing the partnership before identifying a single joint customer
- Building to depth 3 because the partner is a famous brand
- Measuring the integration by launch date instead of usage
- Leaving support ownership undefined until the first outage

## Related

- Skill: [product-partnership-evaluator](../skills/product-partnership-evaluator/SKILL.md)
- Skill: [integration-launch-plan](../skills/integration-launch-plan/SKILL.md)
- [Back to all playbooks](README.md)
