
from schemas import AnalysisInput, AnalysisResult


class AnalysisAgent:

    def __init__(self):
        self.agent_name = "analysis_agent"

    def analyze(self, agent_input: AnalysisInput) -> AnalysisResult:

        findings = []
        problems = []
        trends = []

        data = agent_input.research_data

        # Check whether research data is a dictionary
        if not isinstance(data, dict):
            raise ValueError("Research data must be a dictionary")

        # Analyze sales
        previous_sales = data.get("previous_sales")
        current_sales = data.get("current_sales")

        if previous_sales is not None and current_sales is not None:

            if previous_sales <= 0:
                raise ValueError("Previous sales must be greater than zero")

            change = (
                (current_sales - previous_sales)
                / previous_sales
            ) * 100

            findings.append(
                f"Sales changed by {change:.2f}%"
            )

            if change < 0:
                problems.append("Sales have decreased")

                trends.append("Negative sales trend detected")

            elif change > 0:
                trends.append("Positive sales trend detected")

            else:
                trends.append("Sales remained unchanged")

        # Analyze customer complaints
        complaints = data.get("customer_complaints")

        if complaints is not None:

            if complaints < 0:
                raise ValueError("Customer complaints cannot be negative")

            findings.append(
                f"Customer complaints: {complaints}"
            )

            if complaints > 20:
                problems.append(
                    "High number of customer complaints"
                )

        # Analyze customer satisfaction
        satisfaction = data.get("customer_satisfaction")

        if satisfaction is not None:

            if not 0 <= satisfaction <= 100:
                raise ValueError(
                    "Customer satisfaction must be between 0 and 100"
                )

            findings.append(
                f"Customer satisfaction is {satisfaction}%"
            )

            if satisfaction < 70:
                problems.append(
                    "Customer satisfaction is below 70%"
                )

        # Generate summary
        if problems:
            summary = (
                "The business has identified issues that require attention. "
                + "; ".join(problems)
            )
        else:
            summary = (
                "No major problems were identified in the available data."
            )

        if not findings:
            summary += " More research data is required."

        return AnalysisResult(
            key_findings=findings,
            identified_problems=problems,
            trends_and_patterns=trends,
            analysis_summary=summary
        )


# Simple standalone execution
if __name__ == "__main__":

    sample_input = AnalysisInput(
        task_id="TASK001",
        user_request="Analyze monthly business performance",
        research_data={
            "previous_sales": 50000,
            "current_sales": 40000,
            "customer_complaints": 25,
            "customer_satisfaction": 65
        },
        context={}
    )

    agent = AnalysisAgent()

    result = agent.analyze(sample_input)

    print("\nANALYSIS AGENT RESULT")
    print(result.model_dump_json(indent=4))
