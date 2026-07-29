# Claim 2 — explicit WGD equals the JKO update

**Verdict: VERIFIED under Proposition 3.2 and Lemma F.2's assumptions.** This
supersedes the **Historical rejected baseline**, which only multiplied a
ten-point objective by `2 tau`.

## Exact update contract

For the Moreau functional

`F_epsilon(mu) = inf_eta W2^2(mu,eta) + epsilon D_f(eta||nu)`,

one Wasserstein gradient descent step with `gamma=1/2` and `epsilon=2 tau`
must push `mu` exactly to the JKO minimizer of `D_f`.

See the [contract](../../evidence/claim2/claim_contract.json) and
[source audit](../../evidence/claim2/source_audit.md).

## Exact certificate

Lemma F.2 gives the WGD map
`Id - gamma epsilon grad phi`. The optimal transport map to the envelope
minimizer is `Id - (epsilon/2) grad phi`. SymPy finds the unique coefficient
match `gamma=1/2`. It also returns zero residual for both the transport-cost
normalization and the objective rescaling after `epsilon=2 tau`.

## Independent continuous check

The checker optimizes the continuous 2-D Gaussian Moreau envelope, estimates
its gradient by central finite differences, and compares the explicit WGD
update to the independently optimized JKO/envelope minimizer.

| Divergence | epsilon | tau | gamma=1/2 error | gamma=0.35 error |
| --- | ---: | ---: | ---: | ---: |
| KL | 0.30 | 0.15 | 1.08e-8 | 0.08638 |
| chi-squared | 0.20 | 0.10 | 1.25e-8 | 0.04716 |
| Jensen–Shannon | 0.50 | 0.25 | 1.02e-8 | 0.02374 |

The acceptance tolerance was `8e-4`. Download the
[checker output](../../evidence/claim2/checker_output.json).

## Reproducibility and control

```bash
uv run --frozen python run_campaign.py
```

Successful HF run `772255a4-c39d-4d64-a5d7-00c76d536b59` used frozen Git SHA
`7e4dae6c5b3d6ed6a53808b942155b6115e32106`. It was estimated at one core,
used `cpu-upgrade`, exposed 64 logical CPUs, took 4.198139 seconds in the
cumulative verifier, and 37 seconds including setup.

The [verifier source](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/blob/7e4dae6c5b3d6ed6a53808b942155b6115e32106/verification/claim2_exact.py)
and [raw result](../../evidence/claim2/raw_result.json) are downloadable.

Replacing `gamma=1/2` by `0.35` misses every JKO update by at least `0.02374`
and exits 1; see the
[control output](../../evidence/claim2/negative_control_output.json).

## Limitation

Lemma F.2 is an audited theorem premise rather than a Lean/Coq development.
See the full [limitations](../../evidence/claim2/limitations.md).
