"""M3 reusable deterministic tools for the Enterprise Workflow Platform.

No third-party dependencies are required. Functions return JSON-serializable
Python values and raise TypeError/ValueError for invalid inputs.
"""
from collections.abc import Mapping, Sequence
from typing import Any


def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be an integer or float.")
    return float(value)


def calculate_total(values: Sequence[float]) -> float:
    """Return the sum of a non-string sequence of numbers."""
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TypeError("values must be a sequence of numbers.")
    return sum(_number(v, f"values[{i}]") for i, v in enumerate(values))


def calculate_average(values: Sequence[float]) -> float:
    """Return the arithmetic mean; reject an empty sequence."""
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TypeError("values must be a sequence of numbers.")
    if not values:
        raise ValueError("values must contain at least one number.")
    return calculate_total(values) / len(values)


def calculate_percentage(part: float, total: float) -> float:
    """Return part / total * 100; total must not be zero."""
    part = _number(part, "part")
    total = _number(total, "total")
    if total == 0:
        raise ValueError("total must not be zero.")
    return (part / total) * 100


def compare_values(value1: float, value2: float) -> dict[str, Any]:
    """Compare two numeric values and return a structured result."""
    a, b = _number(value1, "value1"), _number(value2, "value2")
    relation = "greater_than" if a > b else "less_than" if a < b else "equal_to"
    return {"value1": a, "value2": b, "relation": relation}


def calculate_weighted_score(
    criteria_scores: Mapping[str, float],
    weights: Mapping[str, float],
) -> dict[str, Any]:
    """Calculate a weighted mean for scores on a 0-100 scale.

    The two mappings must have identical keys. Weights must be non-negative
    with a positive sum; they are normalized by dividing by their sum.
    """
    if not isinstance(criteria_scores, Mapping) or not isinstance(weights, Mapping):
        raise TypeError("criteria_scores and weights must be mappings.")
    if not criteria_scores:
        raise ValueError("At least one criterion score is required.")
    if set(criteria_scores) != set(weights):
        raise ValueError("criteria_scores and weights must have identical keys.")

    weight_sum = 0.0
    weighted_sum = 0.0
    breakdown = {}
    for criterion, raw_score in criteria_scores.items():
        score = _number(raw_score, f"score for {criterion}")
        weight = _number(weights[criterion], f"weight for {criterion}")
        if not 0 <= score <= 100:
            raise ValueError(f"Score for {criterion} must be between 0 and 100.")
        if weight < 0:
            raise ValueError(f"Weight for {criterion} cannot be negative.")
        weight_sum += weight
        weighted_sum += score * weight
        breakdown[str(criterion)] = {"score": score, "weight": weight}

    if weight_sum <= 0:
        raise ValueError("The sum of weights must be greater than zero.")
    return {
        "weighted_score": round(weighted_sum / weight_sum, 2),
        "total_weight": round(weight_sum, 4),
        "breakdown": breakdown,
    }


def evaluate_risk(likelihood: int, impact: int) -> dict[str, Any]:
    """Return likelihood x impact and a starter risk band (1-5 scales).

    Bands: low 1-5, medium 6-14, high 15-25. Confirm these thresholds
    with the project team before treating them as the project's official scale.
    """
    for value, name in ((likelihood, "likelihood"), (impact, "impact")):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer from 1 to 5.")
        if not 1 <= value <= 5:
            raise ValueError(f"{name} must be between 1 and 5.")
    score = likelihood * impact
    level = "low" if score <= 5 else "medium" if score <= 14 else "high"
    return {
        "likelihood": likelihood,
        "impact": impact,
        "risk_score": score,
        "risk_level": level,
    }


def compare_options(
    options: Mapping[str, Mapping[str, float]],
    weights: Mapping[str, float],
) -> dict[str, Any]:
    """Rank options using weighted scores; higher criterion scores are better.

    Convert cost/time/risk into benefit-style 0-100 scores before calling,
    if lower raw values are preferable.
    """
    if not isinstance(options, Mapping) or not options:
        raise ValueError("options must be a non-empty mapping.")
    if not isinstance(weights, Mapping) or not weights:
        raise ValueError("weights must be a non-empty mapping.")

    ranked = []
    for option_name, scores in options.items():
        if not isinstance(scores, Mapping):
            raise TypeError(f"Scores for {option_name} must be a mapping.")
        if set(scores) != set(weights):
            raise ValueError(f"Option {option_name} must contain exactly the weighted criteria.")
        score_result = calculate_weighted_score(scores, weights)
        ranked.append({
            "option": str(option_name),
            "weighted_score": score_result["weighted_score"],
            "breakdown": score_result["breakdown"],
        })

    ranked.sort(key=lambda item: item["weighted_score"], reverse=True)
    return {
        "ranked_options": ranked,
        "recommended_option": ranked[0]["option"],
        "note": "Ranking is based only on the supplied scores and weights.",
    }
