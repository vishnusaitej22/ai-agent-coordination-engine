# Common Agent and Workflow Contracts

## 1. Purpose
This document defines the common data formats that agents and the workflow use to communicate. The examples follow the project specification. They are illustrative contracts; M1 and M7 must agree the final Pydantic schemas before implementation.

## 2. Contract principles
- Use JSON-compatible data.
- Keep field names consistent across all modules.
- Preserve task/workflow identifiers as data moves through the system.
- Use explicit status and error fields.
- Put structured information in `result`; do not rely on unstructured prose alone.
- Validate inputs and outputs at component boundaries.
- Discuss and document any breaking contract change before implementation.

## 3. Contract A — Agent input
```json
{
  "task_id": "TASK001",
  "user_request": "Analyse product sales",
  "context": {}
}
```

| Field | Meaning |
|---|---|
| `task_id` | Identifier for the task being performed |
| `user_request` | Business request or task instruction |
| `context` | Additional relevant workflow/context data |

## 4. Contract B — Agent output
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

| Field | Meaning |
|---|---|
| `task_id` | Identifier matching the input task |
| `agent_name` | Name of the agent returning the result |
| `status` | Execution status |
| `result` | Structured result produced by the agent |
| `next_agent` | Suggested/expected next agent; orchestrator controls actual routing |
| `error` | `null` on success, structured error information when failed |

The example status `completed` is from the specification. The team should agree the complete allowed status set with M7.

## 5. Contract C — Workflow output
```json
{
  "workflow_id": "WF001",
  "status": "completed",
  "agents_executed": [
    "planning_agent",
    "research_agent",
    "analysis_agent",
    "decision_agent",
    "response_agent"
  ],
  "final_result": {}
}
```

| Field | Meaning |
|---|---|
| `workflow_id` | Identifier for the complete workflow |
| `status` | Overall workflow status |
| `agents_executed` | Ordered list of agents that executed |
| `final_result` | Structured final output for the user |

## 6. Example error output (proposed extension)
The following is a proposed implementation detail to agree with M7; it is not a literal example from the PDF:
```json
{
  "task_id": "TASK002",
  "agent_name": "research_agent",
  "status": "failed",
  "result": {},
  "next_agent": null,
  "error": {
    "code": "SOURCE_UNAVAILABLE",
    "message": "The required information source could not be reached"
  }
}
```

## 7. Schema ownership and approval
1. M1 documents and proposes the `agent_schema.py` and `workflow_schema.py` contracts.
2. M7 implements the approved contracts in the backend API schemas.
3. M1 and M7 review changes together.
4. All agent owners must update their implementations and tests when a contract change is approved.
5. Do not independently add, rename or remove shared fields.

## 8. Questions to resolve with M7 before freezing schemas
- Final allowed values for `status`.
- Whether `next_agent` is informational or required for routing (the orchestrator remains authoritative).
- Exact shape of `context`, `result` and `error`.
- Whether timestamps, correlation IDs or version fields are required.
- Workflow status and partial-result behavior.
- How retries and human approval are represented.

## 9. Contract test expectations
- Valid input passes validation.
- Missing required fields are rejected.
- Wrong field types are rejected.
- Agent output preserves the task identifier.
- Successful output has a valid status and `error: null`.
- Failed output contains an error description.
- Workflow output includes workflow ID, status, executed agents and final result.
