# Claim 6 evaluator checklist

- Exact source and assumptions: `claim_contract.json`, `source_audit.md`
- Executable verifier: `verification/claim6_preconditioned_flow.py`
- General certificate: endpoint Frechet expansion and little-o scaling
- Independent checker: nonlinear 2-D continuous translation family
- Nontrivial metric: minimum eigenvalue 0.2468; off-diagonal at least 0.7283
- Negative control: replace G by identity; residual 1.8314; exit 1
- Fixed command: `uv run --frozen python run_campaign.py`
- Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`
- Frozen scientific Git SHA: `3c66d998242e2887de319cbbdf52b110dc06d2cd`
- Successful run: `ab42506e-29c2-45e7-8b89-bd3d03ba4f5e`
- Compute: estimated 1 core; HF `cpu-upgrade`; 64 logical CPUs exposed;
  cumulative verifier runtime 4.910138 s; job 35 s including setup
- Current status: `VERIFIED`
