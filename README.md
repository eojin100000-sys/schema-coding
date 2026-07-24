# Schema Coding

Schema Coding treats an LLM as a language runtime and keeps judgment in a persistent, editable backend. This demo runs one incident through Markdown nodes, follows explicit rejection routes, and saves the full trail instead of hiding it in a chat. It accompanies [the Schema Coding essay](ESSAY_URL_HERE).

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
