"""Deterministic Supervisor: enforces the Triage->Repro->Fix->Review loop.

Runs the sandbox between steps and re-loops Fix->Review until the tests pass
or max_loops is reached. Agents are LLM-backed; the Supervisor is plain code.
"""
import os

from sandbox import run_tests


def _event(etype, role, content, **extra):
    return {"type": etype, "role": role, "content": content, **extra}


def run_war_room(ask, repo_dir, agents=None, max_loops=3):
    if agents is None:
        from agents import make_agent

        agents = {r: make_agent(r) for r in ("triage", "repro", "fix", "review")}

    target_name = agents["triage"].run(ask).strip() or "order_service.py"
    target = os.path.join(repo_dir, target_name)
    test_path = "test_" + target_name
    yield _event("step", "triage", target_name, file=target_name)
    yield _event("step", "repro", agents["repro"].run(ask))

    passed = False
    for loop in range(1, max_loops + 1):
        patch = agents["fix"].run(ask)
        with open(target, "w") as fh:
            fh.write(patch)
        yield _event("step", "fix", patch, loop=loop, diff=patch)
        result = run_tests(repo_dir, test_path=test_path)
        verdict = agents["review"].run(result.output)
        yield _event("step", "review", verdict, passed=result.passed, loop=loop, output=result.output)
        if result.passed:
            passed = True
            break

    yield _event("finished", "supervisor", "done", passed=passed)
