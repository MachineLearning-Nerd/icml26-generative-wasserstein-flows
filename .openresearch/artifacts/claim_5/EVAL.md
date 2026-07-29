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
- Frozen Git SHA: `3e951a4fba16e722ad64fe751f343d529ebdb74a`
- Successful run: `a915c7f0-113b-4a29-ab7d-301f2d9c72fa`
- Raw result: `raw_result.json`
- Independent checker: `checker_output.json`
- Failure-control output: `negative_control_output.json`
- Compute: estimated 1 core; HF `cpu-upgrade`; 64 logical CPUs exposed;
  verifier 0.721391 s; job 21 s including setup
- Current status: `FALSIFIED`
