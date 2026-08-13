# Branch audit

The old `orx/*` names are retained here only as historical provenance. Each
branch is renamed to describe the claim or release role it carries.

| Historical branch | Clean branch | Purpose |
| --- | --- | --- |
| `orx/historical-judged-baseline-5-12` | `historical/judged-baseline-5-of-12` | Preserve the earlier judged Space revision and its 5/12 baseline. |
| `orx/c1-exact-minimax-proof-certificate` | `audit/c1-vwgf-s-jko-equivalence` | Verify Proposition 3.1’s minimax-order and VWGF/S-JKO equivalence certificate. |
| `orx/c1-evaluator-visible-evidence-bundle` | `release/c1-evaluator-evidence` | Publish Claim 1 evidence and evaluator-facing claim pages. |
| `orx/c2-exact-wasserstein-gradient-update` | `audit/c2-wasserstein-jko-update` | Verify Proposition 3.2’s `gamma=1/2`, `epsilon=2tau` update identity. |
| `orx/c2-evaluator-visible-evidence-bundle` | `release/c2-evaluator-evidence` | Publish Claim 2 evidence and evaluator-facing claim pages. |
| `orx/c3-exact-dv-proof-certificate` | `audit/c3-donsker-varadhan-bound` | Verify the pointwise DV-versus-classical KL variational bound. |
| `orx/c3-evaluator-visible-evidence-bundle` | `release/c3-evaluator-evidence` | Publish Claim 3 evidence and evaluator-facing claim pages. |
| `orx/c4-eq18-discriminator-counterexample` | `audit/c4-eq18-discriminator` | Separate Equation 18’s learned-kernel saddle problem from fixed-kernel Algorithm 1. |
| `orx/c4-evaluator-visible-evidence-bundle` | `release/c4-evaluator-evidence` | Publish Claim 4’s narrow falsification and evaluator-facing pages. |
| `orx/c5-exhaustive-source-table-falsification` | `audit/c5-fid-consistency` | Exhaust the reported CIFAR-10 tables against the consistency quantifier. |
| `orx/c5-evaluator-visible-evidence-bundle` | `release/c5-evaluator-evidence` | Publish Claim 5’s table evidence and evaluator-facing pages. |
| `orx/c6-nontrivial-pullback-metric-certificate` | `audit/c6-parametric-flow` | Verify Proposition 6.3 with a nonlinear, non-identity pullback metric. |
| `orx/c6-evaluator-visible-evidence-bundle` | `release/c6-evaluator-evidence` | Publish Claim 6 evidence and evaluator-facing claim pages. |
| `orx/final-publication-package` | `release/final-publication-package` | Preserve the final publication package before cumulative release. |
| `orx/release-candidate-report-and-logbook` | `release/cumulative-candidate` | Preserve the cumulative evaluator-visible regression and release report. |

`main` is the publication surface. Superseded `orx/*` refs are deleted from
the live GitHub repository after the clean refs are published.
