# Contributing

This repository is maintained by [@varunk130](https://github.com/varunk130). Only the maintainer can merge.

## How changes land

1. `main` is protected. Nothing is pushed to it directly.
2. Every change goes through a pull request with one approving review from the code owner.
3. History is linear: pull requests are rebased or squashed, never merge-committed.
4. CI must pass on Python 3.10 and 3.12.

## Suggesting a change

Open an issue describing the partnership problem you are trying to solve and the data you have. Forks and pull requests are welcome; expect questions about how a change affects scoring for existing partners.

## Ground rules

- **Synthetic data only.** Never commit real partner names, customer lists, or pipeline numbers.
- **No new dependencies** without a strong reason. The toolkit runs on the standard library.
- **Test what you change.** Scoring and attribution changes need a test that pins the expected number.
- **Explain weight changes.** If you move a weight, cap, or tier threshold, update `docs/scoring-methodology.md` in the same pull request.

## Local setup

```bash
python -m unittest discover -v
python -m partner_ecosystem score data/partners.csv
```
