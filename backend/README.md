# Backend Documentation

## 1. Introduction

The `backend` folder contains the Python components of the AI Agent Coordination and Decision Engine.

It includes the agents, tools, application configuration, memory management, database connections, workflows and APIs.

Each team member develops their assigned module while following the shared project architecture and common Agent Contract.

## 2. Backend Folder Structure

| Folder | Purpose |
|---|---|
| `agents/` | Base Agent and specialized agents |
| `core/` | Application settings and LLM configuration |
| `tools/` | Reusable Python functions and external tools |
| `orchestration/` | Agent coordination and LangGraph workflow |
| `memory/` | Shared and long-term memory management |
| `workflows/` | Business workflow implementation |
| `api/` | Backend API routes and schemas |
| `database/` | Database connection and models |
| `tests/` | Unit and integration tests |

## 3. Requirements

The backend uses Python 3.11 for development.

The initial Python dependencies are maintained in `backend/requirements.txt`.

They currently include:

- Pydantic
- Pydantic Settings
- python-dotenv
- LangChain Core
- Pytest

Additional dependencies will be included as the remaining team modules are integrated.

## 4. Local Setup Instructions

Follow these steps to set up the backend on your computer.

### Step 1: Open the project directory

Open the `ai-agent-coordination-engine` project folder in VS Code.

### Step 2: Create a virtual environment

Run:

`python -m venv .venv`

### Step 3: Activate the virtual environment

For Windows PowerShell:

`.\.venv\Scripts\Activate.ps1`

For macOS/Linux:

`source .venv/bin/activate`

### Step 4: Install backend dependencies

Run this command from the project root directory:

`python -m pip install -r backend/requirements.txt`

### Step 5: Configure environment variables

Create a local `.env` file by copying `.env.example`.

For Windows PowerShell:

`Copy-Item .env.example .env`

For macOS/Linux:

`cp .env.example .env`

The LLM provider and model settings will be filled in after the team finalizes the provider selection.

Never commit actual API keys or passwords to GitHub.

## 5. Running Backend Tests

All backend tests are maintained in the `backend/tests/` directory.

To run all available backend tests, execute:

`python -m pytest backend/tests -v`

To run an individual test file:

`python -m pytest backend/tests/test_base_agent.py -v`

`python -m pytest backend/tests/test_response_agent.py -v`

Tests involving external LLM services should use mocked responses unless live API testing has been explicitly approved.

## 6. Development Guidelines

All team members should follow these rules:

1. Work only on the module assigned to you.
2. Follow the finalized common Agent Contract.
3. Use Pydantic for input and output validation.
4. Add unit tests for new functionality.
5. Keep API keys and passwords in local environment variables.
6. Do not independently change shared schemas or interfaces.
7. Use Git feature branches for development.
8. Submit changes through Pull Requests for review.

## 7. Current Development Status

The backend is under active development.

The M2 module currently includes:

- Application settings.
- Initial LLM configuration.
- Reusable Base Agent helper functionality.
- Response Agent.
- System and response prompt templates.
- Unit tests for Base Agent and Response Agent.

Actual LLM provider integration and full workflow integration are pending team-level decisions and coordination.

## 8. Team Responsibilities

| Member | Responsibility |
|---|---|
| M1 | System Architecture and Integration |
| M2 | LLM Integration and Base Agent |
| M3 | Tool Integration |
| M4 | Planning and Research Agents |
| M5 | Analysis and Decision Agents |
| M6 | Memory Management |
| M7 | Orchestration and Backend API |
| M8 | Frontend and Deployment |

## 9. Ownership

The backend is developed collaboratively by all eight team members.

Each member is responsible for maintaining and testing their assigned module and coordinating shared-interface changes with M1 and M7.