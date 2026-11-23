# Git and GitHub Workflow

## 1. Purpose

This document defines a consistent Git and GitHub workflow for all eight contributors. The project uses feature branches and reviewed pull requests to maintain code quality and prevent conflicts.

The `main` branch is the stable branch. A separate `develop` branch is optional if the team agrees to use it.

## 2. Branch model

- `main`: Stable, reviewed project version.
- `feature/<short-description>`: One focused development task.
- `fix/<short-description>`: One focused defect fix.
- `docs/<short-description>`: Documentation-only changes.

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

Each member should work on their assigned feature branch. Create additional focused branches for separate tasks when practical.

## 3. Initial setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd <repository-folder>
git checkout main
git pull origin main
```

Create or switch to the feature branch assigned to the member:

```bash
git checkout -b feature/<assigned-branch>
```

If the branch already exists remotely:

```bash
git fetch origin
git checkout -b feature/<assigned-branch> origin/feature/<assigned-branch>
```

## 4. Daily workflow

Before starting work:

```bash
git status
git pull origin main
```

Stage only the files related to the current task:

```bash
git add <specific-files>
```

Commit with a meaningful message:

```bash
git commit -m "type: describe the change"
```

Push the feature branch:

```bash
git push -u origin <branch-name>
```

For subsequent pushes, use:

```bash
git push
```

Avoid staging unrelated files or using `git add .` without checking the changes first.

## 5. Pull request process

1. Push the feature branch to GitHub.
2. Open a pull request targeting `main`, or `develop` if the team has adopted it.
3. Explain the purpose of the change and link the related task or issue.
4. Describe tests performed.
5. Request at least one teammate review.
6. Resolve review comments.
7. Merge only after approval and required checks pass.
8. Delete the merged feature branch if it is no longer needed.
9. Update the local base branch after merging.

## 6. Commit message format

Use a short type and clear description:

- `docs: add system architecture`
- `feat(agent): add research agent`
- `fix(api): handle invalid workflow request`
- `test: add workflow contract tests`
- `chore: update development dependencies`

Commit messages should describe the actual change.

## 7. Pull request checklist

- [ ] PR explains its purpose and links to the task or issue.
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
4. Discuss changes to shared contracts with M1 and M7 before coding against them.
5. Do not overwrite another contributor's work.
6. Resolve merge conflicts carefully and run tests afterward.
7. Keep commits meaningful and avoid generated files or secrets.
8. For a small team, merging reviewed feature branches directly into `main` is sufficient; add `develop` only if the team agrees.
9. Notify M1 about integration blockers and shared documentation changes.

## 9. M1 coordination responsibilities

M1 is responsible for:

- Maintaining the shared architecture and project documentation.
- Coordinating repository structure and integration conventions.
- Reviewing changes that affect shared interfaces.
- Monitoring pull requests and integration progress.
- Coordinating system-level testing with component owners.
- Keeping the team informed about integration blockers.