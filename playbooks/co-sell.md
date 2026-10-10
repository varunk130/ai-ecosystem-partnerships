# Co-Sell

Co-sell is two companies working the same account toward a result that is better for the customer than either would deliver alone. It runs on trust, and trust runs on rules.

## 1. Check the preconditions

Do not start co-sell until all four are true.

- A product reason exists: an integration at certified depth or better, or a clear services fit
- Both sales teams are paid, or at least not penalized, for partner deals
- Data sharing is agreed in writing
- Each side has named one person who can unblock a deal

## 2. Map accounts and pick plays

```bash
python -m partner_ecosystem overlap data/our_accounts.csv data/partner_accounts.csv --opportunities data/opportunities.csv
```

| Play | Situation | First action |
|------|-----------|--------------|
| Co-sell | We have an open deal, they have the customer | Ask their account owner for the buyer's priorities and a joint call |
| Joint pursuit | We have an open deal, they are also selling in | Agree one combined story before the next meeting |
| Intro request | We are cold, they have the customer | Ask for a named introduction with a reason the customer cares |
| Joint expansion | Both have the customer | Build a combined value case and a reference |
| Referral to partner | We have the customer, they do not | Make the introduction; this is what earns the next ask |
| Co-marketing | Neither is in | Run one targeted campaign to the shared prospect list |

Work five to ten accounts per partner per quarter. A list of two hundred shared accounts is a spreadsheet, not a plan.

## 3. Write the rules of engagement

Agree these before the first shared deal, on one page.

| Topic | Rule to settle |
|-------|----------------|
| Deal registration | Who registers, how long protection lasts, what renews it |
| Sourced against influenced | A definition both sides can apply without arguing |
| Account ownership | Who leads the customer conversation, and when that changes |
| Information sharing | What can be shared about the account, and with whom |
| Conflict | What happens when two partners claim the same deal |
| Pricing | Who can discount what, and who approves a joint offer |

A workable definition: **sourced** means the partner introduced an opportunity that did not exist in your pipeline; **influenced** means the partner took a documented action on a deal you already had.

## 4. Run the deal together

| Stage | Our side | Partner's side |
|-------|----------|----------------|
| Qualify | Share the opportunity and the gap | Confirm relationship and buyer context |
| Plan | Draft a joint account plan | Add contacts, history, and risks |
| Engage | Lead the commercial conversation | Bring the technical or executive sponsor |
| Close | Own paper and pricing | Support procurement and references |
| Deliver | Hand over to customer success | Implement or integrate |
| Record | Log partner role on the opportunity | Confirm the same on their side |

Recording the partner role at the time of the action is the only way attribution stays credible.

## 5. Keep the exchange balanced

`overlap` prints asks against gives for each partner. If you only ever ask, the partner's sellers stop answering. Lead with a referral or a customer introduction when you can.

## 6. Review

```bash
python -m partner_ecosystem attribution data/opportunities.csv --partner "Northwind Data"
```

Review weekly on shared deals and quarterly on results. Ask three questions: what did we close together, what stalled and why, and what did each side give.

## Common mistakes

- Sharing a full account list before agreeing how it may be used
- Counting every deal a partner touched as sourced
- Running co-sell with no change to seller compensation
- Treating the partner manager as the only relationship; sellers need to know sellers

## Related

- Skill: [co-sell-account-mapping](../skills/co-sell-account-mapping/SKILL.md)
- Next: [Leading a partner ecosystem](leading-a-partner-ecosystem.md), for the cadence co-sell runs on
- [Back to all playbooks](README.md)
