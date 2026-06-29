"""FastAPI app streaming AG-UI events from the War Room run."""
import json
import os
import shutil
import tempfile
from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from agui import to_agui
from tickets import TICKETS, chat, get_ticket

DEMO = Path(__file__).resolve().parents[1] / "demo_repo"
FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
app = FastAPI()


def _internal_events(ask, ticket=None):
    if os.environ.get("DEMO_MODE") == "1":
        from replay import DEFAULT, REPLAYS

        yield from REPLAYS.get(ticket or DEFAULT, REPLAYS[DEFAULT])
        return
    from supervisor import run_war_room

    work = tempfile.mkdtemp(prefix="run-")
    repo = os.path.join(work, "repo")
    shutil.copytree(DEMO, repo)
    try:
        yield from run_war_room(ask, repo)
    finally:
        shutil.rmtree(work, ignore_errors=True)


@app.get("/api/tickets")
def tickets():
    return TICKETS


@app.get("/api/chat")
def ticket_chat(ticket: str = "", q: str = ""):
    return {"reply": chat(ticket, q)}


@app.get("/api/start")
def start(ticket: str = ""):
    base = os.environ.get("DURABLE_BASE_URL", "").rstrip("/")
    r = httpx.get(f"{base}/api/start", params={"ticket": ticket}, timeout=30)
    return r.json()


@app.get("/api/status")
def status(url: str = ""):
    r = httpx.get(url, timeout=30)
    return r.json()


@app.get("/api/run")
def run(ask: str = "", ticket: str = ""):
    t = get_ticket(ticket)
    if t:
        ask = ask or t["ask"]

    def stream():
        for ev in to_agui(_internal_events(ask, ticket or None)):
            yield f"data: {json.dumps(ev)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory=str(FRONTEND), html=True), name="ui")
