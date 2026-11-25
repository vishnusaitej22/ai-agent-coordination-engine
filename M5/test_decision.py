import pytest

from decision_agent import DecisionAgent
from schemas import DecisionInput, AgentInput


# ==========================================
# HELPER FUNCTION
# ==========================================

def create_decision_input():

    return DecisionInput(
        task_id="TEST004",
        analysis_result={},
        available_options=[
            {
                "name": "Option A",
                "cost": 10,
                "benefit": 20,
                "risk": 2
            },
            {
                "name": "Option B",
                "cost": 5,
                "benefit": 30,
                "risk": 1
            }
        ],
        evaluation_criteria={},
        context={}
    )


# ==========================================
# 1. BASIC DECISION TEST
# ==========================================

def test_decision_agent_success():

    agent = DecisionAgent()
    data = create_decision_input()

    result = agent.decide(data)

    assert result.recommended_decision == "Option B"
    assert len(result.evaluated_options) == 2


# ==========================================
# 2. NO OPTIONS TEST
# ==========================================

def test_decision_agent_no_options():

    agent = DecisionAgent()

    data = DecisionInput(
        task_id="TEST005",
        analysis_result={},
        available_options=[],
        evaluation_criteria={},
        context={}
    )

    with pytest.raises(ValueError):
        agent.decide(data)


# ==========================================
# 3. NEGATIVE COST TEST
# ==========================================

def test_decision_agent_negative_cost():

    agent = DecisionAgent()

    data = DecisionInput(
        task_id="TEST006",
        analysis_result={},
        available_options=[
            {
                "name": "Option A",
                "cost": -10,
                "benefit": 20,
                "risk": 2
            }
        ],
        evaluation_criteria={},
        context={}
    )

    with pytest.raises(ValueError):
        agent.decide(data)


# ==========================================
# 4. STANDARD RESPONSE SUCCESS
# ==========================================

def test_decision_agent_standard_response_success():

    agent = DecisionAgent()

    data = DecisionInput(
        task_id="TEST007",
        analysis_result={},
        available_options=[
            {
                "name": "Option A",
                "cost": 10,
                "benefit": 30,
                "risk": 5
            }
        ],
        evaluation_criteria={},
        context={}
    )

    response = agent.decide_response(data)

    assert response.task_id == "TEST007"
    assert response.agent_name == "decision_agent"
    assert response.status == "completed"
    assert response.result["recommended_decision"] == "Option A"
    assert response.error is None


# ==========================================
# 5. STANDARD RESPONSE FAILURE
# ==========================================

def test_decision_agent_standard_response_failure():

    agent = DecisionAgent()

    data = DecisionInput(
        task_id="TEST008",
        analysis_result={},
        available_options=[],
        evaluation_criteria={},
        context={}
    )

    response = agent.decide_response(data)

    assert response.task_id == "TEST008"
    assert response.agent_name == "decision_agent"
    assert response.status == "failed"
    assert response.result == {}
    assert response.error.code == "DECISION_FAILED"
    assert response.next_agent is None


# ==========================================
# 6. M3 TOOLS INTEGRATION TEST
# ==========================================

def test_decision_agent_m3_integration():

    agent = DecisionAgent()
    data = create_decision_input()

    result = agent.decide(data)

    assert result.recommended_decision == "Option B"
    assert len(result.evaluated_options) == 2

    for option in result.evaluated_options:
        assert "score" in option
        assert "normalized_scores" in option

    assert "comparison_note" in result.risks_and_benefits


# ==========================================
# 7. NORMALIZATION TEST
# ==========================================

def test_decision_agent_score_normalization():

    agent = DecisionAgent()

    data = DecisionInput(
        task_id="TEST010",
        analysis_result={},
        available_options=[
            {
                "name": "Option A",
                "cost": 10,
                "benefit": 20,
                "risk": 5
            },
            {
                "name": "Option B",
                "cost": 10,
                "benefit": 20,
                "risk": 5
            }
        ],
        evaluation_criteria={},
        context={}
    )

    result = agent.decide(data)

    for option in result.evaluated_options:

        scores = option["normalized_scores"]

        assert scores["benefit"] == 100.0
        assert scores["cost"] == 100.0
        assert scores["risk"] == 100.0


# ==========================================
# 8. DUPLICATE OPTION TEST
# ==========================================

def test_decision_agent_duplicate_options():

    agent = DecisionAgent()

    data = DecisionInput(
        task_id="TEST011",
        analysis_result={},
        available_options=[
            {
                "name": "Option A",
                "cost": 10,
                "benefit": 20,
                "risk": 5
            },
            {
                "name": "Option A",
                "cost": 5,
                "benefit": 30,
                "risk": 2
            }
        ],
        evaluation_criteria={},
        context={}
    )

    with pytest.raises(ValueError, match="unique"):
        agent.decide(data)


# ==========================================
# 9. COMMON AGENT INPUT EXECUTE TEST
# ==========================================

def test_decision_agent_execute():

    agent = DecisionAgent()

    data = AgentInput(
        task_id="TEST012",
        user_request="Choose the best option",
        context={
            "analysis_result": {},
            "available_options": [
                {
                    "name": "Option A",
                    "cost": 10,
                    "benefit": 20,
                    "risk": 2
                },
                {
                    "name": "Option B",
                    "cost": 5,
                    "benefit": 30,
                    "risk": 1
                }
            ],
            "evaluation_criteria": {}
        }
    )

    response = agent.execute(data)

    assert response.task_id == "TEST012"
    assert response.agent_name == "decision_agent"
    assert response.status == "completed"
    assert response.result["recommended_decision"] == "Option B"
    assert response.error is None
