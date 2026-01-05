#!/usr/bin/env python3
"""
List all available Claude Code agents.

This script scans the .claude/agents/ directory and displays information
about all available agents.
"""

import argparse
import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class AgentInfo:
    """Information about a Claude Code agent."""
    name: str
    filename: str
    expertise: str
    capabilities: List[str]


def parse_agent_file(filepath: Path) -> Optional[AgentInfo]:
    """
    Parse an agent markdown file to extract information.

    Args:
        filepath: Path to the agent markdown file

    Returns:
        AgentInfo object or None if parsing fails
    """
    try:
        content = filepath.read_text()

        # Extract agent name from the first heading
        name_match = re.search(r'^#\s+(.+?)(?:\s+Agent)?$', content, re.MULTILINE)
        name = name_match.group(1) if name_match else filepath.stem.replace('-agent', '').title()

        # Extract expertise from "Your Role" or "Expertise" section
        expertise_match = re.search(
            r'(?:##\s+Your Role|expertise)[\s\S]*?:\s*(.+?)(?:\n|$)',
            content,
            re.IGNORECASE
        )
        expertise = expertise_match.group(1).strip() if expertise_match else "No description available"

        # Extract capabilities from "Capabilities" section
        capabilities = []
        capabilities_section = re.search(
            r'##\s+Capabilities\s*\n([\s\S]*?)(?=\n##|\Z)',
            content,
            re.MULTILINE
        )

        if capabilities_section:
            # Find all bullet points or numbered items
            cap_matches = re.findall(r'[-*]\s+(.+?)(?:\n|$)', capabilities_section.group(1))
            capabilities = [cap.strip() for cap in cap_matches[:5]]  # Limit to 5

        return AgentInfo(
            name=name,
            filename=filepath.name,
            expertise=expertise,
            capabilities=capabilities
        )

    except Exception as e:
        print(f"Warning: Failed to parse {filepath.name}: {e}")
        return None


def find_agents(agents_dir: Path) -> List[AgentInfo]:
    """
    Find all agent markdown files in the agents directory.

    Args:
        agents_dir: Path to the .claude/agents directory

    Returns:
        List of AgentInfo objects
    """
    agents = []

    if not agents_dir.exists():
        print(f"Error: Agents directory not found: {agents_dir}")
        return agents

    for agent_file in sorted(agents_dir.glob("*.md")):
        agent_info = parse_agent_file(agent_file)
        if agent_info:
            agents.append(agent_info)

    return agents


def format_table(agents: List[AgentInfo]) -> str:
    """
    Format agents as a table.

    Args:
        agents: List of AgentInfo objects

    Returns:
        Formatted table string
    """
    if not agents:
        return "No agents found."

    # Calculate column widths
    name_width = max(len(agent.name) for agent in agents)
    name_width = max(name_width, len("Agent Name"))

    expertise_width = max(len(agent.expertise) for agent in agents)
    expertise_width = max(expertise_width, len("Expertise"))
    expertise_width = min(expertise_width, 50)  # Cap width

    # Build table
    lines = []
    separator = f"┌─{'─' * name_width}─┬─{'─' * expertise_width}─┐"
    header = f"│ {'Agent Name':<{name_width}} │ {'Expertise':<{expertise_width}} │"
    divider = f"├─{'─' * name_width}─┼─{'─' * expertise_width}─┤"

    lines.append(separator)
    lines.append(header)
    lines.append(divider)

    for agent in agents:
        # Truncate expertise if too long
        expertise = agent.expertise
        if len(expertise) > expertise_width:
            expertise = expertise[:expertise_width-3] + "..."

        row = f"│ {agent.name:<{name_width}} │ {expertise:<{expertise_width}} │"
        lines.append(row)

    bottom = f"└─{'─' * name_width}─┴─{'─' * expertise_width}─┘"
    lines.append(bottom)

    return "\n".join(lines)


def format_detailed(agents: List[AgentInfo]) -> str:
    """
    Format agents with detailed information.

    Args:
        agents: List of AgentInfo objects

    Returns:
        Formatted detailed string
    """
    if not agents:
        return "No agents found."

    lines = []
    for i, agent in enumerate(agents, 1):
        lines.append(f"\n{i}. {agent.name}")
        lines.append(f"   File: {agent.filename}")
        lines.append(f"   Expertise: {agent.expertise}")

        if agent.capabilities:
            lines.append("   Capabilities:")
            for cap in agent.capabilities:
                lines.append(f"     • {cap}")

    return "\n".join(lines)


def format_json_output(agents: List[AgentInfo]) -> str:
    """
    Format agents as JSON.

    Args:
        agents: List of AgentInfo objects

    Returns:
        JSON string
    """
    return json.dumps([asdict(agent) for agent in agents], indent=2)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="List all available Claude Code agents"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed information including capabilities"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    parser.add_argument(
        "--agents-dir",
        type=Path,
        default=Path(__file__).parent.parent / ".claude" / "agents",
        help="Path to agents directory (default: .claude/agents)"
    )

    args = parser.parse_args()

    # Find all agents
    agents = find_agents(args.agents_dir)

    # Format and display
    if args.json:
        output = format_json_output(agents)
    elif args.detailed:
        output = format_detailed(agents)
    else:
        output = format_table(agents)

    print(output)

    # Only show count for human-readable formats
    if not args.json:
        print(f"\nTotal agents: {len(agents)}")


if __name__ == "__main__":
    main()
