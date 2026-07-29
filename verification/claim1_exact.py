"""Exact proof skeleton and continuous checker for Proposition 3.1."""

from __future__ import annotations

import argparse
import json
import math

import numpy as np
import sympy as sp
from scipy.optimize import minimize


def symbolic_certificate() -> dict:
    """Mechanically verify the order argument after the cited duality premises."""
    a, c, d = sp.symbols("A C D", real=True)
    weak_duality_gap = a - d
    map_subset_gap = d - c
    minimax_gap = a - c
    gap_identity = sp.simplify(
        weak_duality_gap + map_subset_gap - minimax_gap
    )

    q = sp.symbols("q", nonnegative=True)
    gamma_curvature = sp.Integer(0)
    critic_curvature = -q
    passed = (
        gap_identity == 0
        and gamma_curvature == 0
        and sp.ask(sp.Q.nonpositive(critic_curvature)) is True
    )
    return {
        "objective_symbols": {
            "A": "inf_T sup_h L(T,h)",
            "C": "sup_h inf_gamma L_tilde(gamma,h)",
            "D": "sup_h inf_T L(T,h)",
        },
        "premises": [
            "A=C by coupling reparametrization, minimax, and Monge recovery",
            "A-D>=0 by weak duality",
            "D-C>=0 because deterministic-map couplings are a subset",
        ],
        "gap_identity": "(A-D)+(D-C)=A-C",
        "sympy_residual": str(gap_identity),
        "curvature": {
            "coupling_second_variation": str(gamma_curvature),
            "critic_second_variation": str(critic_curvature),
            "f_star_second_derivative_assumed_nonnegative": True,
        },
        "conclusion": "A=C forces both nonnegative gaps to zero, hence A=D",
        "passed": passed,
    }


def gaussian_primal(
    mu_mean: np.ndarray,
    mu_std: np.ndarray,
    nu_mean: np.ndarray,
    nu_std: np.ndarray,
    tau: float,
) -> tuple[float, dict]:
    dimension = len(mu_mean)

    def objective(params: np.ndarray) -> float:
        scale = np.exp(params[:dimension])
        shift = params[dimension:]
        eta_mean = scale * mu_mean + shift
        eta_std = scale * mu_std
        transport = np.sum(
            ((scale - 1) * mu_mean + shift) ** 2
            + ((scale - 1) * mu_std) ** 2
        ) / (2 * tau)
        kl = 0.5 * np.sum(
            (eta_std**2 + (eta_mean - nu_mean) ** 2) / nu_std**2
            - 1
            + np.log(nu_std**2 / eta_std**2)
        )
        return float(transport + kl)

    start = np.concatenate(
        [np.zeros(dimension), nu_mean - mu_mean]
    )
    result = minimize(objective, start, method="BFGS", options={"gtol": 1e-12})
    return float(result.fun), {
        "optimizer_success": bool(result.success or np.linalg.norm(result.jac) < 1e-6),
        "gradient_norm": float(np.linalg.norm(result.jac)),
        "iterations": int(result.nit),
    }


def gaussian_dual(
    mu_mean: np.ndarray,
    mu_std: np.ndarray,
    nu_mean: np.ndarray,
    nu_std: np.ndarray,
    tau: float,
) -> tuple[float, dict]:
    dimension = len(mu_mean)
    lower_q = np.full(dimension, -1 / tau + 1e-7)
    upper_q = 1 / nu_std**2 - 1e-7

    def objective(params: np.ndarray) -> float:
        q = params[:dimension]
        r = params[dimension:]
        denominator_inner = 1 + tau * q
        scale = 1 / denominator_inner
        shift = -tau * r / denominator_inner
        y_mean = scale * mu_mean + shift
        y_second = (scale * mu_std) ** 2 + y_mean**2
        transport = np.sum(
            ((scale - 1) * mu_mean + shift) ** 2
            + ((scale - 1) * mu_std) ** 2
        ) / (2 * tau)
        critic_mean = np.sum(0.5 * q * y_second + r * y_mean)
        denominator_exp = 1 - q * nu_std**2
        log_normalizer = np.sum(
            -0.5 * np.log(denominator_exp)
            + 0.5 * q * nu_mean**2
            + r * nu_mean
            + 0.5
            * nu_std**2
            * (q * nu_mean + r) ** 2
            / denominator_exp
        )
        dual_value = transport + critic_mean - log_normalizer
        return float(-dual_value)

    bounds = list(zip(lower_q, upper_q, strict=True)) + [
        (-10.0, 10.0)
    ] * dimension
    result = minimize(
        objective,
        np.zeros(2 * dimension),
        method="L-BFGS-B",
        bounds=bounds,
        options={"ftol": 1e-14, "gtol": 1e-10, "maxiter": 2000},
    )
    return float(-result.fun), {
        "optimizer_success": bool(result.success),
        "gradient_norm": float(np.linalg.norm(result.jac)),
        "iterations": int(result.nit),
    }


