# Claim 3 — Donsker–Varadhan bound

Current verifier: `verification/claim3_exact.py` on the current experiment
revision. It supersedes the n=10 random-critic check in the **Historical
rejected baseline**.

## Exact claim

For probability measures `mu << nu` and every admissible bounded critic `h`,
the Donsker–Varadhan KL objective is at least the classical reverse-KL
variational objective. Their suprema equal `KL(mu||nu)`. Literal attainment is
claimed only when `1 + log(dmu/dnu)` belongs to the critic class.

## Proof certificate

Set `s = log integral exp(h) dnu`. The exact gap is
`exp(s - 1) - s`. Its derivative vanishes only at `s=1`, its second derivative
there is positive, its value there is zero, and both boundary limits are
positive infinity.

The fixed command is:

```bash
uv run --frozen python run_campaign.py
```

Pinned versions are in `pyproject.toml` and `uv.lock`. The run prints the full
symbolic certificate, continuous-Gaussian checker, failure control, Git SHA,
CPU allocation, seeds, and runtime inline. Raw output will be copied here after
the first successful proof run before release.

## Negative control

The reversed statement `classical(h) >= DV(h)` is evaluated at `s=0`; it must
exit nonzero because `DV-classical = exp(-1) > 0`.

## Limitation

SymPy certifies the scalar inequality exactly. The substitution lifting it to
arbitrary probability measures is an independently reconstructed analytic
derivation, not a formal proof-assistant development of measure theory.
