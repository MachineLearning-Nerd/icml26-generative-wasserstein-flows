# Claim 2 evaluator checklist

- Exact source and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim2_exact.py`
- Exact certificate: WGD gradient map, unique gamma, epsilon/JKO scaling
- Independent checker: KL, chi2, Jensen-Shannon on 2-D continuous Gaussians
- Negative control: gamma 0.35 must exit 1
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Frozen Git SHA: `7e4dae6c5b3d6ed6a53808b942155b6115e32106`
- Successful run: `772255a4-c39d-4d64-a5d7-00c76d536b59`
- Raw result: `raw_result.json`
- Independent checker: `checker_output.json`
- Failure-control output: `negative_control_output.json`
- Compute: estimated 1 core; HF `cpu-upgrade`; 64 logical CPUs exposed;
  cumulative runtime 4.198139 s; job 37 s including setup
- Current status: `VERIFIED`
