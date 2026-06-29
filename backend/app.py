"""FastAPI app streaming AG-UI events from the War Room run."""
import json
import os
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from agui import to_agui

DEMO = Path(__file__).resolve().parents[1] / "demo_repo"
FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
app = FastAPI()


def _internal_events(ask):
    if os.environ.get("DEMO_MODE") == "1":
        from replay import REPLAY

        yield from REPLAY
        return
    from supervisor import run_war_room

    work = tempfile.mkdtemp(prefix="run-")
    repo = os.path.join(work, "repo")
    shutil.copytree(DEMO, repo)
    try:
        yield from run_war_room(ask, repo)
    finally:
        shutil.rmtree(work, ignore_errors=True)


@app.get("/api/run")
def run(ask: str):
    def stream():
        for ev in to_agui(_internal_events(ask)):
            yield f"data: {json.dumps(ev)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory=str(FRONTEND), html=True), name="ui")
