# Sales framework extracted from the Metal pitch

This is the reasoning behind the current [pitch flow](../../../../decks/postgres-metal/pitch-blueprint.md), adapted for reuse. It is not a mandatory slide sequence or a rule to include every product.

## Buyer reasoning

| Buyer question | Sales job | Reference example |
| --- | --- | --- |
| Where does the current system create pressure? | Establish relevance; connect technical pain to user or team impact. | Opening questions about load, latency, incidents, time, and growth. |
| Why did the usual response leave pressure unresolved? | Explain a constraint without declaring their architecture universally wrong. | Nexus shows compute/storage, then larger resources, then unresolved questions. |
| Has a comparable workload improved? | Establish credibility with applicable evidence. | Convex's original Aurora/Postgres latency charts. |
| What does the workaround cost? | Connect engineering choices to business consequence. | Intercom's bottleneck, added capacity/io2, and reported cost change. This is Vitess/MySQL. |
| What actually changes? | Explain a mechanism in words the buyer could repeat. | Metal's network storage path versus local NVMe path. |
| What should we test ourselves? | Turn evidence into a workload-specific evaluation hypothesis. | Defined throughput and p99 benchmarks. |
| How do we operate it and fit our environment? | Address risk, responsibilities, deployment, and compatibility. | HA topology, selected connections, cloud account choices, migration. |
| What is the next useful decision? | Agree on a concrete evaluation with the right participants. | Database owner, success criteria, migration effort, timeline. |

The deck was influenced by a supplied Gong template, but this is its local adaptation. Problem → current response → outcome describes the customer story. Mechanism → evidence → evaluation describes the proposed solution. Use a buyer's stated problem when available; otherwise explicitly frame a hypothesis and ask whether it applies.

## Choose the depth

- **Sales pitch:** use applicable proof early, explain the mechanism, address adoption risk, and close on evaluation. Optional case studies serve the conversation rather than extending every pitch.
- **Five-minute teach-back:** one problem, one mechanism, one applicable proof point if useful, tradeoffs, a check-in. Do not compress the whole Metal/Neki/cloud/migration deck into five minutes. The brief does not require slides.
- **Discovery support:** prioritize prompts and evidence that help test a hypothesis. Keep question branches in the spoken outline rather than forcing a product tour.

## Slide and speaker contract

Write a compact plan using this example shape; omit fields that add no value for a small edit:

```text
ID: storage-path
Buyer question: Why could more CPU leave this workload waiting?
Purpose: Explain the storage path relevant to the suspected I/O constraint.
Visual: Side-by-side mechanism comparison; identical boundary and labels.
Evidence: Source URL, checked date, engine/workload, measured or illustrative.
States: Current path → local path → buyer-relevant implication, if staged.
Spoken point: Explain the hop and its possible effect without promising query speed.
Check-in: Is storage I/O a meaningful constraint in your current workload?
```

Slide copy names the subject or supported result. Notes hold the conversational explanation, discovery questions, and detail. Context holds source evidence and claim limits. A necessary comparison label or caveat stays visible on the slide: units, engine, percentile, workload, illustrative status, or preview status when omission would mislead.

Use a customer outcome headline only when supported. Use a subject title for a mechanism or architecture explanation. Avoid website recitation, lists of features without consequences, empty slogans, and assumptions about a prospect's pain. End with participants, evaluation success criteria, and a next decision that follows what the buyer said.

## Evidence gates

- A storage-I/O estimate is not query latency. Avoid carrying a µs estimate into a query-speed promise.
- Keep primary benchmark throughput distinct from total cluster capacity or pricing.
- Keep p95/p99, mean/maximum, milliseconds/seconds, and read/write workloads explicit.
- A vendor test, a customer story, a schematic, and an observed prospect workload establish different things.
- Intercom/Cash App Metal stories do not establish Postgres customer results.
- The eligible HA SLA is a commitment, not observed uptime or zero disruption.
- Source dates matter for pricing, preview availability, topology, and migration behavior.
- The private speaker script contains broader phrasing than the research supports in places. Preserve it during unrelated edits; do not reuse its universal speed, first/only, or no-bottleneck claims without evidence.
