# The sales story

The interview brief is to pitch Postgres on Metal to a customer already running Postgres and preview Neki. The next step is a technical discovery session with the database owner, not a purchase decision made from a slide deck.

## Flow

| Section | Buyer question | Role in the pitch |
| --- | --- | --- |
| Opening and discovery | What is creating pressure, and why does it matter? | Establish the prospect's problem before assuming one |
| Nexus | Why might more capacity leave the problem unresolved? | Explain the common capacity model and invite discussion |
| Convex | Has this helped a production Postgres workload? | Show customer-reported latency evidence |
| Intercom | What happens when buying more headroom gets expensive? | Show a business consequence and an observed Metal outcome; identify the Vitess/MySQL workload |
| What is Metal? | What changes in the storage path? | Explain the mechanism behind the performance proposition |
| Benchmarks | What is worth testing on our workload? | Show throughput and p99 for a defined run |
| Architecture | Who handles availability and operations? | Explain the cluster and operator responsibilities |
| Neki and scale | What if one machine stops being enough? | Preview horizontal scaling and its specific benchmark |
| Cloud | Does this fit our deployment requirements? | Discuss hosted or BYOC choices |
| Migration | How do we evaluate and move? | Agree on participants, success criteria, and a next meeting |

Vitalize and Autumn are retained as optional supporting stories. Their inclusion should follow the conversation rather than extend every pitch.

## Gong influence

The supplied Gong presentation template informed the structure: a relevant insight, a recognizable problem, a customer story, a clear value proposition, and evidence that matches the buyer. This deck adapts those ideas to an infrastructure sale; it is not a prescribed Gong sequence.

The technical diagrams earn their place by explaining why a problem occurs or how the proposed operating model changes it. Customer stories establish relevance. Benchmarks support a hypothesis to test, not a guaranteed outcome.

## Delivery

Ask where Postgres creates pressure, what that costs, what the team has tried, and what deadline matters. Use the answers to decide which evidence deserves time.

Nexus establishes compute and network-attached storage, grows the resource shapes, then reveals Latency, Storage I/O, and Availability. Intercom reveals peak-load pain, the previous capacity/IOPS response, and the original cost chart. The PDF uses separate pages for meaningful states.

The vertical-scaling transition now closes the architecture notes: “Metal optimizes performance within a Postgres cluster and is our vertical scaling solution.” Neki opens the discussion of growth beyond one machine.

End by relating the evaluation to the prospect's stated problem and impact. Bring the database owner into a technical session, agree on success criteria and compatibility work, and ask who else needs to join and when.

The actual spoken script lives locally in ignored `private/speaker-outline.json`. This document explains the choices; it is not a second script.
