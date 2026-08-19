# Audit report

## Executive result

Claims 1–3 and 6 pass their scoped mathematical contracts. Claim 4 is narrowly
falsified for the no-discriminator reading attached to Equation 18. Claim 5 is
narrowly falsified for the complete-table “consistent improvements” quantifier.
The only score claimed is the historical external result `5/12`.

Overall status:

`PARTIAL_C1_C2_C3_C6_VERIFIED_C4_C5_NARROWLY_FALSIFIED_HISTORICAL_SCORE_5_OF_12_NO_CURRENT_SCORE`

## Claim matrix

| Claim | Result | Primary route | Main boundary |
| --- | --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | VWGF/S-JKO gap certificate and three Gaussian cases | Measure-theoretic premises are audited, not proof-assistant formalized. |
| C2 | `VERIFIED_SCOPED` | Exact coefficient identity and three divergence updates | Depends on Lemma F.2’s transport/regularity assumptions. |
| C3 | `VERIFIED_SCOPED` | Exact DV scalar gap and 60 deterministic cases | The probability-measure lift is reconstructed analytically. |
| C4 | `FALSIFIED_SCOPED` | Equation 18 source inspection and finite PSD-kernel counterexample | Only the no-discriminator conjunct is rejected; fixed-kernel Algorithm 1 remains separate. |
| C5 | `FALSIFIED_SCOPED` | Complete primary and different-seed FID table audit | Falsifies “consistent” across all named divergences, not every improvement. |
| C6 | `VERIFIED_SCOPED` | General Frechet certificate and nonlinear off-diagonal metric sweep | Continuous mechanism audit, not a neural or proof-assistant reproduction. |

## Quantitative evidence

- C1: maximum VWGF/S-JKO agreement error `4.44e-14`.
- C2: maximum `gamma=1/2` update error `1.25e-8`; wrong-`gamma` minimum error
  `0.0237359`.
- C3: 60 continuous cases; minimum DV-classical gap `0.017834658`; maximum
  optimum equality error `8.33e-17`.
- C4: exact optimizer `phi*=1,t*=1/3`; fixing `phi=0` shifts the generator
  solution to `t=1`, a difference of `2/3`.
- C5: Jensen–Shannon FID changes from `14.60` to best JKO `15.23` (`+0.63`);
  the different-seed table changes `16.84` to `16.87` (`+0.03`).
- C6: theorem-residual slope `0.9833`, velocity-error slope `0.9815`, metric
  minimum eigenvalue `0.2468`, and off-diagonal magnitude at least `0.7283`.

## Score and publication boundary

- Historical live score: `5/12`
- Current score claim: `false`
- Publication allowed: `false`
- Official author endorsement: `false` / not claimed

Open [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md) for production paths and
controls, and [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) for source/version scope.
