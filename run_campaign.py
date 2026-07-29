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
from scipy.optimize import minimize

from verification.claim1_exact import run_contract as run_claim1_contract
from verification.claim2_exact import run_contract as run_claim2_contract
from verification.claim3_exact import run_contract as run_claim3_contract
from verification.claim4_eq18_falsification import (
    run_contract as run_claim4_contract,
)
from verification.claim5_source_falsification import (
    run_contract as run_claim5_contract,
)


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
    result = run_claim1_contract()
    control = subprocess.run(
        [sys.executable, "verification/claim1_exact.py", "--negative-control"],
        check=False,
        capture_output=True,
        text=True,
    )
    result["negative_control"]["exit_code"] = control.returncode
    result["negative_control"]["stdout"] = control.stdout.strip()
    if control.returncode != 1:
        result["status"] = "BLOCKED"
    result["claim"] = 1
    return result


def claim_2() -> dict:
    result = run_claim2_contract()
    control = subprocess.run(
        [sys.executable, "verification/claim2_exact.py", "--negative-control"],
        check=False,
        capture_output=True,
        text=True,
    )
    result["negative_control"]["exit_code"] = control.returncode
    result["negative_control"]["stdout"] = control.stdout.strip()
    if control.returncode != 1:
        result["status"] = "BLOCKED"
    result["claim"] = 2
    return result


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
    result = run_claim4_contract()
    control = subprocess.run(
        [
            sys.executable,
            "verification/claim4_eq18_falsification.py",
            "--negative-control",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    result["negative_control"] = {
        "exit_code": control.returncode,
        "stdout": control.stdout.strip(),
    }
    if control.returncode != 1:
        result["status"] = "BLOCKED"
    result["claim"] = 4
    return result


def claim_5() -> dict:
    result = run_claim5_contract()
    control = subprocess.run(
        [
            sys.executable,
            "verification/claim5_source_falsification.py",
            "--negative-control",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    result["negative_control"] = {
        "exit_code": control.returncode,
        "stdout": control.stdout.strip(),
    }
    if control.returncode != 1:
        result["status"] = "BLOCKED"
    result["claim"] = 5
    return result


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
    allowed_statuses = {"VERIFIED", "FALSIFIED", "TOY", "BLOCKED"}
    return 0 if all(r["status"] in allowed_statuses for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
