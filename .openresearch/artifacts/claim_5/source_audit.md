# Claim 5 source audit

- Paper: `https://ar5iv.labs.arxiv.org/html/2605.31369`
- Retrieved: `2026-07-29T11:22:44Z`
- HTML SHA-256:
  `9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`
- Section 5.3: “GWF for Various Divergences”
- Authors' code:
  `https://github.com/Paulcauch/Generative_Wasserstein_Flows`
- Authors' code revision:
  `6633b553a244634bd2c2e1142603aad1c1fbe55a`

Section 5.3 names KL, Jensen–Shannon, and chi-squared as the
f-divergences and asserts “moderate yet consistent improvements.” It compares
no JKO with every step size in `{0.01, 1, 100}` on CIFAR-10, using Small-Net
and the same number of generator updates.

The complete reported table contradicts the universal consistency word:

| Divergence | no JKO | JKO 0.01 | JKO 1 | JKO 100 |
| --- | ---: | ---: | ---: | ---: |
| chi-squared | 15.60 | 22.26 | **15.01** | 15.87 |
| KL | 15.78 | 26.94 | **15.47** | 17.28 |
| Jensen–Shannon (`Shannon`) | **14.60** | 32.24 | 15.92 | 15.23 |

Lower FID is better. The best Jensen–Shannon JKO mean is 15.23, which is
0.63 worse than 14.60 without JKO. The appendix says its complementary table
uses different random seeds; that table again has no-JKO 16.84 and best-JKO
16.87, 0.03 worse.

The authors' README maps the human-facing Jensen–Shannon divergence to the
`Shannon` CLI label, and `losses.py` implements that label with the softplus
GAN loss.
