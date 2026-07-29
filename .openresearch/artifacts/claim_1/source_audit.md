# Claim 1 source audit

- Source: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- SHA-256: `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Proposition: 3.1
- Main anchors: Equations (6) and (9)
- Proof anchors: Appendix F.1, Equations (109)–(118)

The paper assumes `mu_l, nu in P_ac,2(R^d)` and states equality of the
unrestricted VWGF and S-JKO objective values. After the sign change `h -> -h`,
both use

`L(T,h) = integral [||T-Id||^2/(2 tau) + h(T)] dmu - integral f*(h) dnu`.

Appendix F.1 lifts deterministic maps to couplings with first marginal `mu`,
uses convexity in the coupling and concavity in the critic to exchange
infimum and supremum, and recovers an optimal Monge map from absolute
continuity. Weak duality and the fact that map-induced couplings form a subset
then close the reverse inequality.

The statement concerns the mathematical objectives. Finite neural-network
parameterizations need not preserve the equality.
