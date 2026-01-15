"""Shared pytest fixtures for all tests."""

import json
import shutil
import subprocess
import tempfile
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator, Set, List, Optional

import pytest


@pytest.fixture
def project_root() -> Path:
    """Return the actual project root."""
    return Path(__file__).parent.parent


@pytest.fixture
def logs_dir(project_root: Path) -> Path:
    """Return the logs directory."""
    return project_root / ".claude" / "logs"


@pytest.fixture
def agent_log_path(logs_dir: Path) -> Path:
    """Return the agent invocations log path."""
    return logs_dir / "agent-invocations.log"


@pytest.fixture
def skill_log_path(logs_dir: Path) -> Path:
    """Return the skill invocations log path."""
    return logs_dir / "skill-invocations.log"


@pytest.fixture
def temp_project_dir() -> Generator[Path, None, None]:
    """Create a temporary project directory with minimal structure."""
    temp_dir = Path(tempfile.mkdtemp())

    # Create required directories
    (temp_dir / "agents").mkdir()
    (temp_dir / "skills").mkdir()
    (temp_dir / "commands").mkdir()
    (temp_dir / "agents-available" / "dev").mkdir(parents=True)
    (temp_dir / "skills-available" / "dev").mkdir(parents=True)
    (temp_dir / "commands-available" / "dev").mkdir(parents=True)
    (temp_dir / "hooks").mkdir()

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_project_config() -> dict:
    """Return a sample project configuration."""
    return {
        "name": "test-project",
        "categories": ["dev"],
        "exclude": [],
        "description": "Test project for unit tests"
    }


def get_active_agents(project_root: Path) -> Set[str]:
    """Get set of active agent names."""
    agents_dir = project_root / "agents"
    if not agents_dir.exists():
        return set()

    return {
        item.stem for item in agents_dir.iterdir()
        if item.is_symlink() and item.suffix == ".md"
    }


def get_active_skills(project_root: Path) -> Set[str]:
    """Get set of active skill names."""
    skills_dir = project_root / "skills"
    if not skills_dir.exists():
        return set()

    return {
        item.name for item in skills_dir.iterdir()
        if item.is_symlink()
    }


def get_active_commands(project_root: Path) -> Set[str]:
    """Get set of active command names."""
    commands_dir = project_root / "commands"
    if not commands_dir.exists():
        return set()

    return {
        item.stem for item in commands_dir.iterdir()
        if item.suffix == ".md"
    }


def parse_log_entries(log_file: Path, minutes: int = 30) -> List[dict]:
    """Parse log entries from the last N minutes."""
    if not log_file.exists():
        return []

    cutoff = datetime.now() - timedelta(minutes=minutes)
    entries = []

    with open(log_file) as f:
        for line in f:
            match = re.match(
                r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\S+)",
                line
            )
            if match:
                try:
                    log_time = datetime.strptime(
                        match.group(1), "%Y-%m-%d %H:%M:%S"
                    )
                    if log_time >= cutoff:
                        entries.append({
                            "timestamp": log_time,
                            "name": match.group(2),
                            "line": line.strip()
                        })
                except ValueError:
                    pass

    return entries


def invoke_claude_with_prompt(prompt: str, timeout: int = 60, cwd: Optional[Path] = None) -> dict:
    """
    Invoke Claude CLI with a prompt and return the result.

    Args:
        prompt: The prompt to send to Claude
        timeout: Timeout in seconds
        cwd: Working directory for the command

    Returns:
        dict with keys: success, stdout, stderr, returncode
    """
    cmd = [
        "claude",
        "-p", prompt,
        "--dangerously-skip-permissions",
        "--output-format", "text"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Command timed out after {timeout}s",
            "returncode": -1
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }


def check_agent_invoked(agent_name: str, log_path: Path, since: datetime) -> bool:
    """Check if an agent was invoked after a given time."""
    if not log_path.exists():
        return False

    with open(log_path) as f:
        for line in f:
            if agent_name in line:
                match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                if match:
                    try:
                        log_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                        if log_time >= since:
                            return True
                    except ValueError:
                        pass
    return False


def check_skill_invoked(skill_name: str, log_path: Path, since: datetime) -> bool:
    """Check if a skill was invoked after a given time."""
    if not log_path.exists():
        return False

    with open(log_path) as f:
        for line in f:
            if skill_name in line:
                match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                if match:
                    try:
                        log_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                        if log_time >= since:
                            return True
                    except ValueError:
                        pass
    return False
