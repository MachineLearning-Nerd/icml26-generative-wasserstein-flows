# Claim 6 — parametric JKO and the preconditioned flow

**Verdict: VERIFIED under the exact Proposition 6.3 assumptions.**

## Exact claim tested

For an exact minimizer of Equation (25), if the parametrization is L2
Frechet differentiable, its Jacobian is square integrable, the energy is
differentiable, and `Delta=theta_plus-theta_old=O(tau)`, then

`G(theta_plus) Delta/tau = -grad energy(theta_plus)+o(1)`.

When `G` is invertible, this is the implicit first-order discretization of the
`G^-1`-preconditioned flow. See the
[contract](../../evidence/claim6/claim_contract.json),
[source audit](../../evidence/claim6/source_audit.md), and
[method](../../evidence/claim6/method.md).

## General certificate

Differentiating the JKO objective gives

`(1/tau) integral J_plus^T(F_plus-F_old)dmu + grad energy(theta_plus)=0`.

Frechet differentiability yields
`F_plus-F_old=J_plus Delta+r`, with `||r||=o(||Delta||)`. The quadratic
term becomes `G(theta_plus)Delta`; Cauchy-Schwarz keeps the remaining term
at `o(||Delta||)`. Since `||Delta||=O(tau)`, division by `tau` makes that
remainder `o(1)`. The verifier machine-audits this chain.

## Nontrivial metric experiment

The independent checker uses `mu=N(0,I2)` and

`F_(a,b)(z)=z+(a+0.35ab, 0.45a+b+0.15a²)`.

This is invertible in `z`, nonlinear in two parameters, and has
`G=J^T J` with minimum eigenvalue 0.2468 and absolute off-diagonal at least
0.7283. It does not collapse preconditioning to `G=1`.

| tau | theorem residual | velocity error | identity-G residual |
| ---: | ---: | ---: | ---: |
| 0.200 | 0.081788 | 0.660115 | 1.153388 |
| 0.100 | 0.049414 | 0.391497 | 1.423935 |
| 0.050 | 0.027376 | 0.216592 | 1.607694 |
| 0.020 | 0.011677 | 0.092707 | 1.740904 |
| 0.010 | 0.005968 | 0.047479 | 1.790102 |
| 0.005 | 0.003017 | 0.024033 | 1.815717 |
| 0.002 | **0.001215** | **0.009685** | **1.831428** |

The theorem-residual log-log slope is 0.9833 and the velocity-error slope is
0.9815, both consistent with first-order convergence. Download the
[raw sweep](../../evidence/claim6/raw_result.json) and
[checker output](../../evidence/claim6/checker_output.json).

## Control and reproducibility

The negative control replaces `G(theta_plus)` by the identity and leaves
residual 1.8314 at the smallest step, so the verifier exits 1. See the
[control output](../../evidence/claim6/negative_control_output.json).

Fixed command:

```bash
uv run --frozen python run_campaign.py
```

The [verifier source](../../verification/claim6_preconditioned_flow.py)
passed in HF run `ab42506e-29c2-45e7-8b89-bd3d03ba4f5e`.
The verifier's frozen Git SHA was
`3c66d998242e2887de319cbbdf52b110dc06d2cd`.
It was estimated at one core, ran on `cpu-upgrade`, exposed 64 logical CPUs,
and took 4.910138 seconds cumulatively (35 seconds including setup).
The symbolic and fixed-sweep checks are deterministic and use no random seeds.

## Limitation

The symbolic derivation is not a proof-assistant formalization, and the
continuous checker is not a neural network. See the
[full limitations](../../evidence/claim6/limitations.md).
