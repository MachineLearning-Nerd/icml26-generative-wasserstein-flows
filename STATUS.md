# Audit status

**State:** mixed claim audit complete; three mathematical claims and the
parametric-flow claim are scoped-verified, while two narrower source claims are
falsified.

- Paper: [A Unifying View of Variational Generative Wasserstein Flows](https://arxiv.org/abs/2605.31369)
- Authors: Paul Caucheteux, Clément Bonet, and Anna Korba
- ICML submission: `sJ7ngz2eQx`
- Repository: [MachineLearning-Nerd/icml26-generative-wasserstein-flows](https://github.com/MachineLearning-Nerd/icml26-generative-wasserstein-flows)
- Overall status: `PARTIAL_C1_C2_C3_C6_VERIFIED_C4_C5_NARROWLY_FALSIFIED_HISTORICAL_SCORE_5_OF_12_NO_CURRENT_SCORE`
- C1–C3: `VERIFIED_SCOPED` under the paper’s stated mathematical assumptions
- C4: `FALSIFIED_SCOPED` for the no-discriminator conjunct attached to Equation 18; fixed-kernel Algorithm 1 is not rejected
- C5: `FALSIFIED_SCOPED` for the complete-table “consistent improvements” quantifier; selected divergences can still improve
- C6: `VERIFIED_SCOPED` for the stated first-order/preconditioned-flow contract and nontrivial metric audit
- Historical external score: `5/12`
- Current score claim: `false`
- Publication allowed: `false`
- Official author endorsement: `false` / not claimed
- Commit identity: all reachable history uses `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`
- Recovery bundle SHA-256: `64bb53d2c37cac907f027a248f690a2acda531107472af76eea2c2ecbc3b516a`

The inherited `9–12/12` range and `12/12` best case are forecasts only. This
repository does not convert local evidence into a new judge score.
