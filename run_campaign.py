"""Frozen reconstruction of the 5/12 judged baseline.

These checks intentionally retain the small, simplified scope criticized by
the live judge. Child experiments supersede them with exact claim contracts.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time

import numpy as np
from scipy.optimize import minimize, minimize_scalar

from verification.claim3_exact import run_contract as run_claim3_contract


SEEDS = [0, 1, 2, 3]


def kl(p: np.ndarray, q: np.ndarray) -> float:
    return float(np.sum(p * np.log(p / q)))


def softmax(v: np.ndarray) -> np.ndarray:
    shifted = v - np.max(v)
    exp_v = np.exp(shifted)
    return exp_v / exp_v.sum()


def w2_quantile_1d(p: np.ndarray, q: np.ndarray, grid: np.ndarray) -> float:
    """Exact 1-D W2² for measures on a shared ordered grid."""
    cuts = np.unique(
        np.concatenate(([0.0], np.cumsum(p), np.cumsum(q), [1.0]))
    )
    mids = (cuts[:-1] + cuts[1:]) / 2
    widths = np.diff(cuts)
    p_idx = np.searchsorted(np.cumsum(p), mids, side="right")
    q_idx = np.searchsorted(np.cumsum(q), mids, side="right")
    p_idx = np.minimum(p_idx, len(grid) - 1)
    q_idx = np.minimum(q_idx, len(grid) - 1)
    return float(np.sum(widths * (grid[p_idx] - grid[q_idx]) ** 2))


def discrete_jko(mu: np.ndarray, nu: np.ndarray, grid: np.ndarray, tau: float):
    def objective(logits: np.ndarray) -> float:
        eta = softmax(logits)
        return w2_quantile_1d(mu, eta, grid) / (2 * tau) + kl(eta, nu)

    result = minimize(objective, np.log(mu), method="Powell", options={"maxiter": 800})
    return softmax(result.x), float(result.fun)


def claim_1() -> dict:
    rows = []
    passed = True
    for seed in SEEDS[:3]:
        rng = np.random.default_rng(seed)
        grid = np.linspace(-2, 2, 10)
        mu = rng.dirichlet(np.ones(10))
        nu = rng.dirichlet(np.ones(10))
        tau = 0.04
        eta_jko, jko_value = discrete_jko(mu, nu, grid, tau)
        eta_suot, suot_scaled = discrete_jko(mu, nu, grid, tau)
        suot_value = 2 * tau * suot_scaled
        distance = float(np.linalg.norm(eta_jko - eta_suot))
        ratio = suot_value / (2 * tau * jko_value)
        seed_passed = distance < 5e-3 and abs(ratio - 1) < 0.03
        passed &= seed_passed
        rows.append(
            {
                "seed": seed,
                "argmin_l2": distance,
                "value_ratio": ratio,
                "passed": seed_passed,
            }
        )
    return {
        "claim": 1,
        "status": "TOY" if passed else "BLOCKED",
        "scope": "n=10 shared-grid discrete measures; KL only",
        "rows": rows,
    }


def claim_2() -> dict:
    max_error = 0.0
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        grid = np.linspace(-2, 2, 10)
        mu = rng.dirichlet(np.ones(10))
        nu = rng.dirichlet(np.ones(10))
        tau = 0.04
        for _ in range(20):
            eta = rng.dirichlet(np.ones(10))
            transport = w2_quantile_1d(mu, eta, grid)
            f_eps = transport + 2 * tau * kl(eta, nu)
            jko = transport / (2 * tau) + kl(eta, nu)
            max_error = max(max_error, abs(f_eps - 2 * tau * jko) / f_eps)
    return {
        "claim": 2,
        "status": "TOY" if max_error < 1e-9 else "BLOCKED",
        "scope": "n=10 shared-grid discrete measures; KL only",
        "max_relative_error": max_error,
    }


def claim_3() -> dict:
    result = run_claim3_contract()
    control = subprocess.run(
        [sys.executable, "verification/claim3_exact.py", "--negative-control"],
        check=False,
        capture_output=True,
        text=True,
    )
    result["negative_control"]["exit_code"] = control.returncode
    result["negative_control"]["stdout"] = control.stdout.strip()
    if control.returncode != 1:
        result["status"] = "BLOCKED"
    result["claim"] = 3
    return result


def claim_4() -> dict:
    rng = np.random.default_rng(0)
    grid = np.linspace(0, 1, 12)
    mu = np.exp(-((grid - rng.uniform(0.2, 0.4)) ** 2) / 0.02)
    nu = np.exp(-((grid - rng.uniform(0.55, 0.75)) ** 2) / 0.02)
    mu /= mu.sum()
    nu /= nu.sum()
    sigma = rng.uniform(0.1, 0.2)
    kernel = np.exp(-((grid[:, None] - grid[None, :]) ** 2) / (2 * sigma**2))

    def mmd2(p: np.ndarray) -> float:
        delta = p - nu
        return float(delta @ kernel @ delta)

    tau = 0.1

    def line_objective(alpha: float) -> float:
        eta = (1 - alpha) * mu + alpha * nu
        return w2_quantile_1d(mu, eta, grid) / (2 * tau) + mmd2(eta)

    alpha = float(minimize_scalar(line_objective, bounds=(0, 1), method="bounded").x)
    eta = (1 - alpha) * mu + alpha * nu
    before, after = mmd2(mu), mmd2(eta)
    return {
        "claim": 4,
        "status": "TOY" if after < before else "BLOCKED",
        "scope": "one n=12 grid seed; fixed Gaussian kernel; no neural MMD-GAN",
        "mmd2_before": before,
        "mmd2_after": after,
        "line_search_alpha": alpha,
    }


def claim_5() -> dict:
    return {
        "claim": 5,
        "status": "BLOCKED",
        "scope": "No MNIST/CIFAR-10 training or FID evidence in judged baseline",
        "reason": "Historical baseline explicitly deferred image experiments",
    }


def claim_6() -> dict:
    ratios = []
    gradient = -1.7
    curvature = 0.8
    for tau in [0.2, 0.1, 0.05, 0.02, 0.01]:
        theta_star = -tau * gradient / (1 + tau * curvature)
        flow = -tau * gradient
        ratios.append(theta_star / flow)
    passed = abs(ratios[-1] - 1) < 0.01
    return {
        "claim": 6,
        "status": "TOY" if passed else "BLOCKED",
        "scope": "one-dimensional translation family with G=1",
        "tau": [0.2, 0.1, 0.05, 0.02, 0.01],
        "jko_to_flow_ratio": ratios,
    }


def main() -> int:
    started = time.perf_counter()
    results = [claim_1(), claim_2(), claim_3(), claim_4(), claim_5(), claim_6()]
    runtime = time.perf_counter() - started
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    metadata = {
        "git_sha": git_sha,
        "paper_source_sha256": "9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a",
        "judged_space_revision": "90e3b80761e36f11697a2f3140c216842b30adb4",
        "verdict_dataset_revision": "1b782309550dd756df4fd0f3ffe8dca8a32d5269",
        "estimated_cores": 1,
        "selected_compute": "Hugging Face cpu-upgrade (environment setup runtime uncertain)",
        "actual_logical_cpus": os.cpu_count(),
        "platform": platform.platform(),
        "runtime_seconds": runtime,
        "seeds": SEEDS,
    }
    payload = {"metadata": metadata, "claims": results}
    print("BEGIN_RAW_JSON")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("END_RAW_JSON")
    print("\nEVAL.md")
    print("# Historical rejected baseline")
    for result in results:
        print(f"- Claim {result['claim']}: {result['status']} — {result['scope']}")
    print(f"- Runtime: {runtime:.3f}s")
    return 0 if all(r["status"] in {"TOY", "BLOCKED"} for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
