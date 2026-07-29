# Claim 3 method

`verify.py` uses three independent checks:

1. SymPy reconstructs the exact scalar gap, finds its only stationary point,
   evaluates its second derivative and boundary limits, and certifies a global
   minimum of zero.
2. A closed-form continuous Gaussian checker evaluates 60 affine critics for
   four distinct absolutely continuous measure pairs, then checks the exact
   optimal critic for each pair.
3. A negative control reverses the inequality and must exit nonzero.

The fixed cumulative command is `uv run --frozen python run_campaign.py`.
The standalone verifier is `uv run --frozen python verify.py`.
