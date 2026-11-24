
from schemas import (
    DecisionInput,
    DecisionResult,
    DecisionOption,
    DecisionCriteria,
    AgentResponse,
    AgentError
)


class DecisionAgent:

    def __init__(self):
        self.agent_name = "decision_agent"

    def decide(self, agent_input: DecisionInput) -> DecisionResult:

        options = agent_input.available_options

        if not options:
            raise ValueError("At least one option is required")

        # Step 1: Validate decision criteria
        criteria = DecisionCriteria.model_validate(
            agent_input.evaluation_criteria
        )

        evaluated_options = []

        # Step 2: Validate and evaluate every option
        for raw_option in options:

            option = DecisionOption.model_validate(raw_option)

            name = option.name
            cost = option.cost
            benefit = option.benefit
            risk = option.risk

            # Step 3: Calculate weighted score
            score = (
                (benefit * criteria.benefit_weight)
                - (cost * criteria.cost_weight)
                - (risk * criteria.risk_weight)
            )

            evaluated_options.append({
                "name": name,
                "cost": cost,
                "benefit": benefit,
                "risk": risk,
                "score": score
            })

        # Step 4: Select the highest-scoring option
        best_option = max(
            evaluated_options,
            key=lambda item: item["score"]
        )

        # Step 5: Prepare risk and benefit information
        risks = [
            {
                "option": item["name"],
                "risk": item["risk"],
                "benefit": item["benefit"]
            }
            for item in evaluated_options
        ]

        # Step 6: Read Analysis Agent findings
        analysis_data = agent_input.analysis_result

        identified_problems = analysis_data.get(
            "identified_problems", []
        )

        key_findings = analysis_data.get(
            "key_findings", []
        )

        trends = analysis_data.get(
            "trends_and_patterns", []
        )

        # Keep only valid text entries
        identified_problems = [
            item for item in identified_problems
            if isinstance(item, str) and item.strip()
        ] if isinstance(identified_problems, list) else []

        key_findings = [
            item for item in key_findings
            if isinstance(item, str) and item.strip()
        ] if isinstance(key_findings, list) else []

        trends = [
            item for item in trends
            if isinstance(item, str) and item.strip()
        ] if isinstance(trends, list) else []

        # Step 7: Prepare analysis context
        analysis_details = []

        if identified_problems:
            analysis_details.append(
                "Identified problems: "
                + "; ".join(identified_problems)
            )

        if key_findings:
            analysis_details.append(
                "Key findings: "
                + "; ".join(key_findings)
            )

        if trends:
            analysis_details.append(
                "Trends: "
                + "; ".join(trends)
            )

        if analysis_details:
            analysis_context = " ".join(analysis_details)
        else:
            analysis_context = (
                "No specific analysis findings were provided."
            )

        # Step 8: Generate reasoning
        reasoning = (
            f"{best_option['name']} received the highest weighted "
            f"score of {best_option['score']}. "
            f"Scoring weights used: "
            f"benefit={criteria.benefit_weight}, "
            f"cost={criteria.cost_weight}, "
            f"risk={criteria.risk_weight}. "
            f"Analysis context considered: {analysis_context}"
        )

        # Step 9: Return DecisionResult
        return DecisionResult(
            evaluated_options=evaluated_options,
            risks_and_benefits={
                "options": risks
            },
            recommended_decision=best_option["name"],
            reasoning=reasoning
        )

    # =================================================
    # COMMON AGENT RESPONSE
    # =================================================

    def decide_response(
        self,
        agent_input: DecisionInput
    ) -> AgentResponse:

        try:
            # Run the existing decision logic
            decision_result = self.decide(agent_input)

            # Wrap the result in the common agent contract
            return AgentResponse(
                task_id=agent_input.task_id,
                agent_name=self.agent_name,
                status="completed",
                result=decision_result.model_dump(),
                next_agent=None,
                error=None
            )

        except ValueError as exc:

            # Return a standard error response
            return AgentResponse(
                task_id=agent_input.task_id,
                agent_name=self.agent_name,
                status="failed",
                result={},
                next_agent=None,
                error=AgentError(
                    code="DECISION_FAILED",
                    message=str(exc),
                    details="Decision Agent could not complete the task."
                )
            )


if __name__ == "__main__":

    sample_input = DecisionInput(
        task_id="TASK002",
        analysis_result={
            "identified_problems": [
                "Sales have decreased",
                "Customer satisfaction is low",
                "Customer complaints are high"
            ],
            "key_findings": [
                "Sales changed by -20.00%",
                "Customer complaints: 25",
                "Customer satisfaction is 65%"
            ],
            "trends_and_patterns": [
                "Negative sales trend detected"
            ]
        },
        available_options=[
            {
                "name": "Improve Marketing",
                "cost": 10,
                "benefit": 25,
                "risk": 5
            },
            {
                "name": "Improve Customer Service",
                "cost": 8,
                "benefit": 30,
                "risk": 3
            },
            {
                "name": "Offer Discounts",
                "cost": 15,
                "benefit": 20,
                "risk": 8
            }
        ],
        evaluation_criteria={},
        context={}
    )

    agent = DecisionAgent()

    # Existing detailed result
    result = agent.decide(sample_input)

    print("\nDECISION AGENT RESULT")
    print(result.model_dump_json(indent=4))

    # New standard agent response
    response = agent.decide_response(sample_input)

    print("\nSTANDARD AGENT RESPONSE")
    print(response.model_dump_json(indent=4))

