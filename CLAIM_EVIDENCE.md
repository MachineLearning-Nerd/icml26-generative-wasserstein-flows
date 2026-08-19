# Claim-to-evidence ledger

This repository audits six source-anchored claims from *A Unifying View of
Variational Generative Wasserstein Flows*. The table records how each verdict
is produced and where its controls and limits are stored.

| Claim | Paper anchor | How the result is produced | Evidence and control | Scope and status |
| --- | --- | --- | --- | --- |
| C1 — VWGF/S-JKO equivalence | Proposition 3.1 and Equations (6), (9) | Reconstruct the four optimization orders, minimax/Monge certificate, and exact gap identity; compare three anisotropic 2-D Gaussian cases. | `release_candidate_space/evidence/claim1/raw_result.json`, `checker_output.json`, and `negative_control_output.json`; removing absolute continuity/Monge recovery produces `A=1,B=C=D=0` and fails. | Unrestricted objectives under the proposition’s measure assumptions; finite continuous checks support the certificate. **VERIFIED_SCOPED** |
| C2 — explicit Wasserstein step/JKO update | Proposition 3.2 and Lemma F.2 | Solve the coefficient identity symbolically and compare KL, chi-squared, and Jensen–Shannon updates using independent 2-D Gaussian Moreau/JKO optimization. | `release_candidate_space/evidence/claim2/raw_result.json` and checker; replacing `gamma=1/2` with `0.35` misses every update and fails. | Exact `gamma=1/2`, `epsilon=2 tau` contract with Lemma F.2 assumptions. **VERIFIED_SCOPED** |
| C3 — DV variational bound | Section 3, Equation (11) | Reduce the pointwise gap to `exp(s-1)-s`, certify its unique minimum, and run 60 deterministic Gaussian/linear-critic cases. | `release_candidate_space/evidence/claim3/raw_result.json`, `checker_output.json`, and `negative_control_output.json`; reversing the inequality at `s=0` fails. | Pointwise bound and optimum equality under the stated critic-class and absolute-continuity assumptions. **VERIFIED_SCOPED** |
| C4 — Equation 18 discriminator requirement | Equation (18), Appendix D.4, Algorithm 2 | Preserve the `max_phi min_T` order, cross-check the source/code evidence, and solve a finite PSD-kernel counterexample exactly and by a 1001-point sweep. | `release_candidate_space/evidence/claim4/raw_result.json` and checker; `phi*=1,t*=1/3`, while fixing `phi=0` gives `t=1`, a shift of `2/3`. | Only the attached no-discriminator reading is falsified. Fixed-kernel Algorithm 1 and the broader MMD/GWF extension are outside this falsification. **FALSIFIED_SCOPED** |
| C5 — consistent FID improvements | Section 5.3 and complete reported tables | Exhaust every named divergence and every reported JKO step size, then check an independent-seed table. | `release_candidate_space/evidence/claim5/table4.csv`, `different_seeds.csv`, raw result, checker, and completeness control; Jensen–Shannon worsens by `+0.63` primary and `+0.03` different-seed FID. | Falsifies the exact universal “consistent across all named f-divergences” quantifier, not every selected improvement or the underlying image-training method. **FALSIFIED_SCOPED** |
| C6 — parametric JKO/preconditioned flow | Proposition 6.3 and Equation (25) | Audit the Frechet-remainder derivation and test a nonlinear two-parameter map with a parameter-dependent, off-diagonal pullback metric across fixed small `tau`. | `release_candidate_space/evidence/claim6/raw_result.json`, checker, and identity-metric control; residual slope `0.9833`, metric minimum eigenvalue `0.2468`, off-diagonal magnitude `0.7283`. | Scoped symbolic derivation and nontrivial continuous audit; not a proof-assistant formalization or neural-training reproduction. **VERIFIED_SCOPED** |

## Evidence ladder

1. The arXiv HTML source is pinned by SHA-256
   `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`.
2. Positive routes preserve a source contract, method, raw result, independent
   checker, and a deliberately invalid control.
3. Finite Gaussian and kernel checks support the reconstructed mechanisms; they
   do not replace measure-theoretic proofs or universal quantifiers.
4. Claim 5 uses complete reported tables, not a downscaled image-training proxy;
   no new H100-scale FID uncertainty estimate is claimed.

The complete path inventory is in [`EVIDENCE_MANIFEST.json`](EVIDENCE_MANIFEST.json).
