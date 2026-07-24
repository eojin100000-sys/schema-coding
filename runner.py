#!/usr/bin/env python3
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
API_URL = "https://api.anthropic.com/v1/messages"
def read(path):
    return path.read_text(encoding="utf-8").strip()

def load_order():
    text = read(ROOT / "schema/wiring/call-order.md")
    return [line.strip() for line in text.splitlines() if line.strip()]

def load_routes():
    routes = {}
    for line in read(ROOT / "schema/wiring/rejection-routes.md").splitlines():
        if line.strip():
            source, target = line.split("->", 1)
            routes[source.strip()] = target.strip()
    return routes
def call_model(key, model, system, user):
    payload = {
        "model": model,
        "max_tokens": 1000,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    request = Request(
        API_URL, data=json.dumps(payload).encode(), method="POST",
        headers={
            "content-type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": key,
        },
    )
    try:
        with urlopen(request, timeout=90) as response:
            payload = json.load(response)
    except HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise RuntimeError(f"Anthropic API {error.code}: {detail}") from error
    text = "\n".join(
        block["text"] for block in payload.get("content", [])
        if block.get("type") == "text"
    ).strip()
    if not text:
        raise RuntimeError("Anthropic returned no text")
    return text
def parse_verdict(reply):
    pattern = r"(?:^|\n)VERDICT:[ \t]*(PASS|REJECT)[ \t]*\Z"
    match = re.search(pattern, reply, re.IGNORECASE)
    return match.group(1).upper() if match else "ERROR"
def main():
    if len(sys.argv) != 2:
        print("usage: python runner.py cases/sample-incident.md", file=sys.stderr)
        return 2
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY is not set", file=sys.stderr)
        return 2
    case = read(Path(sys.argv[1]))
    model = os.environ.get("SCHEMA_MODEL", "claude-sonnet-4-6")
    contract = read(ROOT / "schema/contract.md")
    priority = read(ROOT / "schema/wiring/conflict-priority.md")
    system = (
        f"{contract}\n\nCONFLICT PRIORITY\n{priority}\n\n"
        "End the reply with exactly VERDICT: PASS or VERDICT: REJECT."
    )
    order, routes = load_order(), load_routes()
    nodes = {node_id: read(ROOT / f"schema/nodes/{node_id}.md") for node_id in order}
    queue, findings, steps = order.copy(), [], []
    started = datetime.now(timezone.utc)
    run_path = ROOT / "runs" / started.strftime("%Y%m%dT%H%M%S%fZ.json")
    for number in range(1, 21):
        if not queue:
            break
        node_id = queue.pop(0)
        node = nodes[node_id]
        prior = "\n\n".join(findings) or "None yet."
        user = f"NODE CONTRACT\n{node}\n\nINCIDENT\n{case}\n\nFINDINGS SO FAR\n{prior}"
        try:
            reply = call_model(key, model, system, user)
            verdict = parse_verdict(reply)
        except Exception as error:
            reply, verdict = f"ERROR: {error}", "ERROR"
        steps.append({"node": node_id, "verdict": verdict, "full_reply": reply})
        print(f"[{number:02}] {node_id}: {verdict}")
        findings.append(f"{node_id} ({verdict})\n{reply}")

        if verdict == "ERROR":
            print("     HALT - escalate to human")
            break
        if verdict == "REJECT":
            target = routes.get(node_id)
            if not target:
                print("     rejected -> no route; HALT - escalate to human")
                break
            print(f"     rejected -> routed back to '{target}'")
            queue = order[order.index(target):]
        elif not queue:
            break
    else:
        print("     20-step cap reached; HALT - escalate to human")

    log = {"timestamp": started.isoformat(), "model": model, "steps": steps}
    run_path.write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"log -> {run_path.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
