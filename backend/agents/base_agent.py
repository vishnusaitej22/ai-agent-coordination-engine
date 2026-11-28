
"""
Reusable Base Agent helpers for the AI Agent Coordination Engine.

Provides common validation, response construction, error handling,
logging and LLM invocation.

Specialized agents retain ownership of their execute() methods
and their agent-specific business logic.
"""

import json
import logging
from typing import Any

from pydantic import BaseModel

from langchain_core.language_models.chat_models import BaseChatModel


logger = logging.getLogger(__name__)


class BaseAgent:
    """
    Shared helper class for specialized AI agents.

    This class does not implement execute() or agent-specific
    business logic. Each specialized agent owns its own execution.
    """

    def __init__(
        self,
        agent_name: str,
        input_schema: type[BaseModel],
        response_schema: type[BaseModel],
        error_schema: type[BaseModel],
        llm: BaseChatModel | None = None,
    ) -> None:
        self.agent_name = agent_name
        self.input_schema = input_schema
        self.response_schema = response_schema
        self.error_schema = error_schema
        self.llm = llm

    def validate_input(
        self,
        input_data: BaseModel | dict[str, Any],
    ) -> BaseModel:
        """
        Validate input using the injected common Pydantic schema.

        Invalid input raises Pydantic ValidationError.
        """

        if isinstance(input_data, BaseModel):
            input_data = input_data.model_dump()

        return self.input_schema.model_validate(input_data)

    def create_success_response(
        self,
        task_id: str,
        result: BaseModel | dict[str, Any],
        next_agent: str | None = None,
        status: str = "completed",
    ) -> BaseModel:
        """
        Construct a standardized successful AgentResponse.

        Result data must be JSON-serializable.
        """

        if isinstance(result, BaseModel):
            result = result.model_dump(mode="json")

        if not isinstance(result, dict):
            raise TypeError(
                "Agent result must be a dictionary or Pydantic model."
            )

        # Verify that the result can be represented as JSON.
        result = json.loads(json.dumps(result, allow_nan=False))

        return self.response_schema.model_validate({
            "task_id": task_id,
            "agent_name": self.agent_name,
            "status": status,
            "result": result,
            "next_agent": next_agent,
            "error": None,
        })

    def create_error_response(
        self,
        task_id: str,
        error_code: str,
        message: str,
        details: str | None = None,
    ) -> BaseModel:
        """
        Construct a standardized failed AgentResponse.
        """

        error_data: dict[str, Any] = {
            "code": error_code,
            "message": message,
            "details": details,
        }

        # Include agent_name when supported by the shared schema.
        if "agent_name" in self.error_schema.model_fields:
            error_data["agent_name"] = self.agent_name

        error = self.error_schema.model_validate(error_data)

        return self.response_schema.model_validate({
            "task_id": task_id,
            "agent_name": self.agent_name,
            "status": "failed",
            "result": {},
            "next_agent": None,
            "error": error,
        })

    def log_failure(
        self,
        task_id: str,
        message: str,
        *,
        exc_info: bool = False,
    ) -> None:
        """Record an agent execution failure."""

        logger.error(
            "Agent '%s' failed for task '%s': %s",
            self.agent_name,
            task_id,
            message,
            exc_info=exc_info,
        )

    def invoke_llm(self, prompt: str) -> Any:
        """
        Invoke the configured LangChain chat model.

        Raises:
            RuntimeError: When no LLM is configured.
        """

        if self.llm is None:
            raise RuntimeError(
                "LLM is not configured for this agent."
            )

        return self.llm.invoke(prompt)
