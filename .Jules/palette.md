## 2024-05-23 - CLI UX Feedback Loops
**Learning:** CLI tools often neglect intermediate feedback. In `context-flow`, basic `print` statements were used for success/failure, making it hard to distinguish between system output and actual content.
**Action:** Use `click.secho` with color coding (Green for success, Red for errors, Blue for info) to establish a clear visual hierarchy. Distinguish "metadata" output (e.g., "Executing...") from "content" output (the prompt itself).
