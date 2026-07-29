# Claim 6 source audit

- Paper: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- HTML SHA-256:
  `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Anchors: Proposition 6.3, Equations (25)-(26); Appendix G.3,
  Proposition G.4, Equations (209)-(217)

The exact conclusion is

`G(theta_plus)(theta_plus-theta_old)/tau =
 -grad_theta F(mu_theta_plus) + o(1)`.

It is asymptotic as `tau -> 0`, conditional on L2 Frechet
differentiability of the parametrization, a square-integrable Jacobian,
differentiability of the energy, and an `O(tau)` parameter increment.
Invertibility of `G` is additionally needed to rewrite the conclusion as the
`G^-1`-preconditioned flow.

The proof linearizes `F_theta_plus-F_theta_old` at `theta_plus`. The
Jacobian-remainder term is `o(||Delta||)` by Cauchy-Schwarz. Dividing by
`tau` gives `o(1)` precisely because `||Delta||=O(tau)`.
