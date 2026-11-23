# Member Responsibilities and File Ownership

## 1. Purpose
This document records the eight-member allocation from the project specification. Each member owns their assigned module, performs independent testing and supports integration.

## 2. Team allocation

| Member | Role / focus | Main ownership |
|---|---|---|
| M1 | System Architecture, Project Coordination & Integration | Overall architecture, common interfaces, GitHub integration, system-level testing and documentation |
| M2 | LLM Integration & Base Agent Development | LLM configuration, prompt templates, reusable base agent and response generation |
| M3 | Tool Integration & External Services | Custom tools, database retrieval, API integrations, validation and tool execution |
| M4 | Planning Agent & Research Agent | Task planning, information retrieval and research results |
| M5 | Analysis Agent & Decision Agent | Business analysis, option evaluation, decision-making and recommendations |
| M6 | Memory & Knowledge Management | Short-term memory, long-term memory, shared context and retrieval |
| M7 | Agent Orchestration, Workflow Automation & Backend API | LangGraph orchestration, workflow execution, task management and FastAPI endpoints |
| M8 | Frontend Dashboard, Monitoring UI & AWS Deployment | React application, workflow visualization, dashboard and deployment coordination |

## 3. Shared repository ownership
| Folder/file | Owner |
|---|---|
| `docs/` | M1 |
| `backend/core/` | M2 |
| `backend/agents/base_agent.py` | M2 |
| `backend/agents/response_agent.py` | M2 |
| `backend/agents/planning_agent.py` | M4 |
| `backend/agents/research_agent.py` | M4 |
| `backend/agents/analysis_agent.py` | M5 |
| `backend/agents/decision_agent.py` | M5 |
| `backend/tools/` | M3 |
| `backend/memory/` | M6 |
| `backend/orchestration/` | M7 |
| `backend/workflows/` | M7 |
| `backend/api/` | M7 |
| `backend/database/` | M7 |
| `backend/tests/` | Individual component owners |
| `backend/main.py` | M7 |
| `frontend/` | M8 |
| `deployment/` | M8, with M7 supporting backend deployment |
| Root configuration | M1 coordinates; relevant component owner implements |

## 4. Important interface ownership
- M1 designs and documents `agent_schema.py` and `workflow_schema.py` contracts.
- M7 implements those contracts in the shared backend API schemas.
- All members must follow the approved definitions.
- The Execution Agent's external actions are handled by M3's tools and M7's controlled execution workflow.
- The Response Agent is developed by M2.

## 5. Shared responsibilities
Every member must:
1. Implement only their assigned files unless a shared change is agreed.
2. Test their component independently with sample inputs and mock data.
3. Follow the common input/output contracts.
4. Document setup, inputs, outputs and test instructions.
5. Use feature branches and pull requests.
6. Participate in weekly integration and final demonstration.
7. Keep API keys, passwords and cloud credentials out of GitHub.

## 6. Coordination and escalation
- Discuss shared contract changes with M1 and M7 before implementation.
- Notify M1 when a dependency or integration blocker appears.
- Record the blocker, affected component, owner and next action.
- Use mocks for unfinished components so other members can continue development.
