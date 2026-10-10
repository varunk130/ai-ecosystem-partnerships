# Sample Data

Every file here is synthetic. The company names are invented and the `.example` domains cannot resolve. Do not replace these files with real partner or customer data in a public fork.

| File | Used by | Rows |
|------|---------|------|
| `partners.csv` | `score` | 12 partners across ISV, SI, reseller, cloud, and agency types |
| `our_accounts.csv` | `overlap` | 10 of our accounts with a status each |
| `partner_accounts.csv` | `overlap` | 12 partner account rows for three partners, with deliberately messy domains |
| `opportunities.csv` | `attribution`, `overlap --opportunities` | 16 opportunities, with and without a partner attached |
| `weights.pipeline-heavy.json` | `score --weights` | Example weights that favor pipeline over ICP fit |

Column definitions are in the [usage guide](../docs/HOW-TO-USE.md#input-files).

The tests pin numbers from these files, so changing a value here will fail a test. That is intended: update the test in the same commit and explain why.
