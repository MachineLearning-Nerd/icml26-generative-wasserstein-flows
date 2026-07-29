# Claim 2 source audit

- Source: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- SHA-256: `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Proposition: 3.2
- Proof: Appendix F.2, Equations (119)–(136)

Lemma F.2 derives
`grad_W2 F_epsilon(mu) = epsilon grad phi^(c_epsilon)`. The optimal map
to the envelope minimizer is `Id-(epsilon/2) grad phi`, so the explicit WGD
map equals it at `gamma=1/2`. With `epsilon=2 tau`, the envelope minimizer
is also the JKO minimizer.

The historical rejected baseline checked only the final scalar rescaling; it
did not derive or test the gradient or update map.
