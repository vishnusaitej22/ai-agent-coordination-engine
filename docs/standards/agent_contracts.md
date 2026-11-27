# Common Agent and Workflow Contracts

## 1. Purpose

This document defines the common data formats and communication standards used by all agents and the workflow orchestration system in the AI Agent Coordination Engine.

These contracts are agreed between M1 (System Architecture and Integration) and M7 (Agent Orchestration and Backend) as the initial shared contract.

All team members must follow these standards when implementing their modules.

## 2. Contract Principles

- Use JSON-compatible data structures.
- Keep field names consistent across all modules.
- Preserve task and workflow identifiers throughout execution.
- Use explicit status and error fields.
- Store structured information in `result`.
- Validate inputs and outputs at component boundaries using Pydantic.
- Use TypedDict for LangGraph workflow state.
- The orchestrator controls agent routing and handoffs.
- Retry handling is centrally managed by the orchestrator.
- Discuss and document breaking contract changes before implementation.

## 3. Contract A — Agent Input

All agents must accept a common input structure.

```json
{
  "task_id": "TASK001",
  "user_request": "Analyse product sales",
  "context": {}
}
```

| Field | Description |
|---|---|
| `task_id` | Unique identifier for the task |
| `user_request` | User's business request or task instruction |
| `context` | Additional workflow information and relevant data |

**Standard method:** `execute(input_data)`

Each agent must process the input and return a standard AgentResponse.

## 4. Contract B — Agent Response

All agents must return a common response structure.

```json
{
  "task_id": "TASK001",
  "agent_name": "research_agent",
  "status": "completed",
  "result": {},
  "next_agent": "analysis_agent",
  "error": null
}
```

| Field | Description |
|---|---|
| `task_id` | Identifier matching the input task |
| `agent_name` | Name of the executing agent |
| `status` | Agent execution status |
| `result` | Structured output produced by the agent |
| `next_agent` | Optional next-agent information |
| `error` | Structured error information or null |

### Allowed Agent Statuses

- `completed` — Agent completed its task successfully.
- `partial` — Agent completed only part of its task.
- `failed` — Agent execution failed.

**Important:** The `next_agent` field is informational. Actual routing and handoffs are controlled by LangGraph, not individual agents.

## 5. Contract C — Agent Error

Errors must follow a common structure.

```json
{
  "code": "SOURCE_UNAVAILABLE",
  "message": "The required information source could not be reached",
  "details": {},
  "agent_name": "research_agent"
}
```

| Field | Description |
|---|---|
| `code` | Error identifier |
| `message` | Human-readable error description |
| `details` | Optional additional error information |
| `agent_name` | Optional name of the agent where the error occurred |

Retry counts and retry attempts are maintained centrally by the orchestrator, not independently by individual agents.

## 6. Contract D — Workflow State

LangGraph uses a shared workflow state implemented with TypedDict.

The initial workflow state contains the following fields:

| Field | Description |
|---|---|
| `workflow_id` | Unique workflow identifier |
| `task_id` | Task identifier |
| `user_request` | Original user request |
| `context` | Shared context information |
| `plan` | Planning agent output |
| `research_result` | Research agent output |
| `analysis_result` | Analysis agent output |
| `decision_result` | Decision agent output |
| `agent_outputs` | Complete agent responses for tracking and debugging |
| `agents_executed` | Ordered list of executed agents |
| `current_agent` | Currently executing agent |
| `status` | Overall workflow status |
| `retry_count` | Retry tracking information |
| `approval_status` | Human approval information |
| `final_result` | Final workflow output |
| `error` | Workflow error information, if any |

### Allowed Workflow Statuses

- `pending` — Workflow has not started.
- `running` — Workflow is currently executing.
- `completed` — Workflow completed successfully.
- `failed` — Workflow execution failed.
- `skipped` — A workflow step was skipped.
- `waiting_for_approval` — Workflow is waiting for human approval.

Agent statuses and workflow statuses must remain separate.

## 7. Contract E — Workflow Output

The workflow returns a standard final response.

```json
{
  "workflow_id": "WF001",
  "status": "completed",
  "agents_executed": [
    "planning_agent",
    "research_agent",
    "analysis_agent",
    "decision_agent"
  ],
  "final_result": {},
  "error": null
}
```

| Field | Description |
|---|---|
| `workflow_id` | Unique workflow identifier |
| `status` | Overall workflow status |
| `agents_executed` | Ordered list of agents that executed |
| `final_result` | Structured final output |
| `error` | Workflow error information or null |

## 8. Workflow Execution and Orchestration

The initial workflow execution sequence is:

1. Planning Agent
2. Research Agent
3. Analysis Agent
4. Decision Agent
5. Human Approval, if required
6. Execution Tool, if approved
7. Final Response

### Orchestration Rules

- LangGraph controls routing and conditional transitions.
- Agents communicate their outputs through the shared workflow state.
- The orchestrator passes relevant outputs between agents.
- The orchestrator manages retries and retry limits centrally.
- Complete agent responses are stored in `agent_outputs`.
- Agents must not independently invoke other agents.
- Human approval must happen before any execution that requires approval.
- The workflow must not proceed with an approval-dependent execution unless the required approval is received.

## 9. Schema Ownership and Responsibilities

1. M1 is responsible for documenting and coordinating the common contracts.
2. M7 is responsible for implementing the approved contracts in the LangGraph workflow and backend API.
3. M1 and M7 review shared contract changes together.
4. M2–M8 must follow the approved interfaces when implementing their respective modules.
5. All agent owners must update their implementations and tests when a contract change is approved.
6. No team member should independently add, rename, or remove shared fields without coordination.

## 10. Contract Testing Expectations

All modules must verify the following:

- Valid agent input passes validation.
- Missing required fields are rejected.
- Incorrect field types are rejected.
- Agent responses preserve the original `task_id`.
- Agent responses use an allowed agent status.
- Successful responses contain `error: null`.
- Failed responses contain structured error information.
- Workflow responses contain a valid workflow ID and status.
- Workflow state tracks executed agents.
- Retry handling is controlled by the orchestrator.
- Approval-dependent execution waits for human approval.

## 11. Contract Approval

This document represents the initial shared contract confirmed by M1 and M7 on 24 November 2026.

All team members should use this document as the common reference for module development and integration.

Any future changes must be discussed and agreed upon by M1 and M7 before implementation.