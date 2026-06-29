"""Map internal Supervisor events to AG-UI protocol events."""


def to_agui(events):
    yield {"type": "RUN_STARTED"}
    for e in events:
        if e["type"] == "finished":
            yield {"type": "RUN_FINISHED", "passed": e.get("passed", False)}
        else:
            yield {
                "type": "TEXT_MESSAGE",
                "role": e["role"],
                "content": e["content"],
            }
            yield {"type": "STATE_DELTA", "role": e["role"], "passed": e.get("passed")}
