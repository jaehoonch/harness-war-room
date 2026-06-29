"""Map internal Supervisor events to AG-UI protocol events."""

_EXTRA = ("loop", "diff", "output", "file")


def to_agui(events):
    yield {"type": "RUN_STARTED"}
    for e in events:
        if e["type"] == "finished":
            yield {"type": "RUN_FINISHED", "passed": e.get("passed", False), "content": e.get("content", "")}
        else:
            extra = {k: e[k] for k in _EXTRA if k in e}
            yield {"type": "TEXT_MESSAGE", "role": e["role"], "content": e["content"], **extra}
            yield {"type": "STATE_DELTA", "role": e["role"], "passed": e.get("passed")}
