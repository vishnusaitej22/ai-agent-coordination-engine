# Coding Standards

## 1. Purpose
These conventions help the team produce code that can be reviewed, tested and integrated consistently. They are proposed team rules and should be confirmed by all members.

## 2. Python conventions
1. Use clear, descriptive names.
2. Use `snake_case` for variables and functions.
3. Use `PascalCase` for classes.
4. Use uppercase names for constants.
5. Keep functions focused and reasonably small.
6. Add type hints to public functions and shared interfaces.
7. Add docstrings to modules, classes and important public functions.
8. Handle expected errors explicitly; do not silently ignore exceptions.
9. Avoid hard-coded credentials, tokens, passwords and environment-specific paths.
10. Keep business logic separate from API route handlers where practical.

## 3. Data and API conventions
- Use JSON for HTTP and agent communication.
- Validate external inputs with the agreed Pydantic schemas.
- Use consistent field names and status values from `agent_contracts.md`.
- Return structured errors; do not expose stack traces or secrets to users.
- Document changes to shared request/response fields before merging.

## 4. Agent conventions
- Each agent has one clearly defined responsibility.
- Each agent accepts the agreed input structure and returns the agreed output structure.
- Agents report missing information and errors explicitly.
- Agents do not independently create uncontrolled execution chains.
- The orchestrator controls routing and workflow state.
- Tools return structured data and meaningful error information.

## 5. Testing conventions
- Add tests for new behavior and bug fixes.
- Include valid, invalid and missing-input cases.
- Use mocks for external APIs and unavailable components.
- Keep tests repeatable; do not depend on live paid services unless explicitly approved.
- Run relevant tests before opening a pull request.

## 6. Security and configuration
- Store local secrets in environment variables or an ignored local `.env` file.
- Commit `.env.example` with placeholder names, never real values.
- Ensure `.env`, credentials, tokens, local databases and virtual environments are ignored by Git.
- Validate and constrain external tool inputs.
- Require approval before consequential external actions where applicable.

## 7. Documentation
Every module owner documents:
- Purpose and ownership.
- Setup instructions.
- Inputs and outputs.
- Required environment variables (names only).
- How to run tests.
- Known limitations and dependencies.

## 8. Review checklist
- [ ] Names and structure are clear.
- [ ] Type hints and documentation are adequate.
- [ ] Errors are handled.
- [ ] Tests pass.
- [ ] Shared contracts are unchanged or documented and approved.
- [ ] No secrets or generated files are committed.
