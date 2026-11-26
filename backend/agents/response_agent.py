
"""
Response Agent for the AI Agent Coordination and Decision Engine.

Generates the final user-facing response from previous agent results.
Uses BaseAgent for shared validation, LLM invocation,
response construction and error handling.
"""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError
from langchain_core.language_models.chat_models import BaseChatModel

from backend.agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):
    """Generates the final response for a completed workflow."""

    def __init__(
        self,
        input_schema: type[BaseModel],
        response_schema: type[BaseModel],
        error_schema: type[BaseModel],
        llm: BaseChatModel | None = None,
    ) -> None:
        super().__init__(
            agent_name="response_agent",
            input_schema=input_schema,
            response_schema=response_schema,
            error_schema=error_schema,
            llm=llm,
        )

        prompt_directory = Path(__file__).resolve().parent / "prompts"

        self.system_prompt = self._load_prompt(
            prompt_directory / "system_prompt.txt"
        )

        self.response_prompt = self._load_prompt(
            prompt_directory / "response_prompt.txt"
        )

    @staticmethod
    def _load_prompt(file_path: Path) -> str:
        """Load and validate a prompt text file."""

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Prompt file was not found: {file_path}"
            )

        prompt = file_path.read_text(encoding="utf-8").strip()

        if not prompt:
            raise ValueError(
                f"Prompt file is empty: {file_path}"
            )

        return prompt

    def _build_prompt(
        self,
        user_request: str,
        context: dict[str, Any],
    ) -> str:
        """Build the final response generation prompt."""

        context_json = json.dumps(
            context,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

        return (
            f"{self.system_prompt}\n\n"
            f"{self.response_prompt}\n\n"
            f"ORIGINAL USER REQUEST:\n{user_request}\n\n"
            "WORKFLOW CONTEXT AND PREVIOUS AGENT RESULTS:\n"
            f"{context_json}\n\n"
            "Generate the final response using only the "
            "information provided. Do not invent facts."
        )

    @staticmethod
    def _extract_text(llm_result: Any) -> str:
        """Extract readable text from an LLM response."""

        content = getattr(llm_result, "content", llm_result)

        if isinstance(content, str):
            response_text = content.strip()

        elif isinstance(content, list):
            text_parts = []

            for block in content:
                if isinstance(block, str):
                    text_parts.append(block)

                elif isinstance(block, dict):
                    block_text = block.get("text")

                    if isinstance(block_text, str):
                        text_parts.append(block_text)

            response_text = "\n".join(text_parts).strip()

        else:
            response_text = ""

        if not response_text:
            raise ValueError(
                "The LLM returned an empty or unreadable response."
            )

        return response_text

    def _process(
        self,
        agent_input: BaseModel,
    ) -> dict[str, Any]:
        """Generate the final response using workflow context."""

        context = agent_input.context or {}

        prompt = self._build_prompt(
            user_request=agent_input.user_request,
            context=context,
        )

        llm_result = self.invoke_llm(prompt)

        final_response = self._extract_text(llm_result)

        return {
            "final_response": final_response
        }

    def execute(
        self,
        input_data: BaseModel | dict[str, Any],
    ) -> BaseModel:
        """
        Execute the Response Agent and return the common AgentResponse.

        Input validation errors are raised to the caller.
        Processing errors are returned as structured AgentResponse errors.
        """

        # Validate common agent input.
        validated_input = self.validate_input(input_data)

        try:
            result = self._process(validated_input)

            return self.create_success_response(
                task_id=validated_input.task_id,
                result=result,
                next_agent=None,
                status="completed",
            )

        except Exception as exc:
            self.log_failure(
                task_id=validated_input.task_id,
                message=str(exc),
            )

            return self.create_error_response(
                task_id=validated_input.task_id,
                error_code="RESPONSE_GENERATION_FAILED",
                message="The Response Agent could not generate the final response.",
                details="Response generation failed. Check application logs for details.",
            )
