# Claim 1 method

The verifier uses three routes:

1. An exact SymPy certificate names the three objective values and checks
   `(A-D) + (D-C) = A-C`. The cited minimax and Monge premises give `A=C`;
   weak duality and the map-subset relation make both left gaps nonnegative,
   so both must be zero.
2. A continuous checker independently solves both orders for three
   two-dimensional anisotropic Gaussian KL cases. Affine maps and quadratic
   optimal critics make both sides closed finite-dimensional formulations.
3. A negative control removes absolute continuity/Monge recovery and supplies
   a countermodel satisfying every remaining order premise while `A != D`.

The fixed cumulative command is `uv run --frozen python run_campaign.py`.
The standalone verifier is `uv run --frozen python verification/claim1_exact.py`.
