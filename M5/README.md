# M5: Analysis Agent & Decision Agent

**Project:** AI Agent Coordination & Decision Engine

## Overview

Module M5 implements two agents that convert research data into actionable business recommendations.

### 1. Analysis Agent
- Analyzes incoming research data.
- Identifies business problems.
- Extracts key findings and trends.
- Produces structured, schema-validated analysis results.

### 2. Decision Agent
- Evaluates available business options.
- Scores options on benefit, cost, and risk.
- Normalizes option scores for comparison.
- Recommends the highest-scoring option.
- Generates decision reasoning.

### 3. M3 Tools Integration

The Decision Agent uses the shared M3 `compare_options()` utility for weighted option comparison.

### 4. Common Agent Contract

Both agents implement the standard `execute()` method and return an `AgentResponse`.

## Project Structure

| File | Description |
|---|---|
| `analysis_agent.py` | Analysis Agent implementation |
| `decision_agent.py` | Decision Agent implementation |
| `schemas.py` | Pydantic input and output schemas |
| `main.py` | Standalone execution entry point |
| `test_analysis.py` | Analysis Agent tests |
| `test_decision.py` | Decision Agent tests |

## Setup

### 1. Activate virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install required packages

```bash
python -m pip install pydantic pytest
```

## Usage

Run the Decision Agent:

```bash
python M5/decision_agent.py
```

## Testing

Run tests from the project root:

```bash
python -m pytest M5 M3_Tools -v
```

### Test Results

| Component | Tests Passed |
|---|---:|
| Analysis Agent | 3 |
| Decision Agent | 9 |
| M3 Tools | 9 |
| **Total** | **21** |

## Integration Status

| Component | Status |
|---|---|
| Analysis Agent | Completed |
| Decision Agent | Completed |
| M3 Tools Integration | Completed |
| Shared Schema Approval | Pending M7 confirmation |
| LangGraph Workflow Integration | Pending M7 integration |