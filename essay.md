# Stop Making the Model Smarter. Build the Roads.

Here's a thing I've watched an LLM do more times than I want to admit: correctly observe that a rollback is unsafe, and then — three paragraphs later, in the same response — recommend the rollback. It knew. The knowledge was right there in its own output. It just didn't have anywhere to *put* that knowledge where the rest of the reasoning would be forced to respect it.

When we hit failures like this, our instinct is always the same. Reach deeper into the box. More parameters, more context, a cleverer prompt, next quarter's model. The assumption underneath is that the model *is* the whole program, so any failure must be a model failure.

But plenty of these failures aren't about knowledge at all. The model noticed the wrong thing first. It let a weak consideration outvote a critical one. It flagged a problem and then breezed past its own flag. Those are path failures — and you don't fix a path failure by making the traveler smarter. You fix it by building roads.

So that's the proposal, and I'll give it a name up front: **Schema Coding**. Leave the LLM alone. It stays a general-purpose language runtime. Outside it, build a persistent, human-readable judgment backend — folders, Markdown files, links, state, versions, and rejection routes. The model handles local language operations. The schema decides which judgments must happen, in what order, on what evidence, and — the part everything else hinges on — where execution goes when a judgment *fails*.

The model supplies linguistic computation. The schema supplies judgment topology.

## A backend made of language

The most interesting AI program you build this year might look like a directory:

```
incident-schema/
├── contract.md
├── nodes/
│   ├── blast-radius.md
│   ├── data-integrity.md
│   ├── change-correlation.md
│   └── rollback-safety.md
├── wiring/
│   ├── call-order.md
│   ├── conflict-priority.md
│   └── rejection-routes.md
├── references/
└── revisions/
```

Each node is a judgment operation written in plain language. The wiring files describe how those operations constrain each other. A small, deliberately boring runner does the deterministic parts:

```
node   = schema.load(current_path)
result = model.run(node.contract, state)
current_path = wiring.route(node.id, result.status)
```

The Markdown isn't documentation *about* the program. The Markdown *is* the program — the judgment contracts the runtime executes.

If you're thinking "isn't this just a prompt with extra steps," fair, let me draw the lines. A prompt is a request; it flows through once and evaporates. A skill packages one thing a model can do. A schema is different in kind: it's a persistent address space where multiple judgments can block, override, revisit, and repair one another. The difference isn't instruction length. It's architecture.

Andrej Karpathy's [Software 3.0](https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again) is the right umbrella here — natural language has become a programming layer, and LLMs execute programs written in it. Schema Coding is what happens when you take that seriously as an *engineering* claim and ask the unglamorous follow-ups: fine, language is a programming layer. So what are its modules? Its control flow? Its rejection semantics, persistent state, and version history — when the thing being programmed is judgment?

## Grinding versus casting

Pretraining grinds the library.

Millions of books, arguments, corrections, and worked examples go into one giant optimization process, and what comes out is genuinely astonishing. But the ingredients lose their addresses on the way in. Some expert's hard-won distinction may well be shaping the weights right now — you just can't open it, list its callers, bump its priority, or diff revision 12 against revision 13. The model may contain the pattern. It never gives the pattern an address.

Schema Coding tries the opposite move: *cast* one judgment procedure as a separate object, seams intact. This criterion lives in this file. This exception traces to this source. This rule outranks that one. This rejection returns to that earlier node. This edge changed on March 12th, after a specific failure, and the diff says why.

Grinding buys you capability. Casting buys you something you can inspect, fork, and repair.

There's a second reversal hiding in here, and it's my favorite part. Software engineering has always translated in one direction: take rich human judgment and compress it *down* until it fits the machine. The expert speaks in context, exceptions, analogies, uneasy distinctions — and the implementation flattens all of it into enums, branches, and thresholds. The machine's vocabulary wins. It has always won, because it was the only vocabulary that could execute.

That constraint just expired. LLMs can execute the human's vocabulary now. So keep the judgment close to the language the expert actually left it in. Give that language addresses and topology. Let deterministic code do what it's good at — storage, permissions, traversal, logs — and make the machine climb *up* to the expert's structure instead of dragging the expert down into the machine's ontology.

Software used to make judgment speak machine. Now the machine can travel through judgment spoken human.

## Three primitives

You need three: nodes, wiring, and reverse-engineering.

### 1. Nodes — give a judgment an address

A node is a local judgment unit: when to look, at what evidence, what passes, what fails, what repair is owed, and where execution goes after a rejection. Here's `data-integrity.md` from the incident schema:

