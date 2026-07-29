# Current verification

The current evidence supersedes the historical rejected baseline. Start here:

| Claim | Current page | Current status |
| --- | --- | --- |
| 1 | [VWGF equals S-JKO](claims/claim1.md) | **VERIFIED** |
| 2 | [Explicit WGD equals JKO](claims/claim2.md) | **VERIFIED** |
| 3 | [Donsker–Varadhan exact bound](claims/claim3.md) | **VERIFIED** |
| 4 | [Equation 18 discriminator requirement](claims/claim4.md) | **FALSIFIED** |
| 5 | [Reported FID consistency](claims/claim5.md) | **FALSIFIED** |
| 6 | [Parametric JKO and preconditioned flow](claims/claim6.md) | **VERIFIED** |

See the [evaluator-visible evidence matrix](visibility_matrix.md) and the
[evaluator-blind red-team review](../evidence/release/red_team_review.md).
Scientific rows are complete.

Historical judged pages will be preserved additively in the release candidate.

## Reproduce all current checks

```bash
uv run --frozen python run_campaign.py
```

The candidate includes the [cumulative verifier](../run_campaign.py), the
[pinned project](../pyproject.toml), [complete lockfile](../uv.lock), and
[Python version](../.python-version). Every claim page links its standalone
verifier, raw result, checker output, and failing control.
