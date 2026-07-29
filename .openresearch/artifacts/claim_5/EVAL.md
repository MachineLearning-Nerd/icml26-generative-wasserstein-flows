# Claim 5 evaluator checklist

- Exact source statement and quantifier: `claim_contract.json`
- Source anchors and assumptions: `source_audit.md`
- Complete primary table: `verification/data/claim5_table4.csv`
- Independent different-seed table:
  `verification/data/claim5_different_seeds.csv`
- Executable verifier: `verification/claim5_source_falsification.py`
- Negative control: remove Jensen–Shannon; completeness audit must exit 1
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Current status: pending formal ORX run