```
NODE: data-integrity

Trigger:
  The incident may involve a stateful write path.

Inspect:
  Write failures, invariant violations, replication lag,
  irreversible mutations, and missing evidence.

Pass:
  Corruption risk is excluded by relevant evidence.

Reject:
  Integrity remains uncertain or an invariant is broken.

On rejection:
  Block remediation. Route to evidence collection or
  containment before availability recovery.
```

"Check data integrity" is advice. This is a contract — and the difference is what happens when things go wrong. If your system keeps missing silent corruption, you now know *which object* to open. Tighten its trigger. Strengthen its evidence bar. Split it in two. Reroute its exit. What you don't have to do is rewrite a two-thousand-word mega-prompt and pray the side effects are friendly.

A principle earns its place in a schema the moment it can cause a decision. Until then it's a poster on the wall.

### 2. Wiring — turn criteria into a system

A folder of excellent criteria still isn't a judgment system. The system shows up when the criteria can call, block, override, and send each other back. In the incident schema, the wiring says things like: establish blast radius before anyone proposes remediation. If availability and possible corruption collide, integrity wins — every time, no vibes. If rollback safety fails, go back to change analysis; do not improvise a rollback. If evidence is thin, reject the transition instead of writing a confident summary over the gap.

Notice that no single node contains any of that. It lives in the topology.

And this is the real dividing line between a rule list and a schema — not how many rules you have, but whether a failure can be *routed back to its cause*. That route is exactly what one-shot LLM workflows lack, which is how you get my rollback story from the opening: the model can name the danger and still walk into it, because naming carried no consequences. A rejection route changes the physics. The failed candidate doesn't get a warning label. It loses the right to continue.

### 3. Reverse-engineering — recover the edges nobody wrote down

Experts almost never describe their full wiring, and the fun part is they don't know they're not describing it.

An incident commander tells you, "collect evidence before acting." Sensible. But the incident record shows that whenever a fresh deploy touched a stateful write path, she rolled back *immediately* — same incomplete observability, opposite action. That repeated trigger is the tell: in her actual hierarchy, possible irreversible writes outrank the usual appetite for more evidence. That edge appears in no handbook. It has to be inferred from behavior.

