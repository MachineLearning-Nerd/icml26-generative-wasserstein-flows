# Source audit entry point

## Primary source

- Paper: *A Unifying View of Variational Generative Wasserstein Flows*
- Authors: Paul Caucheteux, Clément Bonet, and Anna Korba
- arXiv: [2605.31369](https://arxiv.org/abs/2605.31369)
- HTML source: <https://arxiv.org/html/2605.31369>
- Retrieved: `2026-07-29T11:22:44Z`
- HTML SHA-256: `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- ICML submission identifier: `sJ7ngz2eQx`

## Version and claim mapping

The current pages use the paper’s displayed anchors: Proposition 3.1 for the
VWGF/S-JKO objective equivalence, Proposition 3.2 and Lemma F.2 for the
explicit Wasserstein/JKO update, Section 3 Equation (11) for the DV bound,
Equation (18) and Appendix D.4/Algorithm 2 for the discriminator requirement,
Section 5.3 for the reported FID consistency wording, and Proposition 6.3 for
the parametric JKO limit.

The historical judged Space revision is preserved in the release candidate and
its paths are listed by [`release_candidate_space/logbook.json`](release_candidate_space/logbook.json).

## Fidelity boundary

Claims 1–3 and 6 are scoped audits of mathematical contracts and deterministic
continuous cases. Claim 4 is a source-aware falsification of one conjunct and
does not generalize to all MMD-GAN or JKO schemes. Claim 5 is a complete-table
falsification of a universal word, not a claim that all JKO settings worsen FID.
The image-scale experiments were not independently rerun at H100 scale.
