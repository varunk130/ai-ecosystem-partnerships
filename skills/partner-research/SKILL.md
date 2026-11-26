---
name: partner-research
description: 'Researches a current or prospective partner from its public website: who it sells to, what it claims, how it integrates, and how well its customers match our ICP. Produces a one-page partner profile and a draft partners.csv row so the partner can be scored. Use when: research a partner, evaluate a new partner, who are their customers, partner due diligence, company intel, scan their website, add a partner to the portfolio.'
---

# Partner Research (SCOUT)

Turn a company name or URL into evidence: who the partner's customers are, how it positions itself, how it connects to our product, and a first estimate of fit. The output feeds straight into `partner-eco score`, so a new partner can be tiered next to the existing portfolio.

## When to Use

- A new partner asks to join the program, or we are recruiting one
- Before a first partner meeting or a joint business plan
- Refreshing an existing partner's profile before a QBR
- Checking a competitor's partners or customers for overlap

## What You'll Need

**Critical inputs (ask if not provided):**

- The partner's company name or website URL

**Nice-to-have:**

- Our ICP in one or two sentences (industries, company sizes, buyers)
- Our account list (`our_accounts.csv`) to check named customers for overlap
- What we already know: joint customers, pipeline, exec sponsor, certified people

## SCOUT Framework

| Step | What it does | Output |
|------|--------------|--------|
| **S**can | Fetch the homepage, customers or case-studies page, integrations or marketplace page, and about page | Page notes with URLs |
| **C**apture | List named customers, testimonials, metrics, and integrations shown on the site | Evidence table |
| **O**utline | Summarize what they sell, to whom, and their main claims | Company profile |
| **U**ncover | Group customers by industry and size; compare with our ICP and our account list | ICP overlap estimate, shared accounts |
| **T**abulate | Write the one-page profile and the draft `partners.csv` row | Profile + CSV row |

## Process

### 1. Scan

Fetch, in order: homepage; `/customers`, `/case-studies`, or `/stories`; `/integrations`, `/partners`, or `/marketplace`; `/about`. Record the URL of each page used.

### 2. Capture

| # | Customer | Source page | Evidence | Detail |
|---|----------|-------------|----------|--------|
| 1 | Name | Case studies | Case study + quote | "Quote", Person, Title |

**Rules:**

- Include only customers the site names: logo, case study, testimonial, or named reference. Never infer customers.
- Note the evidence type for each one; case studies and quotes outrank logos.
- Record integrations exactly as listed, including any with our product or our cloud marketplace.

### 3. Outline

Company name, one-line description, tagline, target buyers, key metrics they claim (with the page each came from), and two or three notable claims.

### 4. Uncover

- **ICP overlap:** the share of named customers that fit our ICP. With fewer than ten named customers, say the estimate is low-confidence.
- **Shared accounts:** named customers whose domain is in `our_accounts.csv`. These become rows in the partner's account list for `partner-eco overlap`.
- **Integration depth:** 0 if no integration with us, 1 if listed in a directory, 2 if certified, 3 if embedded in their product.
- **Patterns:** the industries, company sizes, and use cases that dominate.

### 5. Tabulate

Write the one-page profile, then the draft CSV row. Fields the website cannot show (pipeline, exec sponsor, certified people) come from our CRM or partner team; if unknown, use `0` or `no` and mark them as unknown so the score is read as a floor.

```text
name,partner_type,region,icp_overlap,integration_depth,joint_customers,pipeline_sourced,pipeline_influenced,exec_sponsor,certified_people
Arbor Robotics,isv,NA,0.65,1,4,0,0,no,0
```

Then run `partner-eco score partners.csv --partner "Arbor Robotics"` to see the tier and the weakest dimension.

## Output

1. **Partner profile** (one page): what they do, who they sell to, evidence table, ICP overlap estimate with confidence, integrations, shared accounts, sources.
2. **Draft `partners.csv` row**, with unknown fields called out.
3. **Next step**: the tier the row scores into, and the one question to ask the partner that would change the score most.

If a slide is wanted and a deck skill is available, put the profile on one slide: metrics strip on top, profile and target buyers on the left, customer evidence on the right.

## Quality Checks

- [ ] Every customer and metric links to the page it came from
- [ ] No inferred customers
- [ ] ICP overlap shows how many named customers it is based on
- [ ] Unknown CSV fields are marked as unknown, not guessed

## Chain Connections

- **Feeds into:** `partner-fit-scorecard` (score and tier), `co-sell-account-mapping` (shared accounts), `ecosystem-review` (portfolio report)
- **Pairs with:** `joint-business-plan` once a partner reaches the Strategic tier
