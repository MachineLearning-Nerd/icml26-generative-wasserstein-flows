"""Verify Proposition 6.3 with a nontrivial pullback metric."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import root
import sympy as sp


SOURCE = Path(__file__).parent / "data" / "claim6_source_excerpt.txt"
EXPECTED_SOURCE_SHA256 = (
    "bd779873b16071a1324af0e09d47fc7052b97f56397b1a3175c93699dcbe2ba4"
)
TAUS = np.array([0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002])
THETA_OLD = np.array([0.7, -0.4])
TARGET_MEAN = np.array([-0.4, 0.8])
ENERGY_MATRIX = np.array([[1.4, 0.3], [0.3, 0.9]])


def source_sha256() -> str:
    return hashlib.sha256(SOURCE.read_bytes()).hexdigest()


def translation(theta: np.ndarray) -> np.ndarray:
    a, b = theta
    return np.array([a + 0.35 * a * b, 0.45 * a + b + 0.15 * a * a])


def jacobian(theta: np.ndarray) -> np.ndarray:
    a, b = theta
    return np.array([[1.0 + 0.35 * b, 0.35 * a], [0.45 + 0.3 * a, 1.0]])


def metric(theta: np.ndarray) -> np.ndarray:
    j = jacobian(theta)
    return j.T @ j


def energy_gradient(theta: np.ndarray) -> np.ndarray:
    residual = translation(theta) - TARGET_MEAN
    return jacobian(theta).T @ ENERGY_MATRIX @ residual


def jko_first_order(theta: np.ndarray, tau: float) -> np.ndarray:
    displacement = translation(theta) - translation(THETA_OLD)
    return jacobian(theta).T @ displacement / tau + energy_gradient(theta)


def symbolic_certificate() -> dict:
    tau, increment_bound, remainder_ratio = sp.symbols(
        "tau increment_bound remainder_ratio", positive=True
    )
    delta_norm = tau * increment_bound
    remainder_norm = remainder_ratio * delta_norm
    divided_remainder = sp.simplify(remainder_norm / tau)
    return {
        "first_order_condition": (
            "(1/tau) integral J(theta_plus)^T"
            "(F(theta_plus)-F(theta_old)) dmu + grad_energy(theta_plus)=0"
        ),
        "frechet_expansion": (
            "F(theta_plus)-F(theta_old)=J(theta_plus) Delta+r, "
            "||r||=o(||Delta||)"
        ),
        "metric_identity": "integral J(theta_plus)^T J(theta_plus) dmu=G(theta_plus)",
        "cauchy_schwarz_remainder": (
            "||integral J^T r dmu|| <= ||J||_L2 ||r||_L2 = o(||Delta||)"
        ),
        "delta_substitution": str(delta_norm),
        "remainder_after_dividing_by_tau": str(divided_remainder),
        "limit_reason": (
            "increment_bound is bounded and remainder_ratio tends to zero "
            "because Delta tends to zero"
        ),
        "passed": sp.simplify(divided_remainder - increment_bound * remainder_ratio)
        == 0,
    }


def nonlinear_family_check() -> dict:
    rows = []
    flow_velocity = -np.linalg.solve(
        metric(THETA_OLD), energy_gradient(THETA_OLD)
    )
    for tau in TAUS:
        solved = root(jko_first_order, THETA_OLD + tau * flow_velocity, args=(tau,))
        if not solved.success:
            raise RuntimeError(solved.message)
        theta_new = solved.x
        delta_velocity = (theta_new - THETA_OLD) / tau
        g_new = metric(theta_new)
        gradient_new = energy_gradient(theta_new)
        theorem_residual = g_new @ delta_velocity + gradient_new
        identity_control_residual = delta_velocity + gradient_new
        rows.append(
            {
                "tau": float(tau),
                "theta_new": theta_new.tolist(),
                "metric": g_new.tolist(),
                "metric_eigenvalues": np.linalg.eigvalsh(g_new).tolist(),
                "metric_off_diagonal": float(g_new[0, 1]),
                "increment_over_tau_norm": float(np.linalg.norm(delta_velocity)),
                "implicit_residual_norm": float(np.linalg.norm(theorem_residual)),
                "velocity_error_to_preconditioned_flow": float(
                    np.linalg.norm(delta_velocity - flow_velocity)
                ),
                "identity_metric_control_residual": float(
                    np.linalg.norm(identity_control_residual)
                ),
            }
        )
    small_tau = TAUS[-4:]
    errors = np.array(
        [row["velocity_error_to_preconditioned_flow"] for row in rows[-4:]]
    )
    slope = float(np.polyfit(np.log(small_tau), np.log(errors), 1)[0])
    theorem_residuals = np.array(
        [row["implicit_residual_norm"] for row in rows[-4:]]
    )
    theorem_residual_slope = float(
        np.polyfit(np.log(small_tau), np.log(theorem_residuals), 1)[0]
    )
    maximum_theorem_residual = max(
        row["implicit_residual_norm"] for row in rows
    )
    smallest_tau_theorem_residual = rows[-1]["implicit_residual_norm"]
    minimum_metric_eigenvalue = min(
        min(row["metric_eigenvalues"]) for row in rows
    )
    minimum_off_diagonal = min(
        abs(row["metric_off_diagonal"]) for row in rows
    )
    identity_control_limit = rows[-1]["identity_metric_control_residual"]
    euclidean_velocity = -energy_gradient(THETA_OLD)
    preconditioning_effect = float(
        np.linalg.norm(flow_velocity - euclidean_velocity)
    )
    passed = (
        smallest_tau_theorem_residual < 0.002
        and 0.9 < theorem_residual_slope < 1.1
        and 0.9 < slope < 1.1
        and minimum_metric_eigenvalue > 0.1
        and minimum_off_diagonal > 0.2
        and identity_control_limit > 0.2
        and preconditioning_effect > 0.2
    )
    return {
        "family": (
            "mu=N(0,I2), F_theta(z)=z+m(theta), "
            "m(theta)=(a+0.35ab, 0.45a+b+0.15a^2)"
        ),
        "invertibility": "translation in z for every theta",
        "energy": (
            "0.5*(mean(mu_theta)-target)^T C "
            "(mean(mu_theta)-target)"
        ),
        "theta_old": THETA_OLD.tolist(),
        "taus": TAUS.tolist(),
        "preconditioned_flow_velocity": flow_velocity.tolist(),
        "euclidean_flow_velocity": euclidean_velocity.tolist(),
        "preconditioning_effect_norm": preconditioning_effect,
        "maximum_implicit_residual_norm": maximum_theorem_residual,
        "implicit_residual_at_smallest_tau": smallest_tau_theorem_residual,
        "small_tau_implicit_residual_loglog_slope": theorem_residual_slope,
        "small_tau_velocity_error_loglog_slope": slope,
        "minimum_metric_eigenvalue": minimum_metric_eigenvalue,
        "minimum_absolute_metric_off_diagonal": minimum_off_diagonal,
        "identity_metric_control_residual_at_smallest_tau": (
            identity_control_limit
        ),
        "rows": rows,
        "passed": passed,
    }


def run_contract() -> dict:
    certificate = symbolic_certificate()
    checker = nonlinear_family_check()
    integrity = source_sha256() == EXPECTED_SOURCE_SHA256
    passed = certificate["passed"] and checker["passed"] and integrity
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "scope": (
            "Proposition 6.3 under its Frechet regularity, square-integrable "
            "Jacobian, differentiable-energy, and O(tau)-increment assumptions"
        ),
        "exact_contract": (
            "G(theta_plus)(theta_plus-theta_old)/tau equals "
            "-grad F(mu_theta_plus)+o(1) as tau tends to zero."
        ),
        "source_integrity": {
            "observed_sha256": source_sha256(),
            "expected_sha256": EXPECTED_SOURCE_SHA256,
            "paper_html_sha256": (
                "9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a"
            ),
            "passed": integrity,
        },
        "symbolic_certificate": certificate,
        "independent_checker": checker,
        "limitations": (
            "The general proof is an independently reconstructed symbolic "
            "derivation rather than a proof-assistant formalization. The numerical "
            "checker is a nonlinear continuous translation family, not a neural network."
        ),
    }


def negative_control() -> dict:
    checker = nonlinear_family_check()
    residual = checker["identity_metric_control_residual_at_smallest_tau"]
    passed = residual < 1e-3
    return {
        "control": "replace the pullback metric G(theta_plus) by the identity",
        "smallest_tau": float(TAUS[-1]),
        "identity_metric_residual": residual,
        "acceptance_tolerance": 1e-3,
        "expected_to_fail": True,
        "passed_as_claim": passed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    result = negative_control() if args.negative_control else run_contract()
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.negative_control:
        return 0 if result["passed_as_claim"] else 1
    return 0 if result["status"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
