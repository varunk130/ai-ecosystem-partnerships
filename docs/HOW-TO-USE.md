# How to Use

## Install

The toolkit has no third-party dependencies. Python 3.10 or newer is enough.

```bash
git clone https://github.com/varunk130/ai-ecosystem-partnerships.git
cd ai-ecosystem-partnerships
python -m partner_ecosystem score data/partners.csv
```

To get the `partner-eco` command on your path:

```bash
pip install -e .
partner-eco score data/partners.csv
```

## Commands

| Command | Input | Answers |
|---------|-------|---------|
| `score <partners.csv>` | Partner portfolio | Which partners deserve investment, and what holds each back |
| `overlap <ours.csv> <theirs.csv>` | Two account lists | Which shared accounts to work, and how |
| `attribution <opportunities.csv>` | Opportunity export | What partners sourced and influenced, and whether attached deals win more |

Add `--json` to any command for machine-readable output.

## Input files

### partners.csv

| Column | Type | Meaning |
|--------|------|---------|
| `name` | text | Partner name |
| `partner_type` | `isv`, `si`, `reseller`, `cloud`, `agency` | Kind of partner |
| `region` | text | Free-form label, such as `NA` or `EMEA` |
| `icp_overlap` | 0-1 | Share of their customers inside your ICP |
| `integration_depth` | 0-3 | 0 none, 1 listed, 2 certified, 3 embedded |
| `joint_customers` | integer | Customers you share today |
| `pipeline_sourced` | number | Trailing-12-month pipeline the partner originated |
| `pipeline_influenced` | number | Trailing-12-month pipeline the partner helped on |
| `exec_sponsor` | `yes` / `no` | A named executive owns the relationship on their side |
| `certified_people` | integer | Their people trained on your product |

### Our accounts and partner accounts

- Ours: `domain,name,status` with status `customer`, `open_opp`, or `prospect`
- Theirs: `partner,domain,status` with status `customer` or `prospect`

Domains may be full URLs; scheme, `www.`, port, path, and case are ignored when matching.

### opportunities.csv

`opp_id,account,amount,stage,partner,role`

- `stage` is `open`, `won`, or `lost`
- `role` is `sourced`, `influenced`, or `none`
- Leave `partner` empty when `role` is `none`; any other combination is rejected

## Using the skills

Each folder under `skills/` is a self-contained skill.

**Claude Code**

```bash
cp -r skills/partner-fit-scorecard ~/.claude/skills/
```

**GitHub Copilot**: copy the folder into `.github/skills/` in your repository.

Then ask in plain language, for example "score my partner portfolio" or "prepare a QBR brief for Northwind Data".

## Running the tests

```bash
python -m unittest discover -v
```
