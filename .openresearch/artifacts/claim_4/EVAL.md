# Claim 4 evaluator checklist

- Exact source and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim4_eq18_falsification.py`
- Independent checker: valid PSD-kernel Equation-18 instance, exhaustive grid
- Negative control: substitute fixed-kernel Algorithm 1; must exit 1
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Frozen scientific Git SHA: `241a8aeed58b5f5d5dd26f83eb623e7b535db97d`
- Successful run: `9cc03198-677d-46e9-857e-5846fe08e772`
- Compute: estimated 1 core; HF `cpu-upgrade`; 64 logical CPUs exposed;
  cumulative verifier runtime 4.800017 s; job 37 s including setup
- Current status: `FALSIFIED`
