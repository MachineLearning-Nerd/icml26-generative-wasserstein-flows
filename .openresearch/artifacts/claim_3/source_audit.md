# Claim 3 source audit

- Source: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- SHA-256: `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Section: 3.1, “Donsker-Varadhan”
- Equation: (11), HTML anchor `S3.E11`

The paper states

`KL(mu||nu) = sup_h [integral h dmu - log integral exp(h) dnu]`

and says this objective is pointwise at least the classical reverse-KL
variational bound

`integral h dmu - integral exp(h - 1) dnu`.

Writing `s = log integral exp(h) dnu`, their difference is
`exp(s - 1) - s`, whose unique global minimum is zero at `s = 1`.
At `h* = 1 + log(dmu/dnu)`, both objectives equal `KL(mu||nu)` whenever
this critic is admissible. If it is not in the bounded critic class, equality is
understood at the level of suprema rather than literal attainment.
