# Claim 4 source audit

- Paper: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- HTML SHA-256:
  `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Anchors: Section 4, Equations (15)-(18); Appendix D.4, Equations
  (106)-(108), Algorithm 2
- Authors' code revision:
  `6633b553a244634bd2c2e1142603aad1c1fbe55a`

The imported claim conflates two different algorithms. For a fixed kernel,
Algorithm 1 has a closed-form squared-MMD witness and the paper explicitly
says that this fixed-kernel scheme is non-adversarial. Equation (18), however,
introduces an adaptive kernel:

`max_phi min_T 1/2 ||Id-T||² + MMD²_{k_phi}(T#mu_l,nu)`.

The paper then says this problem is solved adversarially. Appendix D.4 gives
`phi* in argmax_phi 1/2 MMD²_{k_phi}` and Algorithm 2 performs a positive
gradient update in `phi`. The authors' documented MMD+JKO command uses the
training loop that calls `optimizerD.step()`; `D_steps` defaults to one.

Thus “no explicit discriminator optimization” applies to Algorithm 1, not to
the Equation-18 JKO MMD-GAN named by the imported claim.