There's real prior art for the extraction itself. Militello and Hutton's [Applied Cognitive Task Analysis](https://www.tandfonline.com/doi/abs/10.1080/001401398186108) laid out practical methods for pulling cues, strategies, and exceptions out of experts back in 1998. And there's a standing warning against trusting introspection alone: Nisbett and Wilson's ["Telling More Than We Can Know"](https://doi.org/10.1037/0033-295X.84.3.231) made the case that people's verbal reports on their own high-level cognition are unreliable readouts — experts give useful explanations, not complete ones.

So: interview the expert for vocabulary. Mine the record for wiring. When the written theory and the behavioral record disagree, that disagreement isn't noise. It's where the hidden structure surfaces.

The handbook gives you the first graph. The corrections tell you where the real edges are.

## A codebase for judgment

Chain-of-thought showed that intermediate reasoning improves what a model does within a query — [Wei et al., 2022](https://proceedings.neurips.cc/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html) made reasoning steps a first-class citizen of LLM interaction. But a chain generated for one query is gone by the next. Its steps have no durable identity, its priorities no stable address, its corrections no lineage.

Chain-of-thought is a stack frame. A schema is a codebase.

The same named node runs across a thousand cases. The same priority edge governs every conflict. A change reviews as a diff, a behavior traces to a version, and a model upgrade swaps the runtime while the judgment structure stays put. Which quietly changes the unit of improvement — from "how do I get a better answer?" to "which judgment object took the wrong turn, and how should *that object* change?"

Which brings us to the loop.

## Don't patch the answer

A serious student doesn't study past exams by memorizing the answer key. They solve the problem, compare against the reference, and hunt for the exact point where the two reasoning paths *split*. Ignored a condition? Right concepts, wrong order? A pet heuristic outvoting a stronger rule? Then they repair the method — not the answer — and solve again. The mistake log they keep isn't a list of wrong answers; it's a record of how their method failed and how it changed.

Schema Coding runs the same loop. Build an initial schema from manuals and prior decisions. Run a new case. Compare the output against a reference response. Find where the judgments diverged. Revise the responsible node or wire — then re-run, and record the structural delta.

Don't patch the output. Patch the path that produced it.

The feedback machinery for this already exists. [Self-Refine](https://papers.nips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html) showed iterative natural-language feedback improving outputs with no extra training; [TextGrad](https://www.nature.com/articles/s41586-025-08661-4) treats language feedback as an optimization signal that updates text-defined components across a whole system. Schema Coding changes the *target* of that signal. The correction doesn't dissolve into a slightly better answer or silt up an ever-growing prompt. It lands on a named object — a node, an edge, a trigger, a route — and stays there after the chat ends.

Which is why the error log outranks the polished snapshot. A good revision record holds the triggering case, the observed divergence, the responsible object, the before, the after, and the reason. Over time, the log develops a plot: repeated divergences expose missing concepts, repeated rewiring exposes hidden priorities, and repeated rejection failures expose criteria that exist as prose but carry no force. The error log isn't development debris. It's the artifact.

One rule keeps that history legible: **design-time mutability, run-time immutability**. Between runs, the schema is clay. During a run, it's law — every execution pins a version, and the system doesn't rewrite its own constitution mid-case. Otherwise the route, the explanation, and the outcome all point at a moving target.

## "Isn't this just LangGraph with extra Markdown?"

Someone's typing this comment already, so let's do it here. Orchestration frameworks — LangGraph, state machines, workflow DAGs — absolutely give you graphs, routing, and retries. Two things are different.

First, *where the judgment lives*. In an orchestration framework, a developer encodes the graph in code; the conditions are predicates someone translated. In a schema, the judgment conditions stay in the expert's own language, in files the expert can read and edit directly. A domain expert amends a distinction in Markdown instead of filing a ticket and watching it come back as a Boolean.

Second, *where the graph comes from*. Workflow graphs are designed. Schema wiring is partly *recovered* — reverse-engineered from behavioral records, then revised through observed divergence between the schema's output and a reference response. The graph isn't a spec you wrote once. It's a hypothesis you keep correcting against how the expert actually behaved.

Could you build Schema Coding *on top of* LangGraph? Sure. The framework is the chassis. The claim is about what you load into it.

## The assembly is the claim

Every part of this has precedent, and I mean that as a feature. Software 3.0 supplies the umbrella. ACTA supplies extraction methods. Nisbett and Wilson explain why behavior must check self-report. Chain-of-thought made intermediate reasoning operational. Self-Refine and TextGrad turned language feedback into an optimization signal. [ADAS](https://arxiv.org/abs/2408.08435) even made agent architectures themselves searchable objects.

What doesn't exist yet is the assembly, and a vocabulary for it: a persistent, human-readable judgment graph — nodes and wiring — reverse-engineered from behavioral records, revised through observed divergence, executed by an unchanged language model. That's the proposal. Not a new foundation model; an engineering object that foundation models just made possible.

And once judgment has addresses, it starts behaving like software. Reviewed, diffed, forked, composed, rolled back. Teams argue about an explicit priority edge instead of trading prompt incantations. Models get replaced under an architecture that survives them.

The model becomes a runtime. The schema becomes the judgment backend. And the most valuable output might not be the schema at all — it might be the record of how the schema learned to exist.

## Speculation: from language to judgment

Everything past this line is speculation. Marked as such. Proceeding anyway.

A schema encodes one persistent judgment structure. A **meta-schema** would learn from the revision logs of *many* schemas — not picking from existing workflows, but learning how judgment structures get built: when a concept deserves a node, when a node should split, when an implicit priority needs an explicit edge, how a behavioral divergence should reshape a topology. Hand it a new body of source material and a set of reference decisions, and it proposes the first architecture, then improves it from its own error trail.

And above that, a **meta-meta layer**: a system that generates the method of building itself. Not a better map — a better cartography. It picks the primitives, the decomposition strategy, the evidence model, the revision logic, fitted to a class of judgment nobody has structured before.

The long arc reads: NUMBERS → LANGUAGE → JUDGMENT. Numerical computation became the substrate for statistical language patterns. LLMs made fuzzy distinctions executable at machine speed. The open question is whether language computation, plus durable external structure, becomes the substrate for observable judgment patterns — not judgment as a magic substance sealed in a model, but judgment as a stable, *editable* pattern of noticing, selecting, rejecting, returning, and revising.

You don't need to wait for the black box to turn transparent. Name one judgment. Give it a file. Draw the route it can reject. Run a real case. Save the first wrong turn.

We spent a decade teaching numbers to produce language. The next systems might teach language to accumulate judgment.

Don't open the box. Build the roads — and keep every map of where they failed.
