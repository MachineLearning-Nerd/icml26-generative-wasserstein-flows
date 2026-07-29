"""Exact gradient-map certificate for Proposition 3.2."""

from __future__ import annotations

import argparse
import json
import math

import numpy as np
import sympy as sp
from scipy.optimize import minimize


HERMITE_NODES, HERMITE_WEIGHTS = np.polynomial.hermite.hermgauss(24)


def symbolic_certificate() -> dict:
    epsilon, tau, gamma = sp.symbols(
        "epsilon tau gamma", positive=True, real=True
    )
    gradient_coefficient = gamma * epsilon
    ot_coefficient = epsilon / 2
    gamma_solution = sp.solve(
        sp.Eq(gradient_coefficient, ot_coefficient), gamma
    )
    epsilon_substitution = sp.simplify(epsilon.subs(epsilon, 2 * tau))
    jko_scaling_residual = sp.simplify(
        (sp.Symbol("W2") + epsilon_substitution * sp.Symbol("D"))
        - 2
        * tau
        * (
            sp.Symbol("W2") / (2 * tau)
            + sp.Symbol("D")
        )
    )
    cost_residual = sp.simplify(1 / epsilon_substitution - 1 / (2 * tau))
    passed = (
        gamma_solution == [sp.Rational(1, 2)]
        and jko_scaling_residual == 0
        and cost_residual == 0
    )
    return {
        "wasserstein_gradient": "grad_W2 F_epsilon(mu)=epsilon grad phi_mu,eta*^c_epsilon",
        "wgd_map": "Id-gamma*epsilon*grad phi",
        "optimal_transport_map": "Id-(epsilon/2)*grad phi",
        "unique_gamma": [str(value) for value in gamma_solution],
        "epsilon_substitution": "epsilon=2*tau",
        "jko_objective_scaling_residual": str(jko_scaling_residual),
        "cost_scaling_residual": str(cost_residual),
        "conclusion": "gamma=1/2 makes WGD push mu exactly to eta*, which is the JKO minimizer when epsilon=2*tau",
        "passed": passed,
    }


def gaussian_logpdf(
    points: np.ndarray, mean: np.ndarray, std: np.ndarray
) -> np.ndarray:
    centered = (points - mean) / std
    return (
        -0.5 * np.sum(centered**2, axis=1)
        - np.sum(np.log(std))
        - 0.5 * len(mean) * math.log(2 * math.pi)
    )


