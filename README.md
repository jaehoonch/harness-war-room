# ⚡ Harness War Room

Multi-agent app where **Triage → Repro → Fix → Review** agents collaborate live to turn a customer ask into a real code diff backed by a passing test — the harness loop running visibly on screen.

## Run locally

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
DEMO_MODE=1 python -m uvicorn app:app --app-dir backend --port 8088
# open http://127.0.0.1:8088
```

`DEMO_MODE=1` replays a recorded run (no Azure keys). For live agents set
`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, or `USE_FOUNDRY_AGENT=1` + `AZURE_AI_FOUNDRY_ENDPOINT`.

## Test

```bash
pytest backend/tests -q
```

## Architecture

- **Supervisor** (code) enforces test-gated handoffs, re-loops Fix→Review until green.
- **Agents** (Microsoft Agent Framework, Azure AI Foundry): gpt-4o-mini workers, gpt-4o reviewer.
- **Sandbox**: no-network copy-on-run subprocess pytest.
- **AG-UI** events streamed over SSE; vanilla JS timeline + chat.
- **Deploy**: GitHub → Azure DevOps → ACR → Azure Container Apps.

See `docs/` for the glossary and ADRs. Built with GitHub Copilot harness skills.
