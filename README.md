# Schema Coding

Schema Coding treats an LLM as a language runtime and keeps judgment in a persistent, editable backend. This demo runs one incident through Markdown nodes, follows explicit rejection routes, and saves the full trail instead of hiding it in a chat. It accompanies [the Schema Coding essay](essay.md).

## Quickstart

Python 3.10+ is enough. There are no packages to install.

```sh
export ANTHROPIC_API_KEY="your-key"
python runner.py cases/sample-incident.md
```

Override the default model if needed:

```sh
export SCHEMA_MODEL="another-anthropic-model"
```


## Try it without an API key

```sh
python runner.py --mock cases/sample-incident.md
```

Mock mode replays scripted verdicts so you can watch the routing itself: `data-integrity` rejects and sends execution back to `blast-radius`; later `rollback-safety` rejects and reopens `change-correlation`. No network, no key.

## The comparison that matters

Run the same incident twice with a real key:

```sh
python runner.py --baseline cases/sample-incident.md   # same criteria, one shot, no wiring
python runner.py cases/sample-incident.md              # schema run with rejection routes
```

The baseline gets every criterion in a single prompt and is free to notice that the rollback is unsafe — and recommend it anyway. The schema run cannot: a rejected node loses the right to continue. Both runs land in `runs/` so you can diff the behavior, not the vibes.

## Example trace

```text
[01] blast-radius: PASS
[02] data-integrity: REJECT
     rejected -> routed back to 'blast-radius'
[03] blast-radius: REJECT
     rejected -> no route; HALT - escalate to human
log -> runs/20260724T091500123456Z.json
```

The JSON log records the model and every node's verdict and full reply.

## How to write your own schema

- Put one local judgment contract in each `schema/nodes/*.md` file.
- Give every node Trigger, Inspect, Pass, Reject, and On rejection sections.
- List the normal traversal order in `schema/wiring/call-order.md`.
- Put cross-node priorities in `conflict-priority.md`.
- Add only deliberate failure routes to `rejection-routes.md`.

This is a demo of the concept, not a framework.
