# Hidden Depot case-study script

Depot remains in `decks/teach-back/content.json` with `hidden: true` and is excluded from audience and presenter builds. This is the retained rehearsal script for restoring it later.

## Slide 5 — Depot: faster queries, more history · 2:40–3:35

“Depot gives us a concrete customer outcome. This case is Vitess and MySQL, moving from PlanetScale's EBS-backed service to Metal, so it isn't an Aurora PostgreSQL benchmark.

Depot reported p95 query latency falling from 40 milliseconds to 5, and p99 from 50 to 30. It also reported more consistent performance during peak hours. This is Depot’s original CPU chart. The team reported that I/O wait disappeared after the move, even as they went from eight CPUs to four.

The product outcome matters. Depot previously retained build analytics metadata for seven, thirty or ninety days depending on the customer's plan. After the move, it removed those retention limits and could offer more complete historical analytics.

That's the opportunity: when storage performance is constraining the product, better database performance can make a richer experience practical. These are Depot's results, not a forecast for your workload.”

**Advance:** Show the original CPU chart and exact query results. Reveal the I/O-wait callout, then remove the retention boundary and extend the history schematic. More history is the business result; do not call physical storage unlimited.

