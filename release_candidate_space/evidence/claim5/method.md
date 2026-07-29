# Claim 5 method

The verifier evaluates every named f-divergence and every reported step size;
the Jensen–Shannon row was not selected in advance as the only tested row.

1. Hash and parse the complete primary table.
2. For each named f-divergence, select the minimum reported JKO mean FID
   independently of the prose claim.
3. Compare that minimum with the matched no-JKO mean.
4. Repeat on the paper's explicitly different-seed table.
5. Drop the contradicting row as a negative control; the completeness gate
   must reject the incomplete table with exit code 1.

The fixed cumulative command is `uv run --frozen python run_campaign.py`.
The standalone command is
`uv run --frozen python verification/claim5_source_falsification.py`.
