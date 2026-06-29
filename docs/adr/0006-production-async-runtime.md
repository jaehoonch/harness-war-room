# Production-scale async runtime: live buggy app + Durable Functions

The demo replays canned transcripts. Production scale means the agents act on a
real system. We deploy the buggy services as a **live Container App (`shop-api`)**:
`/price`, `/tax`, `/loyalty` import the same `demo_repo` source, so a defect on
disk is observable over HTTP. Repro is a real call that overcharges.

The pipeline runs **asynchronously in Azure Durable Functions (Python v2)**. An
HTTP starter kicks an orchestrator that fans through activities
triage -> repro -> fix -> review (loop) -> redeploy, persisting state so the UI
polls a durable status endpoint instead of holding an SSE connection. Fix opens a
real ADO branch/PR; redeploy triggers the ADO pipeline that ships `shop-api`.
The `warroom` Container App stays the control plane/UI; `DEMO_MODE` replay remains
for offline demos. All adapters (Azure OpenAI, ADO, shop-api) are seam-injected so
tests run with no network.
