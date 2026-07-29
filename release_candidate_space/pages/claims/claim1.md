# Claim 1 — VWGF equals S-JKO

**Verdict: VERIFIED under Proposition 3.1's mathematical assumptions.** This
supersedes the **Historical rejected baseline**, which only compared a scaled
discrete JKO value to itself on ten points.

## Exact claim

For `mu_l, nu in P_ac,2(R^d)`, the unrestricted VWGF objective (6)
`inf_T sup_h L(T,h)` equals the unrestricted S-JKO objective (9)
`sup_h inf_T L(T,h)` after `h -> -h`. This is an objective-value theorem,
not a claim that finite neural classes or optimizers always reach the saddle.

See the [exact contract](../../evidence/claim1/claim_contract.json),
[source audit](../../evidence/claim1/source_audit.md), and
[method](../../evidence/claim1/method.md).

## Exact proof certificate

Let:

- `A = inf_T sup_h L(T,h)`;
- `C = sup_h inf_gamma L_tilde(gamma,h)`;
- `D = sup_h inf_T L(T,h)`.

The audited coupling minimax and Monge-recovery premises give `A=C`. Weak
duality gives `A-D >= 0`, while map-induced couplings being a subset gives
`D-C >= 0`. SymPy checks the exact identity

`(A-D) + (D-C) = A-C`

with residual zero. Since both gaps are nonnegative and their sum is zero,
both vanish and `A=D`.

## Independent continuous check

| Case | tau | VWGF | S-JKO | absolute error |
| --- | ---: | ---: | ---: | ---: |
| anisotropic Gaussian 1 | 0.17 | 3.9787486463292705 | 3.9787486463292496 | 2.09e-14 |
| anisotropic Gaussian 2 | 0.43 | 4.0256959651823525 | 4.0256959651823490 | 3.55e-15 |
| anisotropic Gaussian 3 | 0.08 | 7.8805084632075280 | 7.8805084632074840 | 4.44e-14 |

The tolerance was `2e-7`. Download the
[checker output](../../evidence/claim1/checker_output.json).

## Reproducibility and control

The fixed command was:

```bash
uv run --frozen python run_campaign.py
```

Successful HF run `200d04b0-a5cc-4cea-8dbd-6e0631bc2ca5` used frozen Git SHA
`c8194ebdf3e34f76d54a2bab1a185e8704949bce`. It was estimated at one core,
used `cpu-upgrade`, exposed 64 logical CPUs, took 1.837545 seconds in the
cumulative verifier, and 27 seconds including setup.
The proof and Gaussian cases are deterministic and use no random seeds.

The [verifier source](../../verification/claim1_exact.py)
and [raw result](../../evidence/claim1/raw_result.json) are downloadable.

The negative control removes absolute continuity/Monge recovery and admits the countermodel
`A=1, B=C=D=0`, which satisfies all remaining order premises but not the
claimed equality. The control exits 1; see its
[output](../../evidence/claim1/negative_control_output.json).

## Limitation

The measure-theoretic theorems are audited premises rather than a Lean/Coq
development. See the full [limitations](../../evidence/claim1/limitations.md).
