# Claim 3 evaluator checklist

- Exact source statement and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim3_exact.py`
- Independent checker: continuous Gaussian family, 60 off-optimum critics
- Negative control: reversed inequality, required nonzero exit
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Successful run: `94499562-aeea-4d4f-95f4-02dd61e20d6b`
- Frozen Git SHA: `361e1508d9f1acf47c65aecdc49dbb1aff15076b`
- Raw result: `raw_result.json`
- Independent output: `checker_output.json`
- Failure-control output: `negative_control_output.json`
- Compute: estimated 1 core; HF `cpu-upgrade`; 64 logical CPUs exposed;
  verifier 0.673309 s; job 26 s including setup
- Current limitation: machine-checking covers the scalar inequality; the
  measure-theory lift is an explicit analytic derivation
