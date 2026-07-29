"""Generate the evidence figures used by the public reproduction report."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path("reports/gwf_reproduction/images")
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"figure.dpi": 160, "font.size": 10})


def save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(OUT / name, bbox_inches="tight")
    plt.close()


divergences = ["χ²", "KL", "Jensen–Shannon"]
no_jko = np.array([15.60, 15.78, 14.60])
best_jko = np.array([15.01, 15.47, 15.23])
x = np.arange(3)
plt.figure(figsize=(7.2, 3.8))
plt.bar(x - 0.18, no_jko, 0.36, label="No JKO", color="#5b6b7a")
plt.bar(x + 0.18, best_jko, 0.36, label="Best reported JKO", color="#d97706")
for i, (base, jko) in enumerate(zip(no_jko, best_jko)):
    delta = jko - base
    plt.text(i + 0.18, jko + 0.12, f"{delta:+.2f}", ha="center", fontsize=9)
plt.xticks(x, divergences)
plt.ylabel("CIFAR-10 FID (lower is better)")
plt.ylim(13.8, 16.5)
plt.legend(frameon=False, ncol=2)
plt.title("The paper table contradicts “consistent” f-divergence gains")
save("headline-fid-comparison.png")


labels = ["Prop 3.1\nobjective gap", "Prop 3.2\nupdate error", "DV\noptimality error"]
values = [4.440892098500626e-14, 1.25478003840223e-8, 8.326672684688674e-17]
plt.figure(figsize=(7.2, 3.6))
bars = plt.barh(labels, values, color=["#2563eb", "#2563eb", "#2563eb"])
plt.xscale("log")
plt.xlabel("Maximum absolute numerical discrepancy (log scale)")
plt.title("Independent continuous checks agree with the exact certificates")
for bar, value in zip(bars, values):
    plt.text(value * 1.25, bar.get_y() + bar.get_height() / 2, f"{value:.2e}", va="center")
plt.xlim(1e-18, 1e-6)
save("theorem-checker-precision.png")


c2_names = ["KL", "χ²", "Jensen–Shannon"]
c2_good = np.array([1.0788853172293131e-8, 1.25478003840223e-8, 1.0209852851746701e-8])
c2_bad = np.array([0.08637744731196349, 0.04716379310938425, 0.023735902823184135])
x = np.arange(3)
plt.figure(figsize=(7.2, 3.7))
plt.semilogy(x, c2_good, "o-", label="γ=1/2 (paper)")
plt.semilogy(x, c2_bad, "s--", label="γ=0.35 control")
plt.xticks(x, c2_names)
plt.ylabel("Distance to independently optimized JKO update")
plt.title("Claim 2: the exact parameter relation matters")
plt.legend(frameon=False)
plt.grid(axis="y", alpha=0.25)
save("claim2-parameter-control.png")


plt.figure(figsize=(7.2, 3.6))
ax = plt.gca()
ax.axis("off")
ax.text(
    0.22,
    0.65,
    "Algorithm 1\nfixed kernel\nclosed-form witness",
    ha="center",
    va="center",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "#dbeafe", "edgecolor": "#2563eb"},
)
ax.text(
    0.78,
    0.65,
    "Equation 18 / Algorithm 2\nlearned kφ\nmaxφ minT",
    ha="center",
    va="center",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "#ffedd5", "edgecolor": "#d97706"},
)
ax.annotate("", xy=(0.58, 0.65), xytext=(0.42, 0.65), arrowprops={"arrowstyle": "->"})
ax.text(0.5, 0.77, "adaptive embedding", ha="center")
ax.text(0.22, 0.30, "No adversarial optimization", ha="center", weight="bold")
ax.text(0.78, 0.30, "Explicit φ / discriminator update", ha="center", weight="bold")
ax.text(0.5, 0.08, "The imported Claim 4 conflated these two schemes.", ha="center")
plt.title("Claim 4: the no-discriminator statement belongs to Algorithm 1")
save("claim4-scheme-distinction.png")


tau = np.array([0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002])
residual = np.array([0.0817876, 0.0494143, 0.0273758, 0.0116775, 0.00596798, 0.00301710, 0.00121489])
velocity = np.array([0.660115, 0.391497, 0.216592, 0.0927068, 0.0474786, 0.0240328, 0.00968520])
identity = np.array([1.15339, 1.42393, 1.60769, 1.74090, 1.79010, 1.81572, 1.83143])
plt.figure(figsize=(7.2, 4.1))
plt.loglog(tau, residual, "o-", label="Proposition 6.3 residual (slope 0.983)")
plt.loglog(tau, velocity, "s-", label="Velocity error (slope 0.982)")
plt.loglog(tau, identity, "x--", label="Identity-metric control")
plt.gca().invert_xaxis()
plt.xlabel("τ → 0")
plt.ylabel("Error / residual")
plt.title("Non-identity off-diagonal metric recovers the preconditioned flow")
plt.grid(which="both", alpha=0.25)
plt.legend(frameon=False)
save("claim6-preconditioned-convergence.png")
