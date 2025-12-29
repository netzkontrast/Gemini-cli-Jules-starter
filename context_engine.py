import os
import yaml
import toml
import json
import datetime
import sys

class HistoryLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.history_file = os.path.join(log_dir, "history.json")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump([], f)

    def log_interaction(self, user_input, full_context, response, rating, comment):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "input": user_input,
            "context_snapshot_len": len(full_context),
            "response": response,
            "feedback": {
                "rating": rating,
                "comment": comment
            }
        }

        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []

        history.append(entry)

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"\n[System] Interaction logged to {self.history_file}")

class MarkdownLoader:
    def _parse_frontmatter(self, filepath):
        with open(filepath, 'r') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return {"metadata": metadata, "body": body, "path": filepath}
            except yaml.YAMLError as e:
                return {"error": str(e), "path": filepath}
        else:
             return {"error": "No YAML frontmatter found", "path": filepath}

class SkillLoader(MarkdownLoader):
    def __init__(self, skills_dir="skills"):
        self.skills_dir = skills_dir

    def load_skills(self):
        skills = []
        if not os.path.exists(self.skills_dir):
            return skills

        for root, dirs, files in os.walk(self.skills_dir):
            for file in files:
                if file == "SKILL.md":
                    filepath = os.path.join(root, file)
                    result = self._parse_frontmatter(filepath)
                    result["type"] = "skill"
                    skills.append(result)
        return skills

