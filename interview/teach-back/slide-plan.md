# Metal teach-back slide plan

Audience: Aurora PostgreSQL staff engineer. Five minutes plus questions. Start with business outcomes, compare Metal’s local NVMe with Aurora’s shared storage on one static slide, then show benchmark evidence. [Assignment](../brief/README.md), [evidence](../../context/product/aurora-metal-teach-back.md), [notes](script-outline.md).

| ID / target time | Purpose | Visual / spoken point |
| --- | --- | --- |
| `problem` / 10s | Establish why Metal matters | Same-line PlanetScale Metal lockup; brief introduction. |
| `outcomes` / 45s | Explain the three business outcomes | Title: Impact of Metal. Three aligned benefit columns with consistent two-line headings and static art: lightning bolt, parallel arrows, and an HA cluster with one primary and two replicas. Thin square frames and replication connectors match the hardware diagrams. Speak to customer waiting, growth capacity and managed recovery. |
| `intercom` / 75s | Show a business outcome | Original hourly database cost chart, 60%+ lower database cost versus previous EBS io2. Faster Inbox loading, reported operational stability and maintenance without customer downtime. Clearly labeled Vitess/MySQL; March 2025 customer report. No animated reveals. |
| `metal` / 120s | Explain the change and operating model | Combined static Aurora/local-NVMe comparison. Faster storage access helps storage-bound queries; higher I/O capacity supports more work. Notes explain HA operator failover and volunteer fixed-drive capacity planning. Aurora DB instance → shared distributed SSD volume versus compute + persistent NVMe on one host. Static ~1 ms network-storage workload and ~50 µs NVMe-access examples are labeled at the values; they are not measured Aurora or matched test results. |
| `benchmark` / 50s | Connect mechanism to measured performance | Original Postgres pitch QPS/p99 slide. 16.3k versus 10.9k QPS in this workload; complete-platform benchmark. No universal speedup. |

The standalone Aurora slide, Convex, Depot and the detailed tradeoffs comparison are hidden and retained. Tradeoffs are spoken during Metal. Aurora also has HA; do not imply it lacks resilience. PlanetScale HA is a managed cluster capability, not a property of a single local disk. No universal availability, savings or query-speed guarantee.

Each section of the speaking script has one optional understanding question. Prioritize the Metal question: “Is the distinction clear between making queries faster and completing more work under load?” Keep it a TeachBack, not discovery or an evaluation close. Timings need aloud rehearsal.

[Notion notes](https://app.notion.com/p/3ef1840cbb9e8105a768d99d5570e754) reconciled October 6, 2026. Sales-manager feedback remains at the bottom of that page. The uncertain downtime-cost anecdote is not reused as evidence.
