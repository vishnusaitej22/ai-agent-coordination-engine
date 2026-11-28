
"""
LLM configuration and initialization.

Provider-specific integrations will be added after
the team confirms the LLM provider.
"""

from langchain_core.language_models.chat_models import BaseChatModel

from backend.core.settings import get_settings


def get_llm() -> BaseChatModel:
    """
    Return the configured language model.

    Raises:
        ValueError: If the LLM provider has not been configured.
        NotImplementedError: If the provider integration is not implemented.
    """

    settings = get_settings()

    if not settings.llm_provider:
        raise ValueError(
            "LLM provider is not configured. "
            "Set LLM_PROVIDER in the environment."
        )

    raise NotImplementedError(
        f"LLM provider '{settings.llm_provider}' "
        "has not been integrated yet."
    )
