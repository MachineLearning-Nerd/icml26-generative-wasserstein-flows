# Claim 1 evaluator checklist

- Exact statement and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim1_exact.py`
- Exact symbolic certificate: coupling/minimax/order gap closure
- Independent checker: three 2-D anisotropic continuous Gaussian KL cases
- Negative control: remove Monge recovery; countermodel must exit 1
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Frozen Git SHA: `c8194ebdf3e34f76d54a2bab1a185e8704949bce`
- Successful run: `200d04b0-a5cc-4cea-8dbd-6e0631bc2ca5`
- Raw result: `raw_result.json`
- Independent checker: `checker_output.json`
- Failure-control output: `negative_control_output.json`
- Compute: estimated 1 core; HF `cpu-upgrade`; 64 logical CPUs exposed;
  cumulative verifier 1.837545 s; job 27 s including setup
- Current status: `VERIFIED`
