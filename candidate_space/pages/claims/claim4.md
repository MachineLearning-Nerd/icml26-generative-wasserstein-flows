# Claim 4 — Equation 18 discriminator requirement

**Verdict: FALSIFIED for the no-discriminator conjunct attached to Equation
18.**

## Exact claim tested

The imported claim says that the Equation-18 JKO-regularized MMD-GAN does not
require explicit discriminator optimization. The paper actually distinguishes
two schemes:

| Scheme | Kernel | Paper optimization | Discriminator |
| --- | --- | --- | --- |
| Algorithm 1 | fixed | closed-form MMD witness | no adversarial optimization |
| Equation 18 / Algorithm 2 | learned `k_phi` | `max_phi min_T` | explicit `phi` update |

See the [contract](../../evidence/claim4/claim_contract.json) and
[source audit](../../evidence/claim4/source_audit.md).

## Direct paper and implementation evidence

Equation (18) is

`max_phi min_T 1/2 ||Id-T||² + MMD²_{k_phi}(T#mu_l,nu)`.

Appendix D.4 writes `phi* in argmax_phi 1/2 MMD²_{k_phi}` and Algorithm 2
performs gradient ascent on `phi`. The authors' documented MMD+JKO training
path executes `optimizerD.step()`. Therefore the no-adversary statement for
fixed-kernel Algorithm 1 cannot be transferred to Equation 18.

## Independent counterexample

For `mu=delta_1`, `nu=delta_0`, `T_t(1)=t`, `phi in [0,1]`, and the valid PSD
kernel `k_phi(x,y)=phi²xy`, Equation (18) becomes

`max_phi min_t 0.5(1-t)² + phi²t²`.

The analytic solution and an exhaustive 1001-point sweep both give
`phi*=1`, `t*=1/3`. Suppressing the discriminator by fixing `phi=0` gives
`t=1`: the generator solution shifts by exactly `2/3`.

Download the [raw result](../../evidence/claim4/raw_result.json) and
[checker output](../../evidence/claim4/checker_output.json).

## Reproducibility and control

Fixed command:

```bash
uv run --frozen python run_campaign.py
```

The [verifier source](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/blob/241a8aeed58b5f5d5dd26f83eb623e7b535db97d/verification/claim4_eq18_falsification.py)
ran successfully as HF run `9cc03198-677d-46e9-857e-5846fe08e772`.
It was estimated at one core, used `cpu-upgrade`, exposed 64 logical CPUs,
and took 4.800017 seconds cumulatively (37 seconds including setup).

The negative control substitutes the true fixed-kernel Algorithm-1 statement.
The completeness gate rejects it for omitting Equation 18 and exits 1. See the
[control output](../../evidence/claim4/negative_control_output.json).

## Limitation

This does not dispute the GWF extension to W1 or squared MMD, nor the
non-adversarial fixed-kernel scheme. It falsifies only the imported
no-discriminator conjunct specifically attached to Equation 18. See the
[full limitations](../../evidence/claim4/limitations.md).
