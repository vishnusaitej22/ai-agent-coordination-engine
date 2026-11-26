
from typing import Any, Literal
from unittest.mock import Mock

import pytest
from pydantic import BaseModel, Field, ValidationError

from backend.agents.base_agent import BaseAgent


# Temporary mock schemas for isolated testing.
class MockAgentInput(BaseModel):
    task_id: str = Field(min_length=1)
    user_request: str = Field(min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)


class MockAgentError(BaseModel):
    code: str
    message: str
    details: str | None = None


class MockAgentResponse(BaseModel):
    task_id: str
    agent_name: str
    status: Literal["completed", "partial", "failed"]
    result: dict[str, Any] = Field(default_factory=dict)
    next_agent: str | None = None
    error: MockAgentError | None = None


class MockResult(BaseModel):
    message: str


def create_base_agent(llm=None):
    """Create a BaseAgent instance for helper testing."""

    return BaseAgent(
        agent_name="test_agent",
        input_schema=MockAgentInput,
        response_schema=MockAgentResponse,
        error_schema=MockAgentError,
        llm=llm,
    )


def sample_input():
    return {
        "task_id": "TASK001",
        "user_request": "Test Base Agent",
        "context": {},
    }


def test_validate_dictionary_input():
    agent = create_base_agent()

    result = agent.validate_input(sample_input())

    assert isinstance(result, MockAgentInput)
    assert result.task_id == "TASK001"


def test_validate_pydantic_input():
    agent = create_base_agent()

    input_data = MockAgentInput(**sample_input())

    result = agent.validate_input(input_data)

    assert isinstance(result, MockAgentInput)
    assert result.user_request == "Test Base Agent"


def test_invalid_input_is_rejected():
    agent = create_base_agent()

    with pytest.raises(ValidationError):
        agent.validate_input({
            "task_id": "",
            "user_request": "Invalid input",
            "context": {},
        })


def test_create_success_response():
    agent = create_base_agent()

    response = agent.create_success_response(
        task_id="TASK002",
        result={"message": "Task completed"},
    )

    assert isinstance(response, MockAgentResponse)
    assert response.task_id == "TASK002"
    assert response.agent_name == "test_agent"
    assert response.status == "completed"
    assert response.result["message"] == "Task completed"
    assert response.next_agent is None
    assert response.error is None


def test_create_success_response_with_pydantic_result():
    agent = create_base_agent()

    response = agent.create_success_response(
        task_id="TASK003",
        result=MockResult(message="Pydantic result"),
    )

    assert response.result == {
        "message": "Pydantic result"
    }


def test_create_error_response():
    agent = create_base_agent()

    response = agent.create_error_response(
        task_id="TASK004",
        error_code="TEST_ERROR",
        message="Simulated failure",
        details="Testing structured error handling",
    )

    assert response.status == "failed"
    assert response.task_id == "TASK004"
    assert response.result == {}
    assert response.error is not None
    assert response.error.code == "TEST_ERROR"
    assert response.error.message == "Simulated failure"


def test_llm_not_configured():
    agent = create_base_agent()

    with pytest.raises(RuntimeError, match="LLM is not configured"):
        agent.invoke_llm("Test prompt")


def test_llm_invocation():
    mock_llm = Mock()
    mock_llm.invoke.return_value = "Mock LLM response"

    agent = create_base_agent(llm=mock_llm)

    result = agent.invoke_llm("Hello")

    assert result == "Mock LLM response"
    mock_llm.invoke.assert_called_once_with("Hello")


def test_invalid_success_result_is_rejected():
    agent = create_base_agent()

    with pytest.raises(TypeError):
        agent.create_success_response(
            task_id="TASK005",
            result="This must be a dictionary or Pydantic model",
        )
