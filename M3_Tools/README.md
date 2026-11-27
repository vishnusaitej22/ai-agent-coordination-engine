# M3 – Tools and Utility Functions

Reusable deterministic Python functions for the Enterprise Workflow Platform with Decision Automation System.

## Package contents
- `tools.py`: calculation, comparison, weighted scoring, and risk tools.
- `test_tools.py`: unit tests using Python's built-in `unittest`.
- `sample_input.json` and `sample_output.json`: sample tool request and response.
- `README.md`: this guide.

## Requirements
- Python 3.10 or later
- No third-party dependencies

## Run tests
From this folder:
```bash
python -m unittest -v
```

## Function interfaces

| Function | Parameters | Purpose |
|---|---|---|
| `calculate_total(values)` | Sequence of numbers | Sum values |
| `calculate_average(values)` | Non-empty sequence of numbers | Calculate arithmetic mean |
| `calculate_percentage(part, total)` | Two numbers; total nonzero | Calculate percentage |
| `compare_values(value1, value2)` | Two numbers | Compare two values |
| `calculate_weighted_score(criteria_scores, weights)` | Matching criterion mappings | Weighted score from 0–100 |
| `evaluate_risk(likelihood, impact)` | Integers 1–5 | Risk score and starter risk band |
| `compare_options(options, weights)` | Option-to-criteria scores and weights | Rank options |

## Usage examples
```python
from tools import calculate_weighted_score, compare_options, evaluate_risk

score = calculate_weighted_score(
    criteria_scores={"quality": 80, "efficiency": 90},
    weights={"quality": 0.6, "efficiency": 0.4},
)
print(score)

ranking = compare_options(
    options={
        "Option A": {"quality": 80, "efficiency": 70},
        "Option B": {"quality": 90, "efficiency": 85},
    },
    weights={"quality": 0.6, "efficiency": 0.4},
)
print(ranking)

risk = evaluate_risk(likelihood=4, impact=3)
print(risk)
```

## Integration notes for M5 / M2 / M7
- Import functions directly from `tools.py`; they do not require an LLM or LangGraph.
- Example: `from tools import calculate_weighted_score, compare_options`.
- Functions return ordinary Python numbers/dictionaries that can be serialized with `json.dumps()`.
- Invalid inputs raise `TypeError` or `ValueError`. The calling agent should catch these and map them into the common error envelope finalized by M1/M2.
- This module does not define the common Agent Input/Output contract.
- `compare_options` assumes higher criterion scores are better. Convert cost, time, or risk into a comparable benefit score (for example, 0–100) before ranking.
- Risk bands are starter conventions only; confirm the project's official thresholds with M1/M5 before production use.
- The recommended option is a mathematical ranking from the provided scores and weights, not an autonomous business decision.

## JSON serialization example
```python
import json
from tools import evaluate_risk

result = evaluate_risk(4, 3)
print(json.dumps(result, indent=2))
```