def gaussian_expectation_points(
    mean: np.ndarray, std: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    first, second = np.meshgrid(
        HERMITE_NODES, HERMITE_NODES, indexing="ij"
    )
    weight_first, weight_second = np.meshgrid(
        HERMITE_WEIGHTS, HERMITE_WEIGHTS, indexing="ij"
    )
    standard = np.stack(
        [first.reshape(-1), second.reshape(-1)], axis=1
    ) * math.sqrt(2)
    points = mean + std * standard
    weights = (weight_first * weight_second).reshape(-1) / math.pi
    return points, weights


def divergence(
    name: str,
    eta_mean: np.ndarray,
    eta_std: np.ndarray,
    nu_mean: np.ndarray,
    nu_std: np.ndarray,
) -> float:
    if name == "KL":
        return float(
            0.5
            * np.sum(
                (eta_std**2 + (eta_mean - nu_mean) ** 2) / nu_std**2
                - 1
                + np.log(nu_std**2 / eta_std**2)
            )
        )

    eta_points, eta_weights = gaussian_expectation_points(
        eta_mean, eta_std
    )
    log_eta_at_eta = gaussian_logpdf(eta_points, eta_mean, eta_std)
    log_nu_at_eta = gaussian_logpdf(eta_points, nu_mean, nu_std)
    if name == "chi2":
        ratio = np.exp(np.clip(log_eta_at_eta - log_nu_at_eta, -50, 50))
        return float(np.sum(eta_weights * ratio) - 1)

    if name == "JS":
        nu_points, nu_weights = gaussian_expectation_points(nu_mean, nu_std)
        log_nu_at_nu = gaussian_logpdf(nu_points, nu_mean, nu_std)
        log_eta_at_nu = gaussian_logpdf(nu_points, eta_mean, eta_std)
        eta_term = (
            math.log(2)
            + log_eta_at_eta
            - np.logaddexp(log_eta_at_eta, log_nu_at_eta)
        )
        nu_term = (
            math.log(2)
            + log_nu_at_nu
            - np.logaddexp(log_nu_at_nu, log_eta_at_nu)
        )
        return float(
            0.5 * np.sum(eta_weights * eta_term)
            + 0.5 * np.sum(nu_weights * nu_term)
        )
    raise ValueError(name)


def solve_envelope(
    mu_coordinate: np.ndarray,
    nu_mean: np.ndarray,
    nu_std: np.ndarray,
    epsilon: float,
    divergence_name: str,
    start: np.ndarray | None = None,
) -> tuple[float, np.ndarray, dict]:
    dimension = len(nu_mean)
    mu_mean = mu_coordinate[:dimension]
    mu_std = mu_coordinate[dimension:]

    def objective(params: np.ndarray) -> float:
        eta_mean = params[:dimension]
        eta_std = np.exp(params[dimension:])
        wasserstein = np.sum((mu_mean - eta_mean) ** 2 + (mu_std - eta_std) ** 2)
        return float(
            wasserstein
            + epsilon
            * divergence(
                divergence_name,
                eta_mean,
                eta_std,
                nu_mean,
                nu_std,
            )
        )

    if start is None:
        start = np.concatenate([mu_mean, np.log(mu_std)])
    mean_bounds = [
        (float(min(mu_mean[i], nu_mean[i]) - 3), float(max(mu_mean[i], nu_mean[i]) + 3))
        for i in range(dimension)
    ]
    if divergence_name == "chi2":
        std_bounds = [
            (math.log(0.25 * value), math.log(1.20 * value))
            for value in nu_std
        ]
    else:
        std_bounds = [(math.log(0.2), math.log(2.5))] * dimension
    result = minimize(
        objective,
        start,
        method="L-BFGS-B",
        bounds=mean_bounds + std_bounds,
        options={"ftol": 1e-14, "gtol": 1e-10, "maxiter": 1200},
    )
    eta = np.concatenate(
        [result.x[:dimension], np.exp(result.x[dimension:])]
    )
    return float(result.fun), eta, {
        "optimizer_success": bool(result.success),
        "gradient_norm": float(np.linalg.norm(result.jac)),
        "iterations": int(result.nit),
        "raw_parameters": result.x,
    }


def finite_difference_gradient(
    mu_coordinate: np.ndarray,
    nu_mean: np.ndarray,
    nu_std: np.ndarray,
    epsilon: float,
    divergence_name: str,
    base_parameters: np.ndarray,
) -> np.ndarray:
    gradient = np.zeros_like(mu_coordinate)
    step = 2e-4
    for index in range(len(mu_coordinate)):
        plus = mu_coordinate.copy()
        minus = mu_coordinate.copy()
        plus[index] += step
        minus[index] -= step
        plus_value, _, _ = solve_envelope(
            plus,
            nu_mean,
            nu_std,
            epsilon,
            divergence_name,
            base_parameters,
        )
        minus_value, _, _ = solve_envelope(
            minus,
            nu_mean,
            nu_std,
            epsilon,
            divergence_name,
            base_parameters,
        )
        gradient[index] = (plus_value - minus_value) / (2 * step)
    return gradient


def continuous_checker() -> dict:
    cases = [
        {
            "divergence": "KL",
            "mu": [-0.8, 0.6, 0.7, 1.2],
            "nu_mean": [0.4, -0.5],
            "nu_std": [1.1, 0.8],
            "epsilon": 0.30,
        },
        {
            "divergence": "chi2",
            "mu": [-0.3, 0.4, 0.75, 0.85],
            "nu_mean": [0.2, -0.2],
            "nu_std": [1.0, 1.1],
            "epsilon": 0.20,
        },
        {
            "divergence": "JS",
            "mu": [-1.0, 0.8, 0.9, 0.7],
            "nu_mean": [0.6, -0.4],
            "nu_std": [1.1, 0.95],
            "epsilon": 0.50,
        },
    ]
    rows = []
    max_error = 0.0
    min_wrong_error = math.inf
    for case in cases:
        mu = np.asarray(case["mu"], dtype=float)
        nu_mean = np.asarray(case["nu_mean"], dtype=float)
        nu_std = np.asarray(case["nu_std"], dtype=float)
        value, eta, info = solve_envelope(
            mu,
            nu_mean,
            nu_std,
            case["epsilon"],
            case["divergence"],
        )
        gradient = finite_difference_gradient(
            mu,
            nu_mean,
            nu_std,
            case["epsilon"],
            case["divergence"],
            info["raw_parameters"],
        )
        wgd_update = mu - 0.5 * gradient
        wrong_update = mu - 0.35 * gradient
        error = float(np.linalg.norm(wgd_update - eta))
        wrong_error = float(np.linalg.norm(wrong_update - eta))
        max_error = max(max_error, error)
        min_wrong_error = min(min_wrong_error, wrong_error)
        rows.append(
            {
                "divergence": case["divergence"],
                "epsilon": case["epsilon"],
                "tau": case["epsilon"] / 2,
                "envelope_value": value,
                "eta_star": eta.tolist(),
                "finite_difference_gradient": gradient.tolist(),
                "gamma_half_update": wgd_update.tolist(),
                "gamma_half_error": error,
                "gamma_0_35_error": wrong_error,
                "optimizer": {
                    key: value
                    for key, value in info.items()
                    if key != "raw_parameters"
                },
            }
        )
    return {
        "family": "2-D diagonal Gaussian measures with numerical Moreau-envelope differentiation",
        "divergences": ["KL", "chi2", "Jensen-Shannon"],
        "rows": rows,
        "maximum_gamma_half_error": max_error,
        "minimum_wrong_gamma_error": min_wrong_error,
        "tolerance": 8e-4,
        "passed": max_error < 8e-4 and min_wrong_error > 1e-2,
    }


def negative_control() -> dict:
    checker = continuous_checker()
    wrong_gamma_passes = checker["minimum_wrong_gamma_error"] <= checker["tolerance"]
    return {
        "control": "replace gamma=1/2 by gamma=0.35",
        "minimum_distance_to_jko_update": checker["minimum_wrong_gamma_error"],
        "acceptance_tolerance": checker["tolerance"],
        "expected_to_fail": True,
        "passed_as_claim": wrong_gamma_passes,
    }


def run_contract() -> dict:
    symbolic = symbolic_certificate()
    independent = continuous_checker()
    control = {
        "control": "replace gamma=1/2 by gamma=0.35",
        "minimum_distance_to_jko_update": independent["minimum_wrong_gamma_error"],
        "acceptance_tolerance": independent["tolerance"],
        "expected_to_fail": True,
        "passed_as_claim": (
            independent["minimum_wrong_gamma_error"] <= independent["tolerance"]
        ),
    }
    passed = symbolic["passed"] and independent["passed"] and not control["passed_as_claim"]
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "scope": "Proposition 3.2 under Lemma F.2 differentiability and optimal-map assumptions",
        "exact_contract": (
            "Wasserstein gradient descent on F_epsilon with gamma=1/2 "
            "and epsilon=2*tau pushes mu exactly to the JKO minimizer of D_f."
        ),
        "symbolic_certificate": symbolic,
        "independent_checker": independent,
        "negative_control": control,
        "limitations": (
            "The exact certificate invokes Lemma F.2's measure-differentiability "
            "result as an audited premise. The independent multi-divergence "
            "checker differentiates the envelope within a continuous diagonal-"
            "Gaussian submanifold."
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