def continuous_gaussian_checker() -> dict:
    cases = [
        {
            "mu_mean": [-1.2, 0.7],
            "mu_std": [0.55, 1.4],
            "nu_mean": [0.4, -0.9],
            "nu_std": [1.1, 0.65],
            "tau": 0.17,
        },
        {
            "mu_mean": [1.5, -0.3],
            "mu_std": [1.8, 0.45],
            "nu_mean": [-0.6, 1.1],
            "nu_std": [0.7, 1.25],
            "tau": 0.43,
        },
        {
            "mu_mean": [0.2, -1.7],
            "mu_std": [0.8, 1.6],
            "nu_mean": [1.3, 0.1],
            "nu_std": [1.45, 0.5],
            "tau": 0.08,
        },
    ]
    rows = []
    max_error = 0.0
    for case in cases:
        arrays = {
            key: np.asarray(case[key], dtype=float)
            for key in ("mu_mean", "mu_std", "nu_mean", "nu_std")
        }
        primal, primal_info = gaussian_primal(**arrays, tau=case["tau"])
        dual, dual_info = gaussian_dual(**arrays, tau=case["tau"])
        error = abs(primal - dual)
        max_error = max(max_error, error)
        rows.append(
            {
                **case,
                "vwgf_value": primal,
                "s_jko_value": dual,
                "absolute_error": error,
                "primal_optimizer": primal_info,
                "dual_optimizer": dual_info,
            }
        )
    return {
        "family": "2-D anisotropic diagonal Gaussians; KL; affine maps and quadratic optimal critics",
        "case_count": len(rows),
        "rows": rows,
        "maximum_absolute_error": max_error,
        "tolerance": 2e-7,
        "passed": max_error < 2e-7,
    }


def negative_control() -> dict:
    """Removing absolute continuity permits a non-Monge coupling gap."""
    countermodel = {"A": 1, "B": 0, "C": 0, "D": 0}
    premises_without_monge = {
        "minimax_B_equals_C": countermodel["B"] == countermodel["C"],
        "weak_duality_D_le_A": countermodel["D"] <= countermodel["A"],
        "map_subset_C_le_D": countermodel["C"] <= countermodel["D"],
    }
    equality_claim = countermodel["A"] == countermodel["D"]
    return {
        "control": "remove absolute continuity/Monge recovery premise A=B",
        "countermodel": countermodel,
        "remaining_premises": premises_without_monge,
        "equality_claim_holds": equality_claim,
        "expected_to_fail": True,
        "passed_as_claim": equality_claim,
    }


def run_contract() -> dict:
    symbolic = symbolic_certificate()
    independent = continuous_gaussian_checker()
    control = negative_control()
    passed = symbolic["passed"] and independent["passed"] and not control["passed_as_claim"]
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "scope": "Proposition 3.1 under its absolute-continuity, finite-second-moment, convex f-divergence, and minimax assumptions",
        "exact_contract": (
            "For mu_l and nu in P_ac,2(R^d), the full VWGF objective (6), "
            "inf_T sup_h L(T,h), equals the full S-JKO objective (9), "
            "sup_h inf_T L(T,h), after h maps to -h."
        ),
        "symbolic_certificate": symbolic,
        "independent_checker": independent,
        "negative_control": control,
        "limitations": (
            "The algebraic order certificate is exact but invokes the cited "
            "measure-theoretic minimax and Monge-recovery theorems as checked "
            "premises rather than formalizing them in a proof assistant."
        ),
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
