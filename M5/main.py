
from analysis_agent import AnalysisAgent
from decision_agent import DecisionAgent

from schemas import AnalysisInput, DecisionInput


def run_m5_workflow():

    print("\n===== M5 BUSINESS WORKFLOW =====")

    # Step 1: Research data
    research_data = {
        "previous_sales": 50000,
        "current_sales": 40000,
        "customer_complaints": 25,
        "customer_satisfaction": 65
    }

    # Step 2: Run Analysis Agent
    analysis_input = AnalysisInput(
        task_id="TASK100",
        user_request="Analyze business performance",
        research_data=research_data,
        context={}
    )

    analysis_agent = AnalysisAgent()

    analysis_result = analysis_agent.analyze(
        analysis_input
    )

    print("\n--- ANALYSIS RESULTS ---")
    print(analysis_result.model_dump_json(indent=4))

    # Step 3: Prepare Decision Agent input
    decision_input = DecisionInput(
        task_id="TASK100",
        analysis_result=analysis_result.model_dump(),
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

    # Step 4: Run Decision Agent
    decision_agent = DecisionAgent()

    decision_result = decision_agent.decide(
        decision_input
    )

    print("\n--- DECISION RESULTS ---")
    print(decision_result.model_dump_json(indent=4))

    # Step 5: Final recommendation
    print("\n===== FINAL RECOMMENDATION =====")

    print(
        "Recommended Action:",
        decision_result.recommended_decision
    )

    print(
        "Reason:",
        decision_result.reasoning
    )


if __name__ == "__main__":
    run_m5_workflow()
