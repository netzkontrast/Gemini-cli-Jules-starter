---
name: sdd
description: Specification-Driven Development (SDD) workflow for Gemini. Provides a structured approach to feature development from specification to documentation.
---

<objective>
This skill implements the Spec-Driven Development (SDD) workflow, guiding developers through a structured process of specification, planning, implementation, and documentation. It ensures that features are well-defined and architected before code is written.
</objective>

<commands>
- `/sdd:00-setup`: Create or update the project constitution.
- `/sdd:01-specify`: Create or update the feature specification.
- `/sdd:02-plan`: Plan the feature development based on the specification.
- `/sdd:03-tasks`: Generate actionable tasks from the plan.
- `/sdd:04-implement`: Execute the implementation plan.
- `/sdd:05-document`: Document the completed feature.
</commands>

<workflow>
1.  **Setup**: Establish project principles with `/sdd:00-setup`.
2.  **Specify**: Define the feature with `/sdd:01-specify`.
3.  **Plan**: Architect the solution with `/sdd:02-plan`.
4.  **Tasks**: Break down into tasks with `/sdd:03-tasks`.
5.  **Implement**: Write code with `/sdd:04-implement`.
6.  **Document**: Update docs with `/sdd:05-document`.
</workflow>
