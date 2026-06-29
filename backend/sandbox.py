"""Isolated test runner for agent-generated code.

Copies the target repo to a throwaway dir and runs pytest in a subprocess
with no network access and a hard timeout. Never executes code in-process.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass


@dataclass
class SandboxResult:
    passed: bool
    output: str


def run_tests(repo_dir: str, timeout: int = 30) -> SandboxResult:
    work = tempfile.mkdtemp(prefix="warroom-")
    dest = os.path.join(work, "repo")
    shutil.copytree(repo_dir, dest)
    env = {
        "PATH": os.environ.get("PATH", ""),
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        "no_proxy": "*",
        "HTTP_PROXY": "http://127.0.0.1:0",
        "HTTPS_PROXY": "http://127.0.0.1:0",
    }
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=dest,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return SandboxResult(passed=proc.returncode == 0, output=proc.stdout + proc.stderr)
    except subprocess.TimeoutExpired:
        return SandboxResult(passed=False, output="timeout")
    finally:
        shutil.rmtree(work, ignore_errors=True)
