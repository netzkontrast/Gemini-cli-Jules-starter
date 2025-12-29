# Gemini CLI Blueprint Starter

This repository provides a setup for Gemini to use the "Blueprint Extension" workflow locally via a Python CLI tool named `taches`.

## Philosophy

The workflow follows the **PLAN ➡️ DEFINE ➡️ ACT** loop, enforcing a structured approach to software engineering:

1.  **Research/Plan**: Understand the goal.
2.  **Define**: Break it down into atomic tasks.
3.  **Implement**: Execute tasks with state tracking.
4.  **Test**: Verify results.

## Installation

To use the tools locally (or for the Gemini agent to use them):

```bash
pip install -e .
```

## Usage

The `taches` CLI simulates the Blueprint extension commands.

### Blueprint Workflow
- **Plan**: `taches blueprint plan "<goal>"` (Creates `PLAN.md`)
- **Define**: `taches blueprint define` (Creates `TODO.md`)
- **Implement**: `taches blueprint implement "<task>"` (Updates `ACT.md`)
- **Test**: `taches blueprint test`

### Thinking Models
- **Pareto**: `taches consider pareto "<context>"`

## Gemini System Prompt
Refer to `Gemini.md` for the system instructions that guide the AI agent on how to utilize these tools.
