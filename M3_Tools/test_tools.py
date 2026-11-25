import unittest
from tools import (
    calculate_total, calculate_average, calculate_percentage, compare_values,
    calculate_weighted_score, evaluate_risk, compare_options,
)


class TestM3Tools(unittest.TestCase):
    def test_total(self):
        self.assertEqual(calculate_total([10, 20, 30]), 60)

    def test_average(self):
        self.assertEqual(calculate_average([10, 20, 30]), 20)

    def test_percentage(self):
        self.assertEqual(calculate_percentage(25, 100), 25)

    def test_compare_values(self):
        self.assertEqual(compare_values(8, 5)["relation"], "greater_than")

    def test_weighted_score(self):
        result = calculate_weighted_score(
            {"quality": 80, "efficiency": 90},
            {"quality": 0.6, "efficiency": 0.4},
        )
        self.assertEqual(result["weighted_score"], 84.0)

    def test_risk(self):
        result = evaluate_risk(4, 5)
        self.assertEqual((result["risk_score"], result["risk_level"]), (20, "high"))

    def test_compare_options(self):
        result = compare_options(
            {
                "Option A": {"quality": 80, "efficiency": 70},
                "Option B": {"quality": 90, "efficiency": 85},
            },
            {"quality": 0.6, "efficiency": 0.4},
        )
        self.assertEqual(result["recommended_option"], "Option B")

    def test_empty_average_rejected(self):
        with self.assertRaises(ValueError):
            calculate_average([])

    def test_zero_total_rejected(self):
        with self.assertRaises(ValueError):
            calculate_percentage(5, 0)


if __name__ == "__main__":
    unittest.main()
