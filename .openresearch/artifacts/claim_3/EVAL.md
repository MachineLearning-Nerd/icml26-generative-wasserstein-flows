# Claim 3 evaluator checklist

- Exact source statement and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim3_exact.py`
- Independent checker: continuous Gaussian family, 60 off-optimum critics
- Negative control: reversed inequality, required nonzero exit
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Raw run output: emitted between `BEGIN_RAW_JSON` and `END_RAW_JSON`
- Current limitation: machine-checking covers the scalar inequality; the
  measure-theory lift is an explicit analytic derivation
