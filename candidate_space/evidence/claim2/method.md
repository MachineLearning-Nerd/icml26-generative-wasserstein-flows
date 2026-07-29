# Claim 2 method

1. SymPy verifies that the WGD displacement coefficient `gamma epsilon`
   equals the optimal-map coefficient `epsilon/2` only at `gamma=1/2`.
2. It separately verifies the cost scaling and JKO objective scaling after
   `epsilon=2 tau`.
3. A continuous two-dimensional diagonal-Gaussian checker numerically
   differentiates the optimized Moreau envelope and compares the explicit WGD
   update with its independently optimized minimizer for KL, chi-squared, and
   Jensen–Shannon.
4. Replacing `gamma=1/2` by `0.35` is the negative control and must exit 1.

The fixed cumulative command is `uv run --frozen python run_campaign.py`.
The standalone verifier is `uv run --frozen python verification/claim2_exact.py`.
