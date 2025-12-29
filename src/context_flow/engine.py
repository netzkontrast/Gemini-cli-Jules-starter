import os
import yaml
import re
from pathlib import Path
from typing import Dict, Any, List

class ContextEngine:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.skills_dir = self.root_dir / "src/context_flow/skills"
        self.commands_dir = self.root_dir / "src/context_flow/commands"
        self.agents_dir = self.root_dir / "src/context_flow/agents"

    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """Parses YAML frontmatter from a markdown string."""
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
        return {}

    def _parse_body(self, content: str) -> str:
        """Parses the body content, removing frontmatter."""
        return re.sub(r"^---\n(.*?)\n---\n", "", content, count=1, flags=re.DOTALL)

    def load_skill(self, skill_name: str) -> Dict[str, Any]:
        """Loads a skill definition."""
        skill_path = self.skills_dir / skill_name / "SKILL.md"
        if not skill_path.exists():
            raise FileNotFoundError(f"Skill '{skill_name}' not found at {skill_path}")

        content = skill_path.read_text()
        metadata = self._parse_frontmatter(content)
        body = self._parse_body(content)

        return {
            "metadata": metadata,
            "body": body,
            "type": "skill"
        }

    def load_command(self, command_name: str) -> Dict[str, Any]:
        """Loads a command definition."""
        # Handle SDD commands which are nested
        if command_name.startswith("sdd:"):
            cmd_file = command_name.split(":")[1]
            command_path = self.commands_dir / "sdd" / f"{cmd_file}.md"
        else:
            command_path = self.commands_dir / f"{command_name}.md"

        if not command_path.exists():
             raise FileNotFoundError(f"Command '{command_name}' not found at {command_path}")

        content = command_path.read_text()
        metadata = self._parse_frontmatter(content)
        body = self._parse_body(content)

        return {
            "metadata": metadata,
            "body": body,
            "type": "command"
        }

    def load_agent(self, agent_name: str) -> Dict[str, Any]:
        """Loads an agent definition."""
        agent_path = self.agents_dir / f"{agent_name}.md"
        if not agent_path.exists():
            raise FileNotFoundError(f"Agent '{agent_name}' not found at {agent_path}")

        content = agent_path.read_text()
        metadata = self._parse_frontmatter(content)
        body = self._parse_body(content)

        return {
            "metadata": metadata,
            "body": body,
            "type": "agent"
        }

    def execute(self, entity_type: str, name: str, arguments: str = "") -> str:
        """Simulates execution by returning the prompt with arguments substituted."""
        if entity_type == "skill":
            data = self.load_skill(name)
        elif entity_type == "command":
            data = self.load_command(name)
        elif entity_type == "agent":
            data = self.load_agent(name)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")

        prompt = data["body"]

        # Simple argument substitution (mimicking the behavior described in docs)
        if "$ARGUMENTS" in prompt:
            prompt = prompt.replace("$ARGUMENTS", arguments)

        # Positional arguments $1, $2, etc.
        args_list = arguments.split()
        for i, arg in enumerate(args_list):
            prompt = prompt.replace(f"${i+1}", arg)

        return f"Executing {entity_type} '{name}' with prompt:\n\n{prompt}"
