# Claim 2 evaluator checklist

- Exact source and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim2_exact.py`
- Exact certificate: WGD gradient map, unique gamma, epsilon/JKO scaling
- Independent checker: KL, chi2, Jensen-Shannon on 2-D continuous Gaussians
- Negative control: gamma 0.35 must exit 1
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Current status: pending formal ORX run
