# Claim 5 source audit

- Paper: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- HTML SHA-256:
  `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Section 5.3: “GWF for Various Divergences”
- Authors' code revision:
  `6633b553a244634bd2c2e1142603aad1c1fbe55a`

Section 5.3 names KL, Jensen–Shannon, and chi-squared as the
f-divergences and asserts “moderate yet consistent improvements.” It compares
no JKO with every step size in `{0.01, 1, 100}` on CIFAR-10, using Small-Net
and the same number of generator updates.

The authors' README maps Jensen–Shannon to the `Shannon` CLI label, and
`losses.py` implements it with the softplus GAN loss.
