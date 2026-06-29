"""Step functions for one production War Room run.

Each step is small, pure-ish, and seam-injected so it works as a Durable
Functions activity, inside the FastAPI control plane, or under pytest with mocks.
"""
import os


def triage(ticket, agents):
    name = (agents["triage"].run(ticket["ask"]).strip() or ticket["file"])
    return {"type": "step", "role": "triage", "content": f"Mapped to {name}", "file": name}


def repro(ticket, probe):
    path, charged = probe.overcharge(ticket)
    expected = ticket["expected"]
    ok = abs(float(charged) - float(expected)) < 0.005
    return {"type": "step", "role": "repro",
            "content": f"{path} -> {charged}, expected {expected}",
            "passed": ok, "output": f"observed {charged} expected {expected}"}


def fix(ticket, agents, repo, target, loop):
    patch = agents["fix"].run(ticket["ask"])
    repo.patch(target, patch)
    return {"type": "step", "role": "fix", "content": f"Attempt {loop}", "loop": loop, "diff": patch}


def review(agents, result, loop):
    verdict = agents["review"].run(result.output)
    return {"type": "step", "role": "review", "content": verdict,
            "passed": result.passed, "loop": loop, "output": result.output}


def redeploy(repo, deployer, title):
    branch = repo.branch_and_pr(title)
    status = deployer.trigger(branch)
    return {"type": "step", "role": "deploy", "content": f"PR {branch} -> pipeline {status}", "branch": branch}


def make_default_agents():
    from agents import make_agent

    return {r: make_agent(r) for r in ("triage", "repro", "fix", "review")}
