
import pytest

from analysis_agent import AnalysisAgent
from schemas import AgentInput, AnalysisInput


def test_analysis_agent_success():

    agent = AnalysisAgent()

    data = AnalysisInput(
        task_id="TEST001",
        user_request="Analyze sales",
        research_data={
            "previous_sales": 50000,
            "current_sales": 40000,
            "customer_complaints": 25,
            "customer_satisfaction": 65
        },
        context={}
    )

    result = agent.analyze(data)

    assert "Sales changed by -20.00%" in result.key_findings

    assert "Sales have decreased" in result.identified_problems

    assert result.analysis_summary != ""


def test_analysis_agent_positive_sales():

    agent = AnalysisAgent()

    data = AnalysisInput(
        task_id="TEST002",
        user_request="Analyze sales growth",
        research_data={
            "previous_sales": 100,
            "current_sales": 150
        },
        context={}
    )

    result = agent.analyze(data)

    assert "Positive sales trend detected" in result.trends_and_patterns


def test_analysis_agent_invalid_data():

    agent = AnalysisAgent()

    data = AnalysisInput(
        task_id="TEST003",
        user_request="Analyze invalid data",
        research_data="invalid data",
        context={}
    )

    with pytest.raises(ValueError):
        agent.analyze(data)


def test_analysis_agent_execute_common_input():

    input_data = AgentInput(
        task_id="TEST004",
        user_request="Analyze sales",
        context={
            "research_data": {
                "previous_sales": 50000,
                "current_sales": 40000,
                "customer_complaints": 25,
                "customer_satisfaction": 65
            }
        }
    )

    response = AnalysisAgent().execute(input_data)

    assert response.task_id == "TEST004"
    assert response.agent_name == "analysis_agent"
    assert response.status == "completed"
    assert response.error is None
