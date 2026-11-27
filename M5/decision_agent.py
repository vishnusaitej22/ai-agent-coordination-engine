import sys
from pathlib import Path

# ==========================================
# PROJECT ROOT PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================
# IMPORTS
# ==========================================

from schemas import (
    AgentInput,
    DecisionInput,
    DecisionResult,
    DecisionOption,
    DecisionCriteria,
    AgentResponse,
    AgentError
)

from M3_Tools.tools import compare_options


# ==========================================
# DECISION AGENT
# ==========================================

class DecisionAgent:

    def __init__(self):
        self.agent_name = "decision_agent"

    # ==========================================
    # 1. NORMALIZE SCORES
    # ==========================================

    def normalize_scores(self, options):

        benefits = [option.benefit for option in options]
        costs = [option.cost for option in options]
        risks = [option.risk for option in options]

        def normalize(values, higher_is_better=True):

            minimum = min(values)
            maximum = max(values)

            if maximum == minimum:
                return [100.0] * len(values)

            scores = []

            for value in values:

                if higher_is_better:
                    score = (
                        (value - minimum) /
                        (maximum - minimum)
                    ) * 100

                else:
                    score = (
                        (maximum - value) /
                        (maximum - minimum)
                    ) * 100

                scores.append(round(score, 2))

            return scores

        benefit_scores = normalize(benefits, True)
        cost_scores = normalize(costs, False)
        risk_scores = normalize(risks, False)

        return benefit_scores, cost_scores, risk_scores

    # ==========================================
    # 2. EXISTING DECISION BUSINESS LOGIC
    # ==========================================

    def decide(self, agent_input: DecisionInput) -> DecisionResult:

        if not agent_input.available_options:
            raise ValueError("At least one option is required")

        criteria = DecisionCriteria.model_validate(
            agent_input.evaluation_criteria
        )

        options = [
            DecisionOption.model_validate(item)
            for item in agent_input.available_options
        ]

        # Check duplicate option names
        names = [option.name for option in options]

        if len(names) != len(set(names)):
            raise ValueError("Option names must be unique")

        # Normalize scores
        benefit_scores, cost_scores, risk_scores = (
            self.normalize_scores(options)
        )

        # Prepare comparison data for M3
        comparison_data = {}

        for index, option in enumerate(options):

            comparison_data[option.name] = {
                "benefit": benefit_scores[index],
                "cost": cost_scores[index],
                "risk": risk_scores[index]
            }

        weights = {
            "benefit": criteria.benefit_weight,
            "cost": criteria.cost_weight,
            "risk": criteria.risk_weight
        }

        # Call M3 shared comparison tool
        comparison_result = compare_options(
            comparison_data,
            weights
        )

        ranked_options = comparison_result["ranked_options"]

        # Prepare evaluated options
        evaluated_options = []

        for index, option in enumerate(options):

            ranked = next(
                item for item in ranked_options
                if item["option"] == option.name
            )

            evaluated_options.append({
                "name": option.name,
                "cost": option.cost,
                "benefit": option.benefit,
                "risk": option.risk,
                "score": ranked["weighted_score"],
                "normalized_scores": {
                    "benefit": benefit_scores[index],
                    "cost": cost_scores[index],
                    "risk": risk_scores[index]
                }
            })

        # Best option
        best_option = comparison_result["recommended_option"]

        best_score = next(
            item["weighted_score"]
            for item in ranked_options
            if item["option"] == best_option
        )

        # Prepare risks and benefits
        risks = [
            {
                "option": item["name"],
                "risk": item["risk"],
                "benefit": item["benefit"]
            }
            for item in evaluated_options
        ]

        # Read Analysis Agent findings
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

        # Validate text entries
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

        # Prepare analysis context
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

        analysis_context = (
            " ".join(analysis_details)
            if analysis_details
            else "No specific analysis findings were provided."
        )

        # Generate reasoning
        reasoning = (
            f"{best_option} received the highest weighted score "
            f"of {best_score}. "
            f"Scoring weights: "
            f"benefit={criteria.benefit_weight}, "
            f"cost={criteria.cost_weight}, "
            f"risk={criteria.risk_weight}. "
            f"Analysis context considered: {analysis_context}"
        )

        return DecisionResult(
            evaluated_options=evaluated_options,
            risks_and_benefits={
                "options": risks,
                "comparison_note": comparison_result["note"]
            },
            recommended_decision=best_option,
            reasoning=reasoning
        )

    # ==========================================
    # 3. STANDARD AGENT RESPONSE
    # ==========================================

    def decide_response(
        self,
        agent_input: DecisionInput
    ) -> AgentResponse:

        try:

            decision_result = self.decide(agent_input)

            return AgentResponse(
                task_id=agent_input.task_id,
                agent_name=self.agent_name,
                status="completed",
                result=decision_result.model_dump(),
                next_agent=None,
                error=None
            )

        except (ValueError, TypeError) as exc:

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

    # ==========================================
    # 4. COMMON EXECUTE METHOD
    # ==========================================

    def execute(self, input_data: AgentInput) -> AgentResponse:

        try:

            # Extract data from common AgentInput context
            decision_data = input_data.context

            # Convert common AgentInput into DecisionInput
            decision_input = DecisionInput(
                task_id=input_data.task_id,

                analysis_result=decision_data.get(
                    "analysis_result", {}
                ),

                available_options=decision_data.get(
                    "available_options", []
                ),

                evaluation_criteria=decision_data.get(
                    "evaluation_criteria", {}
                ),

                context=input_data.context
            )

            # Call existing decision logic
            return self.decide_response(decision_input)

        except (ValueError, TypeError) as exc:

            return AgentResponse(
                task_id=input_data.task_id,
                agent_name=self.agent_name,
                status="failed",
                result={},
                next_agent=None,
                error=AgentError(
                    code="DECISION_FAILED",
                    message=str(exc),
                    details="Decision Agent could not process the common input."
                )
            )


# ==========================================
# 5. STANDALONE EXECUTION
# ==========================================

if __name__ == "__main__":

    agent = DecisionAgent()

    sample_input = AgentInput(
        task_id="TASK002",

        user_request="Evaluate business improvement options",

        context={

            "analysis_result": {
                "identified_problems": [
                    "Sales have decreased",
                    "Customer satisfaction is low"
                ],

                "key_findings": [
                    "Sales changed by -20.00%"
                ],

                "trends_and_patterns": [
                    "Negative sales trend detected"
                ]
            },

            "available_options": [
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

            "evaluation_criteria": {
                "benefit_weight": 1.0,
                "cost_weight": 1.0,
                "risk_weight": 1.0
            }
        }
    )

    response = agent.execute(sample_input)

    print("\n========== STANDARD AGENT RESPONSE ==========")
    print(response.model_dump_json(indent=4))