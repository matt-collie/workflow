"""
Tests for the list_agents script.
"""

import json
import tempfile
from pathlib import Path
import pytest

# Import the functions we want to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from list_agents import (
    AgentInfo,
    parse_agent_file,
    find_agents,
    format_table,
    format_detailed,
    format_json_output
)


# Test fixtures

@pytest.fixture
def sample_agent_content():
    """Sample agent markdown content."""
    return """# Research Agent

You are a Research Agent specialized in technical research and investigation.

## Your Role

You help developers research technologies, investigate issues, and gather information for decision-making:
- Technology evaluation and comparison
- Library and framework research

## Capabilities

### Technology Research
- Compare libraries, frameworks, and tools
- Evaluate pros/cons of different approaches
- Research compatibility

### Problem Investigation
- Deep-dive into error messages
- Research known issues
"""


@pytest.fixture
def sample_agent_file(tmp_path, sample_agent_content):
    """Create a temporary agent file."""
    agent_file = tmp_path / "research-agent.md"
    agent_file.write_text(sample_agent_content)
    return agent_file


@pytest.fixture
def agents_directory(tmp_path):
    """Create a temporary agents directory with multiple agents."""
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()

    # Create multiple agent files
    agents = {
        "research-agent.md": """# Research Agent

## Your Role

You help with: Technical research and investigation

## Capabilities

- Technology evaluation
- Library research
""",
        "development-agent.md": """# Development Agent

## Your Role

You assist with: Software development and coding

## Capabilities

- Feature implementation
- Bug fixing
""",
    }

    for filename, content in agents.items():
        (agents_dir / filename).write_text(content)

    return agents_dir


# Tests for parse_agent_file

def test_parse_agent_file_success(sample_agent_file):
    """Test successfully parsing an agent file."""
    agent_info = parse_agent_file(sample_agent_file)

    assert agent_info is not None
    assert agent_info.name == "Research Agent"
    assert agent_info.filename == "research-agent.md"
    assert "research" in agent_info.expertise.lower() or "Technical research" in agent_info.expertise
    assert len(agent_info.capabilities) > 0


def test_parse_agent_file_extracts_capabilities(sample_agent_file):
    """Test that capabilities are extracted from the file."""
    agent_info = parse_agent_file(sample_agent_file)

    assert agent_info is not None
    assert len(agent_info.capabilities) >= 2
    # Check that at least some capabilities were found
    capabilities_text = " ".join(agent_info.capabilities)
    assert any(word in capabilities_text.lower() for word in ["technology", "research", "compare"])


def test_parse_agent_file_missing_file():
    """Test parsing a non-existent file."""
    non_existent = Path("/tmp/does-not-exist.md")
    agent_info = parse_agent_file(non_existent)

    # Should return None or handle gracefully
    assert agent_info is None


# Tests for find_agents

def test_find_agents_success(agents_directory):
    """Test finding agents in a directory."""
    agents = find_agents(agents_directory)

    assert len(agents) == 2
    agent_names = [agent.name for agent in agents]
    assert "Research Agent" in agent_names
    assert "Development Agent" in agent_names


def test_find_agents_empty_directory(tmp_path):
    """Test finding agents in an empty directory."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    agents = find_agents(empty_dir)

    assert len(agents) == 0


def test_find_agents_missing_directory(tmp_path):
    """Test finding agents when directory doesn't exist."""
    missing_dir = tmp_path / "missing"

    agents = find_agents(missing_dir)

    assert len(agents) == 0


# Tests for format_table

def test_format_table_with_agents():
    """Test table formatting with agents."""
    agents = [
        AgentInfo(
            name="Research Agent",
            filename="research-agent.md",
            expertise="Technical research",
            capabilities=["Technology evaluation"]
        ),
        AgentInfo(
            name="Development Agent",
            filename="development-agent.md",
            expertise="Software development",
            capabilities=["Feature implementation"]
        ),
    ]

    output = format_table(agents)

    assert "Research Agent" in output
    assert "Development Agent" in output
    assert "Technical research" in output
    assert "Software development" in output
    assert "┌" in output  # Table border
    assert "│" in output  # Table border


def test_format_table_empty_list():
    """Test table formatting with no agents."""
    output = format_table([])

    assert "No agents found" in output


# Tests for format_detailed

def test_format_detailed_with_agents():
    """Test detailed formatting with agents."""
    agents = [
        AgentInfo(
            name="Research Agent",
            filename="research-agent.md",
            expertise="Technical research",
            capabilities=["Technology evaluation", "Library research"]
        ),
    ]

    output = format_detailed(agents)

    assert "Research Agent" in output
    assert "research-agent.md" in output
    assert "Technical research" in output
    assert "Technology evaluation" in output
    assert "Library research" in output
    assert "Capabilities:" in output


def test_format_detailed_empty_list():
    """Test detailed formatting with no agents."""
    output = format_detailed([])

    assert "No agents found" in output


# Tests for format_json_output

def test_format_json_with_agents():
    """Test JSON formatting with agents."""
    agents = [
        AgentInfo(
            name="Research Agent",
            filename="research-agent.md",
            expertise="Technical research",
            capabilities=["Technology evaluation"]
        ),
    ]

    output = format_json_output(agents)
    data = json.loads(output)

    assert len(data) == 1
    assert data[0]["name"] == "Research Agent"
    assert data[0]["filename"] == "research-agent.md"
    assert data[0]["expertise"] == "Technical research"
    assert "Technology evaluation" in data[0]["capabilities"]


def test_format_json_empty_list():
    """Test JSON formatting with no agents."""
    output = format_json_output([])
    data = json.loads(output)

    assert data == []


# Integration tests

def test_full_workflow(agents_directory):
    """Test the complete workflow from finding to formatting."""
    # Find agents
    agents = find_agents(agents_directory)
    assert len(agents) > 0

    # Test all output formats work
    table_output = format_table(agents)
    assert len(table_output) > 0
    assert "Agent Name" in table_output

    detailed_output = format_detailed(agents)
    assert len(detailed_output) > 0
    assert "Capabilities:" in detailed_output

    json_output = format_json_output(agents)
    json_data = json.loads(json_output)
    assert len(json_data) == len(agents)


# Test AgentInfo dataclass

def test_agent_info_creation():
    """Test creating an AgentInfo object."""
    agent = AgentInfo(
        name="Test Agent",
        filename="test-agent.md",
        expertise="Testing",
        capabilities=["Test 1", "Test 2"]
    )

    assert agent.name == "Test Agent"
    assert agent.filename == "test-agent.md"
    assert agent.expertise == "Testing"
    assert len(agent.capabilities) == 2
