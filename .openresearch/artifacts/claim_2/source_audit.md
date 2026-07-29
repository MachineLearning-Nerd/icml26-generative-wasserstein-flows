# Claim 2 source audit

- Source: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- SHA-256: `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Proposition: 3.2
- Proof: Appendix F.2, Equations (119)–(136)

The Moreau functional is

`F_epsilon(mu) = inf_eta W2^2(mu,eta) + epsilon D_f(eta||nu)`.

Lemma F.2 derives

`grad_W2 F_epsilon(mu) = epsilon grad phi^(c_epsilon)`.

The optimal transport map from `mu` to the minimizer `eta-star` is
`Id - (epsilon/2) grad phi`. Therefore the explicit WGD map
`Id - gamma epsilon grad phi` equals that optimal map exactly when
`gamma=1/2`. When `epsilon=2 tau`, `eta-star` also minimizes the JKO
objective because the two objectives differ by the positive scalar `2 tau`.

The old rejected baseline checked only that final scalar identity. It did not
derive or test the Wasserstein gradient or update map.
