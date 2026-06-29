"""Durable Functions War Room: async orchestrator over the agent pipeline.

POST /api/start {ticket} -> returns statusQueryGetUri. The orchestrator fans
through triage -> repro -> fix/review loop -> redeploy as activities, persisting
progress to custom_status so the UI polls instead of holding a connection.
"""
import os
import sys
import tempfile
from pathlib import Path

import azure.durable_functions as df
import azure.functions as func

ROOT = Path(__file__).resolve().parent
for p in ("backend", "demo_repo"):
    sys.path.insert(0, str(ROOT / p))

app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="start")
@app.durable_client_input(client_name="client")
async def start(req: func.HttpRequest, client) -> func.HttpResponse:
    ticket = req.params.get("ticket", "INC0012345")
    iid = await client.start_new("war_room", None, ticket)
    return client.create_check_status_response(req, iid)


@app.orchestration_trigger(context_name="ctx")
def war_room(ctx: df.DurableOrchestrationContext):
    number = ctx.get_input()
    steps = []
    triage = yield ctx.call_activity("act_triage", number)
    steps.append(triage)
    ctx.set_custom_status(steps)
    repro = yield ctx.call_activity("act_repro", number)
    steps.append(repro)
    ctx.set_custom_status(steps)
    passed = False
    for loop in range(1, 4):
        rev = yield ctx.call_activity("act_fix_review", {"ticket": number, "file": triage["file"], "loop": loop})
        steps.extend(rev)
        ctx.set_custom_status(steps)
        if rev[-1].get("passed"):
            passed = True
            break
    if passed:
        steps.append((yield ctx.call_activity("act_redeploy", {"ticket": number, "file": triage["file"]})))
        ctx.set_custom_status(steps)
    return {"passed": passed, "steps": steps}


@app.activity_trigger(input_name="number")
def act_triage(number):
    from pipeline import make_default_agents, triage
    from tickets import get_ticket
    return triage(get_ticket(number), make_default_agents())


@app.activity_trigger(input_name="number")
def act_repro(number):
    from pipeline import repro
    from runtime import ShopApiProbe
    from tickets import get_ticket
    return repro(get_ticket(number), ShopApiProbe())


@app.activity_trigger(input_name="arg")
def act_fix_review(arg):
    import shutil
    from pipeline import fix, make_default_agents, review
    from runtime import RepoOps
    from sandbox import run_tests
    from tickets import get_ticket
    t = get_ticket(arg["ticket"])
    work = tempfile.mkdtemp(prefix="run-")
    repo = os.path.join(work, "repo")
    shutil.copytree(ROOT / "demo_repo", repo)
    agents = make_default_agents()
    ops = RepoOps(repo)
    f = fix(t, agents, ops, arg["file"], arg["loop"])
    result = run_tests(repo, test_path="test_" + arg["file"])
    r = review(agents, result, arg["loop"])
    return [f, r]


@app.activity_trigger(input_name="arg")
def act_redeploy(arg):
    from pipeline import redeploy
    from runtime import RepoOps, Redeployer
    return redeploy(RepoOps(str(ROOT / "demo_repo")), Redeployer(), f"Fix {arg['ticket']}")
