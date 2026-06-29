# Use AG-UI protocol for agent↔UI transport

The War Room backend emits AG-UI events (RUN_STARTED, TEXT_MESSAGE_*, TOOL_CALL_*, STATE_DELTA, RUN_FINISHED) consumed by a single-file vanilla JS frontend over SSE. This standard protocol drives both the conventional timeline UI (via STATE_DELTA) and the chat sidebar from one stream, avoiding a Node build. CopilotKit/React is a documented stretch.
