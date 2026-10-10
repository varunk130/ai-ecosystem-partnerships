# How to Use

- [Install](#install)
- [Commands](#commands)
- [Input files](#input-files)
- [Using the skills](#using-the-skills)
- [Running the tests](#running-the-tests)

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

### Options

| Option | Commands | Effect |
|--------|----------|--------|
| `--format table\|json\|csv` | all | Output format; `table` is the default |
| `--json` | all | Shorthand for `--format json` |
| `--partner NAME` | all | Show one partner only, matched case-insensitively |
| `--weights FILE` | `score` | Score with custom weights from a JSON file |
| `--opportunities FILE` | `overlap` | Rank each partner's plays by priority and open amount, and add an `open_amount` column |

A weights file names all five dimensions and sums to 1. See `data/weights.pipeline-heavy.json` for an example.

### Errors

A missing file, a missing column, an invalid value, or an unknown partner name prints one line to stderr and exits with code 2.

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

`opp_id,account,amount,stage,partner,role,domain`

- `stage` is `open`, `won`, or `lost`
- `role` is `sourced`, `influenced`, or `none`
- Leave `partner` empty when `role` is `none`; any other combination is rejected
- `domain` is optional. When present, it joins opportunities to the account lists for `overlap --opportunities`

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
