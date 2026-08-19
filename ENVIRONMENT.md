# Environment and reproduction boundary

## Locked command

Run the cumulative audit from `main` with:

```bash
uv run --frozen python run_campaign.py
```

The project pins Python `3.11` in [`.python-version`](.python-version),
dependencies in [`pyproject.toml`](pyproject.toml), and the full resolution in
[`uv.lock`](uv.lock). The current theorem, finite counterexample, table, and
fixed-sweep routes are deterministic and CPU-suitable; no random seed is
required for the audited checks.

## What the command checks

- source-preserving exact certificates and independent continuous checks for
  Claims 1–3;
- the Equation 18 optimization order and PSD-kernel counterexample for Claim 4;
- all named divergence rows, all reported JKO settings, and the different-seed
  table for Claim 5;
- the Frechet remainder, nontrivial pullback metric, small-`tau` slopes, and
  identity-metric control for Claim 6;
- one failing negative control per claim.

## Runtime boundary

The verified/falsified results do not claim a new image-training run. The
reported CIFAR-10 tables are audited as published, and the continuous Claim 6
experiment is a mechanism check rather than a neural implementation. A
CPU-downscaled FID experiment would change the paper’s protocol and is not used
to upgrade the evidence.
