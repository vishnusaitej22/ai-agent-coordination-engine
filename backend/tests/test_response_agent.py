
from typing import Any, Literal
from unittest.mock import Mock

import pytest
from pydantic import BaseModel, Field, ValidationError

from backend.agents.response_agent import ResponseAgent


# Temporary schemas for isolated testing.
class ResponseTestInput(BaseModel):
    task_id: str = Field(min_length=1)
    user_request: str = Field(min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)


class ResponseTestError(BaseModel):
    code: str
    message: str
    details: str | None = None


class ResponseTestOutput(BaseModel):
    task_id: str
    agent_name: str
    status: Literal["completed", "partial", "failed"]
    result: dict[str, Any] = Field(default_factory=dict)
    next_agent: str | None = None
    error: ResponseTestError | None = None


def create_response_agent(mock_llm=None):
    """Create a Response Agent with temporary test schemas."""

    return ResponseAgent(
        input_schema=ResponseTestInput,
        response_schema=ResponseTestOutput,
        error_schema=ResponseTestError,
        llm=mock_llm,
    )


def sample_input():
    """Return sample workflow input."""

    return {
        "task_id": "TASK101",
        "user_request": "Analyze monthly business performance",
        "context": {
            "analysis_result": {
                "key_findings": ["Sales decreased by 20%"],
                "identified_problems": ["Sales are declining"],
            },
            "decision_result": {
                "recommended_decision": "Improve customer service"
            },
        },
    }


def test_response_agent_owns_execute_method():
    """Verify ResponseAgent implements its own execute method."""

    assert "execute" in ResponseAgent.__dict__


def test_successful_response_generation():
    mock_llm = Mock()
    mock_llm.invoke.return_value = (
        "Sales declined by 20%. Improving customer service "
        "is the recommended action."
    )

    agent = create_response_agent(mock_llm)

    response = agent.execute(sample_input())

    assert response.status == "completed"
    assert response.task_id == "TASK101"
    assert response.agent_name == "response_agent"
    assert response.result["final_response"]
    assert response.error is None

    mock_llm.invoke.assert_called_once()


def test_prompt_contains_user_request_and_context():
    mock_llm = Mock()
    mock_llm.invoke.return_value = "Business analysis completed."

    agent = create_response_agent(mock_llm)

    agent.execute(sample_input())

    prompt = mock_llm.invoke.call_args.args[0]

    assert "Analyze monthly business performance" in prompt
    assert "Sales decreased by 20%" in prompt
    assert "Improve customer service" in prompt


def test_invalid_input_is_rejected():
    agent = create_response_agent()

    with pytest.raises(ValidationError):
        agent.execute({
            "task_id": "",
            "user_request": "Invalid request",
            "context": {},
        })


def test_response_agent_handles_empty_llm_response():
    mock_llm = Mock()
    mock_llm.invoke.return_value = ""

    agent = create_response_agent(mock_llm)

    response = agent.execute(sample_input())

    assert response.status == "failed"
    assert response.result == {}
    assert response.error is not None
    assert response.error.code == "RESPONSE_GENERATION_FAILED"


def test_response_agent_handles_llm_exception():
    mock_llm = Mock()
    mock_llm.invoke.side_effect = RuntimeError(
        "Simulated LLM connection failure"
    )

    agent = create_response_agent(mock_llm)

    response = agent.execute(sample_input())

    assert response.status == "failed"
    assert response.error is not None
    assert response.error.code == "RESPONSE_GENERATION_FAILED"


def test_response_agent_without_llm():
    agent = create_response_agent()

    response = agent.execute(sample_input())

    assert response.status == "failed"
    assert response.error is not None
    assert response.error.code == "RESPONSE_GENERATION_FAILED"


def test_response_agent_extracts_ai_message():
    from langchain_core.messages import AIMessage

    mock_llm = Mock()
    mock_llm.invoke.return_value = AIMessage(
        content="The final business recommendation is to improve service."
    )

    agent = create_response_agent(mock_llm)

    response = agent.execute(sample_input())

    assert response.status == "completed"
    assert response.result["final_response"] == (
        "The final business recommendation is to improve service."
    )