class AgentLoader(MarkdownLoader):
    def __init__(self, agents_dir="agents"):
        self.agents_dir = agents_dir

    def load_agents(self):
        agents = []
        if not os.path.exists(self.agents_dir):
            return agents

        for root, dirs, files in os.walk(self.agents_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    result = self._parse_frontmatter(filepath)
                    result["type"] = "agent"
                    agents.append(result)
        return agents

class WorkflowLoader(MarkdownLoader):
    def __init__(self, workflows_dir="workflows"):
        self.workflows_dir = workflows_dir

    def load_workflows(self):
        workflows = []
        if not os.path.exists(self.workflows_dir):
            return workflows

        for root, dirs, files in os.walk(self.workflows_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    result = self._parse_frontmatter(filepath)
                    # Often workflows in the input don't have frontmatter, they are just MD.
                    # If error "No YAML frontmatter found", we treat the whole content as body.
                    if "error" in result and "No YAML frontmatter" in result["error"]:
                        with open(filepath, 'r') as f:
                            body = f.read()
                        result = {"type": "workflow", "metadata": {"name": os.path.basename(file)}, "body": body, "path": filepath}
                    else:
                        result["type"] = "workflow"
                    workflows.append(result)
        return workflows

class CommandLoader:
    def __init__(self, commands_dir="commands"):
        self.commands_dir = commands_dir

    def load_commands(self):
        commands = []
        if not os.path.exists(self.commands_dir):
            return commands

        for root, dirs, files in os.walk(self.commands_dir):
            for file in files:
                if file.endswith(".toml"):
                    filepath = os.path.join(root, file)
                    try:
                        data = toml.load(filepath)
                        commands.append({"type": "command", "data": data, "path": filepath})
                    except Exception as e:
                        print(f"Error parsing TOML in {filepath}: {e}")
        return commands

class ContextAssembler:
    def __init__(self, context_dir="context", state_dir="state"):
        self.context_dir = context_dir
        self.state_dir = state_dir

    def get_project_context(self):
        context = ""
        if os.path.exists(self.context_dir):
            # Load all .md files in context dir
            for root, dirs, files in os.walk(self.context_dir):
                for file in files:
                    if file.endswith(".md"):
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r') as f:
                            context += f"\n--- {file} ---\n{f.read()}\n"
        return context

    def get_workflow_state(self):
        state = ""
        if os.path.exists(self.state_dir):
            for file in ["PLAN.md", "TODO.md"]:
                filepath = os.path.join(self.state_dir, file)
                if os.path.exists(filepath):
                    with open(filepath, 'r') as f:
                        state += f"\n--- {file} ---\n{f.read()}\n"
        return state

class ContextEngine:
    def __init__(self):
        self.skill_loader = SkillLoader()
        self.agent_loader = AgentLoader()
        self.workflow_loader = WorkflowLoader()
        self.command_loader = CommandLoader()
        self.assembler = ContextAssembler()
        self.logger = HistoryLogger()
        self.workspace_path = os.getcwd()

    def _resolve_variables(self, text):
        """Resolves ${variable} placeholders."""
        if not isinstance(text, str):
            return text
        return text.replace("${workspacePath}", self.workspace_path)

    def _fill_args(self, text, user_input):
        if not isinstance(text, str):
            return text
        return text.replace("{{args}}", user_input)

    def build_context(self, user_input):
        skills = self.skill_loader.load_skills()
        agents = self.agent_loader.load_agents()
        workflows = self.workflow_loader.load_workflows()
        commands = self.command_loader.load_commands()

        project_context = self.assembler.get_project_context()
        workflow_state = self.assembler.get_workflow_state()

        # Apply Variable Resolution
        project_context = self._resolve_variables(project_context)
        workflow_state = self._resolve_variables(workflow_state)

        full_context = f"""
# System Instructions
You are an intelligent agent operating within the Gemini Framework.
Use the provided Context, Skills, Commands, Agents, and Workflows to fulfill the user request.

## User Request
{user_input}

## Project Context
{project_context}

## Workflow State
{workflow_state}

## Available Agents (Personas)
"""
        for agent in agents:
            if "metadata" in agent:
                name = agent['metadata'].get('name', 'Unknown')
                desc = agent['metadata'].get('description', '')
                desc = self._resolve_variables(desc)
                full_context += f"- {name}: {desc}\n"

        full_context += "\n## Available Workflows\n"
        for wf in workflows:
             # Workflows might not have metadata if no frontmatter
             if "metadata" in wf:
                 name = wf['metadata'].get('name', os.path.basename(wf['path']))
                 full_context += f"- {name}\n"

        full_context += "\n## Available Skills\n"
        for skill in skills:
            if "metadata" in skill:
                name = skill['metadata'].get('name', 'Unknown')
                desc = skill['metadata'].get('description', '')
                desc = self._resolve_variables(desc)
                full_context += f"- {name}: {desc}\n"

        full_context += "\n## Available Commands\n"
        for cmd in commands:
            path = self._resolve_variables(cmd.get('path'))
            full_context += f"- {path}\n"
            if "command" in cmd.get('data', {}):
                 command_str = cmd['data']['command']
                 command_str = self._resolve_variables(command_str)
                 command_str = self._fill_args(command_str, user_input)
                 full_context += f"  Extended: {command_str}\n"

        return full_context

    def simulate_agent_response(self, context):
        print("\n[Thinking...] Analyzing context...")
        return "I have updated the plan and logged the interaction. (SIMULATED RESPONSE)"

    def run_interactive(self):
        print("Welcome to Gemini Agent Orchestrator. Type 'exit' to quit.")
        while True:
            try:
                user_input = input("\nUser> ")
                if user_input.lower() in ["exit", "quit"]:
                    break

                context = self.build_context(user_input)
                # print(f"\n--- DEBUG: Context Length: {len(context)} chars ---")

                # In debug mode, we could print the context
                # print(context)

                response = self.simulate_agent_response(context)
                print(f"\nAgent> {response}")

                # Feedback Loop
                print("\n--- Feedback ---")
                rating = input("Rating (1-5): ")
                comment = input("Comment: ")

                self.logger.log_interaction(user_input, context, response, rating, comment)

            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    engine = ContextEngine()
    if len(sys.argv) > 1:
        # One-shot mode for testing
        ctx = engine.build_context(sys.argv[1])
        print(ctx)
    else:
        engine.run_interactive()
