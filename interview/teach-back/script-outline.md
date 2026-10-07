# Metal teach-back — Speaking script

Five minutes. Explain the mechanism through its effect on customer experience, growth capacity, operating cost and managed recovery. The outcome and teaching sections have short spoken paragraphs and one optional understanding question; the cover is just the introduction. Use the questions naturally; do not turn the five-minute explanation into discovery.

Canonical presenter script; [Notion TeachBack](https://app.notion.com/p/3ef1840cbb9e8105a768d99d5570e754) reconciled October 6, 2026. [Evidence](../../context/product/aurora-metal-teach-back.md) holds sources and claim scope.

## Slide 1 — Intro
You’re running Aurora and it’s working for you. I’ll show what PlanetScale Metal changes and how that can translate into business impact.

## Slide 2 — Impact of Metal
Faster queries mean customers spend less time waiting for application features. For I/O-heavy workloads, Metal’s local NVMe can help keep that experience responsive.

Higher throughput means the database can complete more work under load, giving the business more room for additional customers and more product usage.

Managed high availability uses one primary and two replicas. PlanetScale handles recovery when the primary fails. That helps restore service without waiting for an engineer to intervene, while your team focuses on the product. Brief interruptions can still occur.

**Question:** Are speed, capacity and reliability a useful way to frame the comparison?

## Slide 3 — Case Study: Intercom
Intercom shows what this can mean in practice. It’s a Vitess / MySQL customer using Metal’s local storage approach.

Peak-load I/O saturation on its PlanetScale EBS setup slowed the Inbox. Its immediate workaround was extra capacity and higher-IOPS io2 storage.

With Metal, conversation loading became faster and more consistent, even at peak load, and database cost fell by over 60% compared with that previous EBS io2 setup. That’s a better experience for customers and a lower operating bill for the business.

In its March 2025 report, Intercom also reported no availability issues caused by migrated databases and maintenance without customer downtime through Vitess failover.

**Question:** Does that connect the storage change to both customer experience and operating cost?

## Slide 4 — What is Metal? Aurora comparison
Metal puts Postgres compute and persistent local NVMe on the same machine. Here’s how that compares with your Aurora setup: the database instance has the CPU and memory, while persistent data lives in a separate, shared SSD storage volume.

When Aurora needs data that isn’t cached, it accesses that storage over the network. Under heavy I/O demand, storage waits can slow queries and limit how much work completes. Customers feel that as slower application features during busy periods.

Metal changes that persistent storage path. Fast local NVMe can reduce waiting for storage-bound queries, while higher I/O capacity gives the database room to complete more work under load. The business impact is a responsive product with more headroom for usage and customer growth.

More CPU, memory and tuning can still help on Aurora. Metal’s benefit depends on whether storage I/O is the constraint. The tradeoff is fixed drive capacity: leave headroom and plan resizing ahead of growth.

**Question:** Is it clear how local storage can improve both query speed and capacity under load?

## Slide 5 — Show Benchmarks
In this tested workload, Metal completed 16.3k queries per second versus 10.9k on Aurora, with lower p99 query latency.

That’s more work completed with faster responses for the slowest queries. The business relevance is capacity without sacrificing the customer experience. These results are specific to the benchmark workload.

**Question:** Does that clarify why we look at both throughput and query latency?

## Preparation cues — outside the speaking notes

- Timing → Intro 10s; outcomes 45s; Intercom 75s; Metal comparison 120s; benchmark 50s. Rehearse aloud; timings are targets.
- Questions → one per slide, used naturally to check understanding. Ask the Metal question if time is tight; leave deeper discussion for the Q&A block.
- Availability → HA clusters have replicas and automated failover; single-node plans do not offer the same resilience. Brief disruption and application retries remain possible. Aurora also offers HA; local NVMe alone is not HA. [Postgres operations](https://planetscale.com/docs/postgres/operations-philosophy).
- Intercom → Aurora MySQL/custom sharding → PlanetScale Vitess/EBS → Metal. Its 60%+ saving is database cost versus previous EBS io2, not its total cloud bill or a Postgres result. The 90%+ query improvement in the article involved materialized-view rewrites; do not attribute it to Metal. [Customer report](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure-lessons-and-progress/).
- Mechanism → local attachment and NVMe work together. No verified raw-drive comparison with a particular Aurora SSD. [Metal docs](https://planetscale.com/docs/metal).
- Metrics → Aurora has no universal network-hop latency in these sources. The combined comparison uses Aurora’s actual shared-storage path. Its ~1 ms network-storage workload and ~50 µs local-NVMe access examples have different evidence bases; they are not Aurora measurements or a matched benchmark. IOPS and QPS are different metrics; hardware capacity is finite.
- Tradeoffs → capacity planning stays in the Metal notes; the detailed tradeoffs slide remains hidden.
- Unknown → “I don’t know that configuration. I’d confirm it.”
- ROI → Intercom demonstrates improved service performance and lower database operating cost. Its outcome reflects the complete change from EBS io2 to Metal; the report does not isolate a dollar saving from the network hop alone. Workload growth and hardware still require planning.
