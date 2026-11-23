# System Test Plan

## 1. Purpose
This plan defines how the team will verify that individual components work together as one application. Every member tests their own component; integration testing is shared and coordinated by M1.

## 2. Test levels
| Test type | What it verifies |
|---|---|
| Unit | Individual functions, agents, scoring logic and status transitions |
| Contract | Agent inputs/outputs and API schema compatibility |
| API | HTTP status codes, request validation and error responses |
| Integration | Database repositories and LangGraph execution together |
| End-to-end | User request through agents to dashboard result |
| Failure | Tool timeout, invalid model output, agent failure and database unavailability |

## 3. Tools
- `pytest` for backend unit and integration tests.
- Postman for API testing.
- Browser-based testing for the React dashboard.
- Mock services/data for components that are unfinished or rely on external systems.

## 4. Integration test ownership
| Integration test | Primary testers |
|---|---|
| LLM + Base Agent | M2, M1 |
| Agent + Tools | M2, M3, M4 |
| Planning + Research | M4, M7 |
| Research + Analysis | M4, M5 |
| Analysis + Decision | M5, M7 |
| Agents + Memory | M6, M7 |
| All Agents + Orchestrator | M1, M7 |
| Backend + Frontend | M7, M8 |
| Complete system | All 8 members |
| AWS deployment | M7, M8 |

## 5. Minimum system test cases

| ID | Scenario | Expected result |
|---|---|---|
| SYS-01 | Submit a valid business request | API accepts request and workflow starts |
| SYS-02 | Submit empty/missing required request | API rejects input with a validation response |
| SYS-03 | Planning Agent receives a valid task | Structured task plan is returned |
| SYS-04 | Research Agent receives a valid research task | Structured findings or explicit data gaps are returned |
| SYS-05 | Research result is passed to Analysis | Analysis accepts the agreed contract |
| SYS-06 | Analysis result is passed to Decision | Decision returns an explained recommendation |
| SYS-07 | Agent returns invalid output | Validation catches it; workflow records a safe failure |
| SYS-08 | Tool/source is unavailable | Error or partial result is handled without fabricated data |
| SYS-09 | Agent execution fails | Workflow records failed state and exposes safe status |
| SYS-10 | Workflow completes successfully | Workflow output includes ID, status, executed agents and final result |
| SYS-11 | Relevant context is stored and retrieved | Memory returns the expected stored context |
| SYS-12 | Dashboard receives completed result | Final result is displayed |
| SYS-13 | Workflow is running | Dashboard displays running/loading state |
| SYS-14 | Workflow fails or service is unavailable | Dashboard displays an appropriate failure/unavailable state |
| SYS-15 | Consequential external action is requested | Workflow waits for required human approval before execution |

## 6. End-to-end acceptance scenario
Example user request: **"Analyse product sales and recommend improvements."**

Expected high-level sequence:
1. Dashboard submits the request.
2. Backend validates and creates the workflow.
3. Orchestrator invokes Planning Agent.
4. Research Agent retrieves sales information through approved tools.
5. Analysis Agent identifies findings using appropriate calculations.
6. Decision Agent evaluates options and explains a recommendation.
7. Response Agent prepares the final response.
8. Workflow result is returned and displayed on the dashboard.
9. Workflow status and relevant results are persisted according to the agreed design.

Acceptance: the workflow completes with schema-valid outputs, a traceable execution status and a user-visible final result. Missing data or failures must be represented honestly.

## 7. Test execution record
Record each test run:
| Field | Value |
|---|---|
| Test ID | |
| Date | |
| Build/branch/commit | |
| Tester | |
| Test data | |
| Actual result | |
| Pass/Fail | |
| Defect/issue link | |
| Notes | |

## 8. Definition of done
A task is complete only when:
- Acceptance criteria are met.
- It follows the agreed module and interface contract.
- Relevant tests pass.
- Errors and important edge cases are handled.
- Documentation is updated.
- No secrets or local-only files are committed.
- Its pull request is reviewed and merged into the agreed integration branch.
- It works with the current integrated branch, not only on the contributor's machine.

## 9. Final system acceptance checklist
- [ ] Invalid API input is rejected.
- [ ] Each agent returns schema-valid output for sample input.
- [ ] The graph completes the agreed happy-path workflow.
- [ ] Workflow and agent execution records are persisted.
- [ ] Failure states are stored and returned safely.
- [ ] Frontend handles loading, completed, failed and unavailable states.
- [ ] End-to-end demonstration is completed.
- [ ] Final documentation and handover are ready.
