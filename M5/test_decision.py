
import pytest

from decision_agent import DecisionAgent
from schemas import DecisionInput


def test_decision_agent_success():

    agent = DecisionAgent()

    data = DecisionInput(
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

    result = agent.decide(data)

    assert result.recommended_decision == "Option B"


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
