
# Core Configuration

## 1. Purpose

The `core` folder contains the basic configuration files required by the AI Agent Coordination and Decision Engine.

These files help manage application settings and prepare the connection to the selected Large Language Model (LLM).

## 2. Files in This Folder

### settings.py

This file manages the application configuration.

It is responsible for:
- Loading application settings.
- Reading environment variables.
- Storing the selected LLM provider and model name.
- Managing API keys securely.
- Providing configuration to other modules.

### llm_config.py

This file is responsible for LLM configuration and initialization.

It will:
- Read the LLM settings from `settings.py`.
- Check whether an LLM provider is configured.
- Initialize the selected language model.
- Provide the LLM instance to agents.

**Current status:** The basic configuration is implemented. Actual provider initialization will be completed after the team selects the LLM provider and model.

## 3. Environment Variables

The application uses environment variables to manage configuration.

| Variable | Purpose |
|---|---|
| APP_NAME | Application name |
| ENVIRONMENT | Application environment |
| DEBUG | Enable or disable debug mode |
| LOG_LEVEL | Application logging level |
| LLM_PROVIDER | Selected LLM provider |
| LLM_MODEL | Selected LLM model |
| LLM_API_KEY | API key for the selected provider |
| LLM_BASE_URL | Provider API URL, when required |

API keys must be stored in a local `.env` file and must never be committed to GitHub.

## 4. Required Python Packages

The current core configuration uses:

- pydantic
- pydantic-settings
- python-dotenv
- langchain-core

Python 3.11 is used for local development.

## 5. How to Use

Other backend modules can access the application settings using:

```python
from backend.core.settings import get_settings

settings = get_settings()

print(settings.app_name)
```

The LLM initialization function can be imported using:

```python
from backend.core.llm_config import get_llm
```

The actual LLM connection will work after provider-specific integration is completed.

## 6. Current Development Status

| Component | Status |
|---|---|
| Application settings | Implemented |
| Environment variable support | Implemented |
| Secure API key configuration | Prepared |
| LLM configuration structure | Implemented |
| Actual LLM provider integration | Pending team selection |

## 7. Ownership

**Module Owner:** M2 – LLM Integration and Base Agent Development

Changes to shared configuration should be coordinated with M1 and the relevant team members.
