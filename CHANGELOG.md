# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `--weights` option on `score` for custom scoring weights from a JSON file
- `borderline` column on `score` for partners within three points of a tier threshold
- `--partner` filter and `--format table|json|csv` on every command
- Give/ask balance per partner under the `overlap` table
- Closed-deal counts next to win rate in `attribution`
- Guidance on estimating `icp_overlap`

### Fixed
- Bad input now prints a one-line error and exits 2 instead of a traceback

### Changed
- Standardized on American spelling across code, docs, and skills
- Added tables of contents to the README and usage guide
- Added docstrings to the CLI handlers and the opportunity loader

## [0.1.0] - 2026-10-05

### Added
- Partner data model with validation and CSV loading
- Weighted fit scoring across ICP fit, pipeline, integration, traction, and commitment
- Tiering into Strategic, Growth, Emerging, and Watchlist with a motion per tier
- Account overlap mapping with a suggested play for each shared account
- Sourced vs influenced attribution and partner-attached win-rate lift
- `partner-eco` CLI with `score`, `overlap`, and `attribution` commands and `--json` output
- Three skills: `partner-fit-scorecard`, `co-sell-account-mapping`, `partner-qbr-brief`
- Synthetic sample data, usage guide, and scoring methodology
- CI on Python 3.10 and 3.12, code owners, and a pull request template
