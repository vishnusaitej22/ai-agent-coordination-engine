from schemas import (
    AgentInput,
    AnalysisInput,
    AnalysisResult,
    AgentResponse,
    AgentError
)


class AnalysisAgent:

    def __init__(self):
        self.agent_name = "analysis_agent"

    # Existing analysis business logic - unchanged
    def analyze(self, agent_input: AnalysisInput) -> AnalysisResult:

        findings = []
        problems = []
        trends = []

        data = agent_input.research_data

        if not isinstance(data, dict):
            raise ValueError("Research data must be a dictionary")

        # Analyze sales
        previous_sales = data.get("previous_sales")
        current_sales = data.get("current_sales")

        if previous_sales is not None and current_sales is not None:

            if previous_sales <= 0:
                raise ValueError("Previous sales must be greater than zero")

            change = (
                (current_sales - previous_sales) / previous_sales
            ) * 100

            findings.append(f"Sales changed by {change:.2f}%")

            if change < 0:
                problems.append("Sales have decreased")
                trends.append("Negative sales trend detected")

            elif change > 0:
                trends.append("Positive sales trend detected")

            else:
                trends.append("Sales remained unchanged")

        # Analyze complaints
        complaints = data.get("customer_complaints")

        if complaints is not None:

            if complaints < 0:
                raise ValueError("Customer complaints cannot be negative")

            findings.append(f"Customer complaints: {complaints}")

            if complaints > 20:
                problems.append("High number of customer complaints")

        # Analyze satisfaction
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

    # Standard method required by common agent contract
    def execute(self, input_data: AgentInput) -> AgentResponse:

        try:

            # Extract research data from common context
            research_data = input_data.context.get("research_data")

            # Convert common AgentInput into AnalysisInput
            analysis_input = AnalysisInput(
                task_id=input_data.task_id,
                user_request=input_data.user_request,
                research_data=research_data,
                context=input_data.context
            )

            # Call existing analysis logic
            analysis_result = self.analyze(analysis_input)

            # Return standard AgentResponse
            return AgentResponse(
                task_id=input_data.task_id,
                agent_name=self.agent_name,
                status="completed",
                result=analysis_result.model_dump(),
                next_agent="decision_agent",
                error=None
            )

        except (ValueError, TypeError) as exc:

            return AgentResponse(
                task_id=input_data.task_id,
                agent_name=self.agent_name,
                status="failed",
                result={},
                next_agent=None,
                error=AgentError(
                    code="ANALYSIS_FAILED",
                    message=str(exc),
                    details="Analysis Agent could not complete the task."
                )
            )


# Standalone execution
if __name__ == "__main__":

    agent = AnalysisAgent()

    # Common AgentInput
    common_input = AgentInput(
        task_id="TASK001",
        user_request="Analyze monthly business performance",
        context={
            "research_data": {
                "previous_sales": 50000,
                "current_sales": 40000,
                "customer_complaints": 25,
                "customer_satisfaction": 65
            }
        }
    )

    # Execute through common interface
    response = agent.execute(common_input)

    print("\nSTANDARD AGENT RESPONSE")
    print(response.model_dump_json(indent=4))