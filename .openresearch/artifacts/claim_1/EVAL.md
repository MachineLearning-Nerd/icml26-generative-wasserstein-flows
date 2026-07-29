# Claim 1 evaluator checklist

- Exact statement and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim1_exact.py`
- Exact symbolic certificate: coupling/minimax/order gap closure
- Independent checker: three 2-D anisotropic continuous Gaussian KL cases
- Negative control: remove Monge recovery; countermodel must exit 1
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Current status: pending formal ORX run
