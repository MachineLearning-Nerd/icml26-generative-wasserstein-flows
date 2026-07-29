# Claim 3 — Donsker–Varadhan bound

**Verdict: VERIFIED.** Current verifier:
[`claim3_exact.py`](../../verification/claim3_exact.py) at frozen Git SHA
`361e1508d9f1acf47c65aecdc49dbb1aff15076b`. It supersedes the n=10
random-critic check in the **Historical rejected baseline**.

## Exact claim

For probability measures `mu << nu` and every admissible bounded critic `h`,
the Donsker–Varadhan KL objective is at least the classical reverse-KL
variational objective. Their suprema equal `KL(mu||nu)`. Literal attainment is
claimed only when `1 + log(dmu/dnu)` belongs to the critic class. These are
the audited assumptions for the exact contract.

## Proof certificate

Set `s = log integral exp(h) dnu`. The exact gap is
`exp(s - 1) - s`. Its derivative vanishes only at `s=1`, its second derivative
there is positive, its value there is zero, and both boundary limits are
positive infinity.

The fixed command is:

```bash
uv run --frozen python run_campaign.py
```

Pinned versions are in `pyproject.toml` and `uv.lock`. The run prints the full
symbolic certificate, continuous-Gaussian checker, failure control, Git SHA,
CPU allocation, seeds, and runtime inline.

Successful HF run `94499562-aeea-4d4f-95f4-02dd61e20d6b` exposed 64 logical
CPUs. The verifier was estimated to use one core and took 0.673309 seconds;
the complete job took 26 seconds including environment setup. `cpu-upgrade`
was selected because clean locked-environment setup time was uncertain.
The 60 fixed cases are deterministic and use no random sampling or seeds.

## Observed evidence

| Check | Observed result | Acceptance condition |
| --- | ---: | ---: |
| Exact scalar minimum | `0` at the unique stationary point `s=1` | `>= 0` for every real `s` |
| Continuous off-optimum cases | 60 | all gaps nonnegative |
| Smallest observed DV-classical gap | 0.01783465805601825 | `>= -1e-12` |
| Optimal Gaussian critics | 4 | both objectives equal KL |
| Largest equality error | 8.326672684688674e-17 | `< 1e-12` |

Download the [raw result](../../evidence/claim3/raw_result.json), the
[independent checker output](../../evidence/claim3/checker_output.json), and
the [negative-control output](../../evidence/claim3/negative_control_output.json).

## Negative control

The reversed statement `classical(h) >= DV(h)` is evaluated at `s=0`; it must
exit nonzero because `DV-classical = exp(-1) > 0`. It returned exit code 1
with gap `0.36787944117144233`.

## Source and environment

The source is Section 3, Equation (11), retrieved from
`https://ar5iv.labs.arxiv.org/html/2605.31369` at
`2026-07-29T11:22:44Z`, SHA-256
`9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`.
See the [exact claim contract](../../evidence/claim3/claim_contract.json),
[source audit](../../evidence/claim3/source_audit.md),
[method](../../evidence/claim3/method.md), and
[pinned environment](../../evidence/environment/pyproject.toml). The complete
lock is the repository's
[`uv.lock`](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/blob/361e1508d9f1acf47c65aecdc49dbb1aff15076b/uv.lock)
at the frozen verification revision.

## Limitation

SymPy certifies the scalar inequality exactly. The substitution lifting it to
arbitrary probability measures is an independently reconstructed analytic
derivation, not a formal proof-assistant development of measure theory.
