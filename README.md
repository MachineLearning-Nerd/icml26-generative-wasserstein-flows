# Reproducing A Unifying View of Variational Generative Wasserstein Flows

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/blob/main/notebooks/gwf_reproduction.py)

This CPU-only campaign replaced five toy checks and one deferred claim with
six exact, executable claim contracts. Claims 1, 2, 3, and 6 are **VERIFIED**;
Claims 4 and 5 are narrowly **FALSIFIED**. The strongest observed result is
from the paper's complete CIFAR-10 table: Jensen–Shannon changes from
`14.60` FID without JKO to a best reported `15.23` with JKO (`+0.63`, lower is
better), contradicting only the word “consistent.” We did not substitute a
CPU image model for the authors' H100-scale training.

The exact theorem checks use symbolic certificates plus continuous independent
checks. The managed experiments used Hugging Face `cpu-upgrade`; local CPU was
limited to short, single-core inspection and validation. The live judged score
remains **5/12** while Space revision
[`ecb662a76ee42e4a767b465eec292c943d9aac35`](https://huggingface.co/spaces/DineshAI/sJ7ngz2eQx/tree/ecb662a76ee42e4a767b465eec292c943d9aac35)
awaits evaluator judgment.

- [Illustrated reproduction report](reports/gwf_reproduction/report.md)
- [Final forecast and release report](reports/gwf_reproduction/release_report.md)
- [Self-contained Marimo tutorial](notebooks/gwf_reproduction.py)
- [Exact published Space mirror](release_candidate_space/pages/index.md)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| [`orx/historical-judged-baseline-5-12`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/historical-judged-baseline-5-12) | Freeze the judged baseline | `uv run --frozen python run_campaign.py` | Historical rejected baseline, 5/12 | HF `cpu-upgrade`, 27 s |
| [`orx/c3-exact-dv-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/c3-exact-dv-proof-certificate) | Exact DV certificate | `uv run --frozen python run_campaign.py` | Claim 3 VERIFIED | HF `cpu-upgrade`, 32 s |
| [`orx/c5-exhaustive-source-table-falsification`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/c5-exhaustive-source-table-falsification) | Exhaust complete FID tables | `uv run --frozen python run_campaign.py` | Claim 5 narrowly FALSIFIED | HF `cpu-upgrade`, 26 s |
| [`orx/c1-exact-minimax-proof-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/c1-exact-minimax-proof-certificate) | Exact minimax-order proof | `uv run --frozen python run_campaign.py` | Claim 1 VERIFIED | HF `cpu-upgrade`, 32 s |
| [`orx/c2-exact-wasserstein-gradient-update`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/c2-exact-wasserstein-gradient-update) | Exact WGD/JKO update | `uv run --frozen python run_campaign.py` | Claim 2 VERIFIED | HF `cpu-upgrade`, 37 s |
| [`orx/c4-eq18-discriminator-counterexample`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/c4-eq18-discriminator-counterexample) | Distinguish Algorithm 1 from Equation 18 | `uv run --frozen python run_campaign.py` | Claim 4 narrowly FALSIFIED | HF `cpu-upgrade`, 37 s |
| [`orx/c6-nontrivial-pullback-metric-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/c6-nontrivial-pullback-metric-certificate) | Nontrivial preconditioning certificate | `uv run --frozen python run_campaign.py` | Claim 6 VERIFIED | HF `cpu-upgrade`, 37 s |
| [`orx/release-candidate-report-and-logbook`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/tree/orx/release-candidate-report-and-logbook) | Cumulative evaluator-visible regression | `uv run --frozen python run_campaign.py` | All six current verdicts pass; controls exit 1 | HF `cpu-upgrade`, 37 s |
| `main` | Public landing page, report, notebook, and Space mirror | Not run as an experiment (publication surface) | Published; awaiting live judge | No experiment compute |

## Upstream workspace

ICML 2026 agent reproduction workspace for sJ7ngz2eQx.
