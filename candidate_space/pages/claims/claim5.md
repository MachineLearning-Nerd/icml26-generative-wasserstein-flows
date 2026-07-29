# Claim 5 — reported FID consistency

**Verdict: FALSIFIED for the exact consistency quantifier.** This is a narrow
source-table counterexample, not a CPU downscaling of the authors' H100 image
training.

## Exact claim tested

Section 5.3 names KL, Jensen–Shannon, and chi-squared and states that JKO gives
“moderate yet consistent improvements” for f-divergences. The machine contract
therefore asks whether, for **every** named f-divergence, at least one of the
complete reported JKO step sizes `{0.01, 1, 100}` lowers mean CIFAR-10 FID
relative to the matched no-JKO baseline.

See the [machine-readable contract](../../evidence/claim5/claim_contract.json)
and [source audit](../../evidence/claim5/source_audit.md).

## Complete reported comparison

Lower FID is better.

| Divergence | no JKO | JKO 0.01 | JKO 1 | JKO 100 | Best result |
| --- | ---: | ---: | ---: | ---: | --- |
| chi-squared | 15.60 | 22.26 | **15.01** | 15.87 | JKO improves by 0.59 |
| KL | 15.78 | 26.94 | **15.47** | 17.28 | JKO improves by 0.31 |
| Jensen–Shannon (`Shannon`) | **14.60** | 32.24 | 15.92 | 15.23 | JKO is worse by 0.63 |

The complete [paper table CSV](../../evidence/claim5/table4.csv) contradicts
the universal word “consistent.” The paper's complementary table explicitly
uses different random seeds and repeats the counterexample: no-JKO 16.84
versus best-JKO 16.87, 0.03 worse. Download the
[different-seed CSV](../../evidence/claim5/different_seeds.csv).

## Reproducible evidence

The fixed command was:

```bash
uv run --frozen python run_campaign.py
```

Successful HF run `a915c7f0-113b-4a29-ab7d-301f2d9c72fa` used frozen Git SHA
`3e951a4fba16e722ad64fe751f343d529ebdb74a`. It was estimated at one core,
ran on `cpu-upgrade`, exposed 64 logical CPUs, took 0.721391 seconds in the
verifier, and 21 seconds including setup.

The [verifier source](https://github.com/MachineLearning-Nerd/icml26-repro-sJ7ngz2eQx-a-unifying-view-of-variational-generative-wasserstein-flows/blob/3e951a4fba16e722ad64fe751f343d529ebdb74a/verification/claim5_source_falsification.py)
hash-checks and exhaustively evaluates the table. Download the
[raw result](../../evidence/claim5/raw_result.json) and
[independent checker output](../../evidence/claim5/checker_output.json).

## Negative control

The control drops the contradicting Jensen–Shannon row. The completeness gate
detects the missing required divergence and exits 1. See the
[control output](../../evidence/claim5/negative_control_output.json).

## Limitation

This does not rerun the single-H100 image experiments, and it does not deny
that selected JKO settings improve KL, chi-squared, or MMD. It falsifies only
the exact conjunct asserting consistency across all named f-divergences. See
the full [limitations](../../evidence/claim5/limitations.md).
