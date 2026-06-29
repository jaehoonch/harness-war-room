# Harness War Room

A multi-agent app where specialized agents collaborate live to turn a customer incident or feature ask into a real code diff backed by a passing test, while the harness loop runs visibly on screen.

## Language

**War Room**:
A single end-to-end run that takes one ask and drives it through the agent loop to a verified diff.
_Avoid_: Session, job, pipeline

**Ask**:
The user-provided incident report or feature request that starts a War Room run.
_Avoid_: Ticket, prompt, request

**Agent**:
A specialized Microsoft Agent Framework worker with one job: Triage, Repro, Fix, or Review.
_Avoid_: Bot, worker, persona

**Triage**:
The agent that classifies the Ask and locates the relevant files in the Demo Repo.
_Avoid_: Classifier, router

**Repro**:
The agent that writes a failing test reproducing the Ask.
_Avoid_: Reproducer, tester

**Fix**:
The agent that produces a diff to make the failing test pass.
_Avoid_: Patcher, coder

**Review**:
The stronger-model agent that issues a pass/fail verdict and checks guardrails on the diff.
_Avoid_: Approver, judge

**Supervisor**:
The deterministic, non-LLM orchestrator that enforces the loop, runs tests between steps, and re-loops Fix→Review until green.
_Avoid_: Orchestrator agent, controller

**Test-gated handoff**:
A transition between agents that only proceeds after tests run and meet expectations.
_Avoid_: Manual handoff, soft handoff

**Demo Repo**:
The small curated buggy project the agents operate on; bundled in the workspace for deterministic runs.
_Avoid_: Target repo, sample

**Sandbox**:
The isolated, no-network, copy-on-run subprocess where generated code and tests execute.
_Avoid_: Runner, executor

**AG-UI**:
The open agent↔UI event protocol that carries every War Room run to the frontend, driving both timeline and chat from one stream.
_Avoid_: SSE schema, custom protocol
