# Git and GitHub Workflow

## 1. Purpose
This document defines a simple team workflow for eight contributors. The project specification recommends feature branches and reviewed pull requests. The `main` branch is the stable branch; a separate `develop` branch is optional if the team decides it is useful.

## 2. Branch model
- `main`: stable, reviewed project version.
- `feature/<short-description>`: one focused development task.
- `fix/<short-description>`: one focused defect fix.
- `docs/<short-description>`: documentation-only changes.

Suggested member branches:
| Member | Suggested branch |
|---|---|
| M1 | `feature/project-architecture` |
| M2 | `feature/llm-base-agent` |
| M3 | `feature/tool-integration` |
| M4 | `feature/planning-research-agents` |
| M5 | `feature/analysis-decision-agents` |
| M6 | `feature/memory-management` |
| M7 | `feature/orchestration-backend` |
| M8 | `feature/frontend-deployment` |

A branch is a working branch, not a permanent personal copy. Create focused branches for separate tasks when practical.

## 3. Initial setup
```bash
git clone <repository-url>
cd <repository-folder>
git checkout main
git pull origin main
git checkout -b feature/project-architecture
```

## 4. Daily workflow
```bash
git status
git add docs/
git commit -m "docs(m1): add project architecture documents"
git push -u origin feature/project-architecture
```

Use `git add <specific-files>` rather than adding everything blindly.

## 5. Pull request process
1. Push the feature branch.
2. Open a pull request targeting `main` (or `develop` if the team has adopted it).
3. Explain the purpose and link the related task/issue.
4. Describe tests performed.
5. Request at least one teammate review.
6. Resolve review comments.
7. Merge only after approval and required checks pass.
8. Delete the merged branch if it is no longer needed.

## 6. Commit message format
Use a short type and description:
- `docs: add system architecture`
- `feat(agent): add research agent`
- `fix(api): handle invalid workflow request`
- `test: add workflow contract tests`
- `chore: update development dependencies`

## 7. Pull request checklist
- [ ] PR explains its purpose and links to the task/issue.
- [ ] Changes are limited to the intended task.
- [ ] Tests have been added or updated and run locally.
- [ ] API, agent or database contract changes are documented.
- [ ] No `.env`, passwords, API keys, virtual environments or generated databases are committed.
- [ ] At least one teammate has reviewed the PR.
- [ ] CI checks pass, if configured.
- [ ] Setup instructions or module documentation are updated if needed.

## 8. Team collaboration rules
1. Do not push directly to `main`.
2. Pull the latest base branch before starting work.
3. Use small, focused feature branches and pull requests.
4. Discuss changes to shared contracts before coding against them.
5. Do not overwrite another contributor's work.
6. Resolve merge conflicts carefully and run tests afterward.
7. Keep commits meaningful and avoid generated files or secrets.
8. For a small team, merging reviewed feature branches directly into `main` is sufficient; add `develop` only if the team agrees.