from schemas import (
    DecisionInput,
    DecisionResult,
    DecisionOption,
    DecisionCriteria,
    AgentResponse,
    AgentError
)


class DecisionAgent:

    def __init__(self):
        self.agent_name = "decision_agent"

    def decide(self, agent_input: DecisionInput) -> DecisionResult:

        options = agent_input.available_options

        if not options:
            raise ValueError("At least one option is required")

        # Step 1: Validate decision criteria
        criteria = DecisionCriteria.model_validate(
            agent_input.evaluation_criteria
        )

        evaluated_options = []

        # Step 2: Validate and evaluate every option
        for raw_option in options:

            option = DecisionOption.model_validate(raw_option)

            name = option.name
            cost = option.cost
            benefit = option.benefit
            risk = option.risk

            # Step 3: Calculate weighted score
            score = (
                (benefit * criteria.benefit_weight)
                - (cost * criteria.cost_weight)
                - (risk * criteria.risk_weight)
            )

            evaluated_options.append({
                "name": name,
                "cost": cost,
                "benefit": benefit,
                "risk": risk,
                "score": score
            })

        # Step 4: Select the highest-scoring option
        best_option = max(
            evaluated_options,
            key=lambda item: item["score"]
        )

        # Step 5: Prepare risk and benefit information
        risks = [
            {
                "option": item["name"],
                "risk": item["risk"],
                "benefit": item["benefit"]
            }
            for item in evaluated_options
        ]

        # Step 6: Read Analysis Agent findings
        analysis_data = agent_input.analysis_result

        identified_problems = analysis_data.get(
            "identified_problems", []
        )

        key_findings = analysis_data.get(
            "key_findings", []
        )

        trends = analysis_data.get(
            "trends_and_patterns", []
        )

        # Keep only valid text entries
        identified_problems = [
            item for item in identified_problems
            if isinstance(item, str) and item.strip()
        ] if isinstance(identified_problems, list) else []

        key_findings = [
            item for item in key_findings
            if isinstance(item, str) and item.strip()
        ] if isinstance(key_findings, list) else []

        trends = [
            item for item in trends
            if isinstance(item, str) and item.strip()
        ] if isinstance(trends, list) else []

        # Step 7: Prepare analysis context
        analysis_details = []

        if identified_problems:
            analysis_details.append(
                "Identified problems: "
                + "; ".join(identified_problems)
            )

        if key_findings:
            analysis_details.append(
                "Key findings: "
                + "; ".join(key_findings)
            )

        if trends:
            analysis_details.append(
                "Trends: "
                + "; ".join(trends)
            )

        if analysis_details:
            analysis_context = " ".join(analysis_details)
        else:
            analysis_context = (
                "No specific analysis findings were provided."
            )

        # Step 8: Generate reasoning
        reasoning = (
            f"{best_option['name']} received the highest weighted "
            f"score of {best_option['score']}. "
            f"Scoring weights used: "
            f"benefit={criteria.benefit_weight}, "
            f"cost={criteria.cost_weight}, "
            f"risk={criteria.risk_weight}. "
            f"Analysis context considered: {analysis_context}"
        )

        # Step 9: Return DecisionResult
        return DecisionResult(
            evaluated_options=evaluated_options,
            risks_and_benefits={
                "options": risks
            },
            recommended_decision=best_option["name"],
            reasoning=reasoning
        )

    # =================================================
    # COMMON AGENT RESPONSE
    # =================================================

    def decide_response(
        self,
        agent_input: DecisionInput
    ) -> AgentResponse:

        try:
            # Run the existing decision logic
            decision_result = self.decide(agent_input)

            # Wrap the result in the common agent contract
            return AgentResponse(
                task_id=agent_input.task_id,
                agent_name=self.agent_name,
                status="completed",
                result=decision_result.model_dump(),
                next_agent=None,
                error=None
            )

        except ValueError as exc:

            # Return a standard error response
            return AgentResponse(
                task_id=agent_input.task_id,
                agent_name=self.agent_name,
                status="failed",
                result={},
                next_agent=None,
                error=AgentError(
                    code="DECISION_FAILED",
                    message=str(exc),
                    details="Decision Agent could not complete the task."
                )
            )


if __name__ == "__main__":

    sample_input = DecisionInput(
        task_id="TASK002",
        analysis_result={
            "identified_problems": [
                "Sales have decreased",
                "Customer satisfaction is low",
                "Customer complaints are high"
            ],
            "key_findings": [
                "Sales changed by -20.00%",
                "Customer complaints: 25",
                "Customer satisfaction is 65%"
            ],
            "trends_and_patterns": [
                "Negative sales trend detected"
            ]
        },
        available_options=[
            {
                "name": "Improve Marketing",
                "cost": 10,
                "benefit": 25,
                "risk": 5
            },
            {
                "name": "Improve Customer Service",
                "cost": 8,
                "benefit": 30,
                "risk": 3
            },
            {
                "name": "Offer Discounts",
                "cost": 15,
                "benefit": 20,
                "risk": 8
            }
        ],
        evaluation_criteria={},
        context={}
    )

    agent = DecisionAgent()

    # Existing detailed result
    result = agent.decide(sample_input)

    print("\nDECISION AGENT RESULT")
    print(result.model_dump_json(indent=4))

    # New standard agent response
    response = agent.decide_response(sample_input)

    print("\nSTANDARD AGENT RESPONSE")
    print(response.model_dump_json(indent=4))
