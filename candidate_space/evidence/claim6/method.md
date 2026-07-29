# Claim 6 method

The symbolic certificate reconstructs the general proof:

1. Differentiate the exact JKO objective.
2. Substitute the endpoint Frechet expansion
   `F_plus-F_old=J_plus Delta+r`.
3. Identify `integral J_plus^T J_plus dmu` as `G(theta_plus)`.
4. Bound `integral J_plus^T r dmu` by Cauchy-Schwarz.
5. Substitute `||Delta||=O(tau)` and verify that the divided remainder is
   a bounded increment factor times a vanishing remainder ratio.

The independent checker uses `mu=N(0,I2)` and the invertible nonlinear
translation

`F_(a,b)(z)=z+(a+0.35ab, 0.45a+b+0.15a²)`.

Its metric `G=J^T J` is positive definite, parameter-dependent, and
off-diagonal. Seven independently selected step sizes from `0.2` to `0.002`
measure both the theorem residual and convergence to the preconditioned flow.

The negative control replaces `G` by `I`; it must exit 1.

Fixed cumulative command: `uv run --frozen python run_campaign.py`.
