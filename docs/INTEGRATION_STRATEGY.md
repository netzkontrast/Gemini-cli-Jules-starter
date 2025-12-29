# Context Flow: Integration Strategy

This document outlines the conceptual architecture for integrating high-value patterns from **mdflow**, **Context Engineering Kit (CEK)**, **Continuous Claude**, and the **Origami Thought Protocol** into the `context-flow-cli` tool.

## 1. High-Level Architecture

`context-flow-cli` acts as the **Orchestrator** and **Session Manager**. It does not replace `mdflow` but wraps it to provide structured workflows (Origami), persistent memory (Continuous Claude), and specialized capabilities (CEK).

```mermaid
graph TD
    User[User] -->|Start Task| CLI[Context Flow CLI]

    subgraph "Orchestrator (Context Flow)"
        Protocol[Origami Protocol Engine]
        State[State Manager]
        SkillLoader[Skill Loader]
    end

    subgraph "Resources"
        CEK[CEK Marketplace]
        Templates[Local Templates]
    end

    subgraph "Execution Layer"
        MDFlow[mdflow CLI]
        LLM[Claude / LLM]
    end

    subgraph "Memory Layer (Continuous Claude)"
        Ledger[Session Ledger]
        Handoffs[Handoffs]
        Artifacts[Artifact Index (SQLite)]
    end

    CLI --> Protocol
    Protocol -->|Request Skill| SkillLoader
    SkillLoader -->|Fetch| CEK
    Protocol -->|Update| State
    State -->|Write| Ledger
    State -->|Write| Handoffs

    Protocol -->|Generate Prompt| MDFlow
    MDFlow -->|Run| LLM
```

## 2. Integration by Component

### A. Execution Layer: `mdflow`
**Concept:** The "Engine".
*   **Role:** Handles the actual LLM interaction, tool execution, and prompt rendering.
*   **Integration Strategy:**
    *   `context-flow` generates `.md` files that are fully compatible with `mdflow`.
    *   **Optimization:** Instead of just generating files, `context-flow` can include a `run` command that invokes `mdflow` via subprocess, capturing output to update the Session Ledger automatically.
    *   **Config:** `context-flow init` generates a `.mdflow/config.yaml` optimized for the specific project type.

### B. Skill & Agent Registry: `Context Engineering Kit` (CEK)
**Concept:** The "Library".
*   **Role:** Provides the *content* of the prompts and the definition of specialized agents (e.g., `bug-hunter`, `code-architect`).
*   **Integration Strategy:**
    *   **Plugin System:** Implement a command `context-flow install <skill>` that mimics CEK's loader.
    *   **Structure Mapping:**
        *   CEK `plugins/` -> `my-project/skills/`
        *   CEK `agents/` -> `my-project/agents/`
    *   **Adaptation:** CEK skills often use specific slash commands (`/reflexion:reflect`). `context-flow` should generate mdflow-compatible aliases or wrapper scripts so these work natively within the generated markdown prompts.

### C. State & Memory: `Continuous Claude`
**Concept:** The "Memory".
*   **Role:** Ensures context isn't lost between steps or sessions.
*   **Integration Strategy:**
    *   **Directory Structure:** We have already adopted `thoughts/ledgers` and `thoughts/handoffs`.
    *   **Hooks Implementation:**
        *   **Pre-Session:** `context-flow start` acts as the *SessionStart* hook, loading the last Handoff + Ledger into the new prompt's Context section.
        *   **Post-Session:** A `context-flow wrap-up` command (or an `mdflow` post-run script) acts as the *SessionEnd* hook, summarizing the session into a Handoff markdown file.
    *   **Artifact Index:** Future implementation of a lightweight SQLite DB to index these markdown files for RAG (retrieval-augmented generation), allowing agents to "recall" past decisions.

### D. Workflow Logic: `Origami Thought Protocol`
**Concept:** The "Brain".
*   **Role:** Defines the *sequence* of operations.
*   **Integration Strategy:**
    *   **State Machine:** Implement a Python state machine in the CLI.
        *   *State 1: Decomposition* (Generates `00_decomp.md`)
        *   *State 2: Validation* (Parses output of Decomp, generates `01_valid.md`)
        *   *State 3: Evaluation* (Generates `02_eval.md`)
        *   *State 4: Execution* (Generates task-specific prompts).
    *   **Automation:** The CLI can automatically parse the structured JSON/Markdown output from one step to seed the next, removing manual copy-pasting.

## 3. Recommended Roadmap

1.  **Phase 1 (Current):** Static scaffolding. User manually runs `mdflow` on generated files.
2.  **Phase 2 (Skill Loader):** Implement `context-flow install` to fetch raw skill files from the CEK repo (or a local copy) and convert them to Jinja2 templates.
3.  **Phase 3 (Active State Management):**
    *   Implement `context-flow update-ledger` to parse the last session's output and update the `thoughts/ledgers/*.md` file.
    *   Implement `context-flow handoff` to archive the current session.
4.  **Phase 4 (Origami Automation):**
    *   Modify `00_origami_decomposition.md` to output JSON.
    *   Update `context-flow start` to detect if step 00 is done, and if so, automatically generate step 01 using that JSON output.
