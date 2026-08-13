# A Unifying View of Variational Generative Wasserstein Flows

Independent, claim-by-claim reproduction audit for the ICML 2026 paper
[“A Unifying View of Variational Generative Wasserstein Flows”](https://arxiv.org/abs/2605.31369).

This repository is an audit and evidence package, not an official author
implementation. It keeps theorem assumptions, experimental quantifiers, and
negative controls explicit so a reader can distinguish a verified statement
from a narrow falsification or an experiment that was not rerun at paper scale.

## Current assessment

Claims 1, 2, 3, and 6 are `VERIFIED` under their stated mathematical
assumptions. Claims 4 and 5 are narrowly `FALSIFIED`: the audit rejects an
overly strong no-discriminator reading of Equation 18 and the word
“consistent” for the complete reported Jensen–Shannon CIFAR-10 table. These
verdicts are not a new judge score; the previous live score remains `5/12`
until the evaluator reviews the published Space revision.

| Claim | Paper statement tested | How the result is produced | Evidence and verdict |
| --- | --- | --- | --- |
| 1 | Proposition 3.1: the variational Wasserstein gradient-flow (VWGF) objective and the source-fixed JKO (S-JKO) objective agree. | Reconstruct the four optimization orders and the minimax/Monge certificate, then check three anisotropic 2-D Gaussian cases independently. | Maximum continuous agreement `4.44e-14`; the assumption-removal control fails as intended. **VERIFIED.** |
| 2 | Proposition 3.2 and Lemma F.2: `gamma = 1/2` and `epsilon = 2 tau` make one explicit Wasserstein-gradient step equal the JKO update. | Check the coefficient identity symbolically and compare KL, chi-squared, and Jensen–Shannon updates with independently optimized JKO minimizers. | Maximum update error `1.25e-8`; the wrong-`gamma` control misses every update by at least `0.0237`. **VERIFIED.** |
| 3 | The Donsker–Varadhan (DV) variational form is pointwise tighter than the classical KL variational bound and is equal at the optimum. | Reduce the gap to `exp(s - 1) - s`, prove its minimum, and run 60 continuous Gaussian cases at the optimal critic. | Equality error `8.33e-17`; the pointwise ordering and optimum control pass. **VERIFIED.** |
| 4 | Equation 18’s JKO-regularized MMD-GAN can be read as requiring no discriminator optimization. | Preserve the equation’s `max_phi min_T` order, inspect Appendix D.4/Algorithm 2 and the authors’ code, and solve a finite PSD-kernel counterexample. | `phi` must be optimized for Equation 18; suppressing it changes the minimizer. **Narrowly FALSIFIED.** This does not reject fixed-kernel Algorithm 1. |
| 5 | Section 5: JKO gives moderate, consistent FID improvements for the named f-divergences. | Exhaust the paper’s complete CIFAR-10 table and an independent-seed table rather than selecting favorable rows. | Jensen–Shannon changes from `14.60` no-JKO FID to a best reported `15.23` with JKO (`+0.63`, lower is better); the seed table repeats `16.84` to `16.87` (`+0.03`). **Narrowly FALSIFIED.** |
| 6 | Proposition 6.3: parametric JKO approaches the `G^-1`-preconditioned Wasserstein gradient flow as `tau -> 0`. | Derive the first-order Fréchet remainder and test a nonlinear two-parameter map with a parameter-dependent, off-diagonal pullback metric. | Residual slope `0.983`, metric lower eigenvalue `0.2468`, and off-diagonal magnitude at least `0.7283`; replacing `G` by identity leaves residual `1.8314`. **VERIFIED.** |

## What the paper is doing

The paper proposes Generative Wasserstein Flows (GWF), a unified view of
generative modeling through Wasserstein gradient flows and their implicit
Jordan–Kinderlehrer–Otto (JKO) discretization. It shows how a broad class of
parametric JKO schemes for `f`-divergences recover or connect existing
generative algorithms, including variational Wasserstein methods, transport
maps, and adversarial objectives.

It then extends the construction to integral probability metrics and squared
maximum mean discrepancy (MMD), clarifying the connection to GANs, studies the
effect of JKO regularization in MNIST/CIFAR-10 experiments, and analyzes
parametric flows whose distributions are induced by neural or other maps.

## Reproducing the evidence

Every experiment branch inherits the same pinned command:

```bash
uv run --frozen python run_campaign.py
```

The cumulative runner dispatches one verifier per claim and runs the intended
negative controls as subprocesses. Claims 1–3 and 6 use symbolic or exact
certificates plus continuous checks. Claim 4 uses source inspection and a
finite counterexample. Claim 5 uses all reported table rows. The image-scale
training itself was not replaced by a CPU proxy: the audit tests the paper’s
reported data and records the remaining scale limitation.

Useful entry points:

- [Claim index and published evidence](release_candidate_space/pages/index.md)
- [Illustrated reproduction report](reports/gwf_reproduction/report.md)
- [Final release report](reports/gwf_reproduction/release_report.md)
- [Claim verifiers](verification/)
- [Raw claim evidence](release_candidate_space/evidence/)
- [Reproduction notebook](notebooks/gwf_reproduction.py)
- [Evaluator-visible Space](https://huggingface.co/spaces/DineshAI/sJ7ngz2eQx)

## Branch organization

`main` is the publication surface. `audit/*` branches hold claim-specific
certificates or falsification routes, `release/*` branches hold evaluator-
visible and cumulative packages, and `historical/*` preserves the earlier
judged baseline. The complete old-to-clean mapping is in
[`branch-audit.md`](branch-audit.md). Every clean branch receives this README
and the branch map so an experiment checkout remains self-describing.

## Scope and limitations

- Verified theorem claims are audited under the paper’s assumptions; finite
  checks do not replace a formal proof assistant development.
- The two falsifications are deliberately narrow. They do not claim that all
  MMD-GAN or JKO experiments fail, only that the tested conjuncts are too
  strong as written.
- The CIFAR-10 result uses the paper’s complete reported tables and a
  different-seed table. No independent H100-scale neural training or new FID
  uncertainty estimate is claimed.
- The live judged score remains `5/12` until the evaluator assesses the new
  Space revision.

## Paper

- **Title:** A Unifying View of Variational Generative Wasserstein Flows
- **Authors:** Paul Caucheteux, Clément Bonet, Anna Korba
- **Paper:** [arXiv:2605.31369](https://arxiv.org/abs/2605.31369)
- **HTML source:** [arXiv HTML](https://arxiv.org/html/2605.31369)
- **Submission:** May 29, 2026; accepted as an ICML 2026 spotlight
- **Paper identifier:** `sJ7ngz2eQx`

## Citation

```bibtex
@misc{caucheteux2026unifying,
  title         = {A Unifying View of Variational Generative Wasserstein Flows},
  author        = {Caucheteux, Paul and Bonet, Clément and Korba, Anna},
  year          = {2026},
  eprint        = {2605.31369},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  note          = {Accepted as a spotlight at ICML 2026}
}
```

## Thank you

Thank you to Paul Caucheteux, Clément Bonet, and Anna Korba for presenting the
Wasserstein/JKO connections, optimization orders, divergence extensions, and
parametric-flow assumptions clearly enough to audit claim by claim. The paper
made it possible to preserve both the verified mathematics and the precise
limits of the image-scale evidence.

## Attribution

This independent audit is maintained by
[MachineLearning-Nerd](https://github.com/MachineLearning-Nerd). It is not
affiliated with or endorsed by the paper’s authors.
