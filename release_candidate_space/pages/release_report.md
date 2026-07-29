# Final release forecast and evidence report

- Previous live judged score: `5/12`
- Conservative projected score range after the proposed change: **9–12/12**
- Best-supported possible new score: **12/12 forecast, not a judge result**

The current live score remains **5/12**. Only the live evaluator can change it.
No claim is BLOCKED under the six audited contracts.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | VERIFIED | Exact minimax-order certificate plus continuous 2-D Gaussian agreement to `4.44e-14`; residual risk is that the measure-theoretic premises are audited rather than proof-assistant formalized. |
| 2 | 1 | 2 | HIGH | VERIFIED | Unique coefficient match `gamma=1/2`, `epsilon=2 tau`; KL, χ², and JS updates agree within `1.25e-8`; Lemma F.2 remains an audited premise. |
| 3 | 1 | 2 | HIGH | VERIFIED | Universal scalar DV-gap certificate plus 60 continuous cases and equality error `8.33e-17`; the measure-theory lift is independently derived, not Lean/Coq. |
| 4 | 1 | 2 | MEDIUM | FALSIFIED | Equation 18, Appendix D.4, Algorithm 2, authors' code, and a complete PSD-kernel counterexample require `phi` optimization. Risk: the evaluator may separate the imported no-discriminator wording from Equation 18. |
| 5 | 0 | 2 | MEDIUM | FALSIFIED | The complete primary and different-seed CIFAR tables contradict “consistent” Jensen–Shannon gains by `+0.63` and `+0.03` FID. Risk: no H100 rerun or seed-level uncertainty is available. |
| 6 | 1 | 2 | HIGH | VERIFIED | General Frechet-remainder certificate and a nonlinear off-diagonal pullback metric converge at slope `0.983`; the certificate is not proof-assistant formalized. |

## What changed

All six claim surfaces changed since the previous judge result. Claims 1–3 and
6 replace toy proxies with exact contracts, proof certificates, continuous
checkers, and controls. Claim 4 isolates and falsifies only the
no-discriminator conjunct attached to Equation 18. Claim 5 replaces the
deferred experiment with an exhaustive falsification of the paper's exact
reported-table consistency quantifier.

The exact judged Space revision
`90e3b80761e36f11697a2f3140c216842b30adb4` remains immutable evidence.
All 13 judged files are preserved byte-for-byte either at their original path
or under `historical/judged-90e3b80761e36f11697a2f3140c216842b30adb4/`.

## Winning experiment and regression

The winning scientific/release branch is
`orx/release-candidate-report-and-logbook` at Git SHA
`e6898b5bbc35403b61d4657609c0e87cde3ce567`.

HF run `a892db82-b9dc-44b0-8baa-96a6ac894607` used `cpu-upgrade`, exposed
64 logical CPUs, and completed in 37 seconds including setup. The cumulative
verifier estimated one active core and ran in 4.787447811802849 seconds. Its
log reports Claims 1/2/3/6 VERIFIED, Claims 4/5 FALSIFIED, and every negative
control exiting 1.

The stacked tree froze the historical baseline, then descended through exact
Claim 3, exhaustive Claim 5 tables, exact Claim 1, exact Claim 2, the Claim 4
counterexample, the nontrivial Claim 6 metric, evaluator-visible bundles, and
this release regression.

## Compute and cost

No GPU was used. Long or uncertain work used HF `cpu-upgrade`; local work was
restricted to short, one-core inspection, plotting, manifest, notebook, and
audit tasks. Through the release regression, 17 managed jobs occupied 551
seconds of recorded duration. At the published `$0.0005/min` flavor rate,
the nominal time-proportional amount is about `$0.0046`; provider
minute-accounting can differ.

## Reproduction and release commands

Every experiment inherited the exact command:

```bash
uv run --frozen python run_campaign.py
```

The managed release regression was launched and read with:

```bash
orx exp run 5799581c-28d1-4603-8481-feb507a62558 --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.11-bookworm-slim --timeout 20m
orx exp wait 5799581c-28d1-4603-8481-feb507a62558 --timeout 480
orx logs a892db82-b9dc-44b0-8baa-96a6ac894607 --bytes 200000
```

The evaluator-visible artifact was built and reviewed with:

```bash
uv run --frozen python scripts/build_release_candidate.py --judged-dir /tmp/gwf-space-judged.aVUctt --output release_candidate_space
uv run --frozen python scripts/audit_candidate.py /tmp/gwf-redteam-pass1 --record reports/gwf_reproduction/red_team_pass1.json
uv run --frozen python scripts/audit_candidate.py /tmp/gwf-redteam-pass2 --record reports/gwf_reproduction/red_team_pass2.json
uv run --frozen python scripts/audit_candidate.py /tmp/gwf-redteam-pass3 --record reports/gwf_reproduction/red_team_pass3.json
uv tool run --from marimo==0.23.1 marimo check --strict notebooks/gwf_reproduction.py
uv run --frozen marimo export html notebooks/gwf_reproduction.py -o /tmp/gwf-notebook.html
```

The startup and source-integrity commands included:

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 10c2005e-f679-4dc2-8f25-a752bf29ad90
curl -L -A "OpenResearch-Reproduction/1.0" https://ar5iv.labs.arxiv.org/html/2605.31369
```

The paper HTML was retrieved at `2026-07-29T11:22:44Z` with SHA-256
`9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`.
The verdict dataset revision was
`1b782309550dd756df4fd0f3ffe8dca8a32d5269`, filtered exactly by
`space_id == "DineshAI/sJ7ngz2eQx"`.

## Evidence paths and publication action

Canonical pages are under `pages/claims/`; raw evidence is under
`evidence/claim1/` through `evidence/claim6/`; current verifier sources are
under `verification/`; manifests and the exact text upload allowlist are under
`manifests/`; the blind-review record is under `evidence/release/`.

After the final package regression and a new fresh-copy traversal pass, the
exact publication action is one text-only Hugging Face API commit to the
existing `DineshAI/sJ7ngz2eQx` Space using
`manifests/text_upload_allowlist.txt`. No second Space will be created.
The published text mirror, illustrated report, notebook, and README landing
page will then be fast-forwarded to GitHub `main`, and the remote SHA verified
with `git ls-remote`.
