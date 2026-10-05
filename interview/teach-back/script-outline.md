# Metal teach-back speaking outline

Five-minute target including two brief check-ins; time aloud before the interview. Audience: an Aurora PostgreSQL staff engineer who thinks their current system is fine. One cover plus four teaching slides. The tradeoffs slide is retained but hidden; volunteer the tradeoff during Slide 3. Canonical settled script; [Notion](https://app.notion.com/p/3ef1840cbb9e8105a768d99d5570e754) holds the working story architecture. Reconciled October 4, 2026. [Evidence](../../context/product/aurora-metal-teach-back.md).

## Slide 1 — PlanetScale Metal · 0:00–0:15

“Metal puts persistent database storage on local NVMe alongside compute. Let's start with your Aurora architecture, see what changes, and discuss the tradeoff.”

**Advance:** Move directly from the clean cover to Aurora today.

## Slide 2 — Aurora today, scale-up and storage waits · 0:15–1:35

“Aurora may be working well today. The problem I would watch as your workload grows is keeping query responses fast and predictable.

Here is the relevant part of your architecture: PostgreSQL, CPU and memory in the database instance, with persistent data in a separate, shared SSD-backed storage volume. If a page is in memory, Postgres avoids the storage read. On a cache miss, it requests the page across the storage network.

Now scale up the database instance. More memory can reduce those misses, and a larger instance can provide useful compute and network capacity. Aurora's storage also grows automatically as data grows, independently of compute. But for a page that still needs persistent storage, the remote path remains.

When physical reads become a bottleneck, the query waits. That can affect your slowest responses, and limit throughput as concurrency increases. We should first check plans, indexes and waits; storage isn't the cause of every slow query.

Are physical reads a meaningful part of your slow queries, or does the working set mostly fit in memory?”

“The roughly one-millisecond figure is a published PlanetScale network-attached-storage workload example. It measures storage access, not the network hop alone, and is not a measurement of your Aurora database.”

**Advance:** AWS Aurora Storage architecture → larger compute and SSD → Bottleneck → Network Hop for Storage I/O. Pause briefly for the check-in.

## Slide 3 — What is Metal? · 1:35–2:40

“Here I’m using EBS-backed Postgres as a concrete storage reference; Aurora’s shared volume is a different implementation.

Metal changes where persistent data lives. Postgres, compute, memory and NVMe are on the same host. A local persistent page read avoids the separate storage network round trip.

That shorter path can reduce storage waiting. For an I/O-bound workload, the benefit can be faster query tails and more sustained throughput. It is not a promised multiplier: query plans, locks, CPU and caching still matter.

Aurora can already use local NVMe for temporary data and eligible tiered caching through Optimized Reads. The distinction here is persistent storage placement, not whether Aurora has any local disk.

AWS documents io2 Block Express averaging under 500 microseconds for sixteen-kibibyte I/O. AWS describes gp3 latency as single-digit milliseconds. PlanetScale’s illustrative local-NVMe access example is about 50 microseconds. These aren't matched Aurora-versus-Metal measurements, and we can't turn them into a promised query multiplier. We'd measure your actual storage reads and query tails separately. Metal's drives also have finite capacity; ‘no separately purchased IOPS tier’ doesn't mean unlimited hardware performance.”

“The tradeoff is capacity planning. Metal uses fixed local drive capacity, so you reserve headroom and plan resizing, which copies data to new drives. Aurora’s storage grows automatically. If your queries mostly hit memory or aren’t storage-bound, Metal may offer less benefit.”

**Delivery:** Say this unprompted before advancing to the benchmark. The detailed tradeoffs table remains hidden as a backup.

**Advance:** Both paths and all latency metrics are visible immediately. No metric reveal or animation on What is Metal. Keep the architecture stable. Average storage-read measurement: AWS `os.diskIO.auroraStorage.readLatency` in milliseconds; keep the metric name in Q&A.

## Slide 4 — More QPS & Lower p99 on PlanetScale Metal

“Here is the benchmark from our Postgres pitch: the same published test shows higher throughput and lower p99 on PlanetScale Metal. These are workload-specific benchmark results, not a universal improvement promise.”

## Slide 5 — Convex reduced p99 query latency by over 50% · target 45–55 seconds

“Convex's Chef workload moved from Aurora to PlanetScale Postgres. These are its original charts, with all percentile curves preserved. Query p99 changed from ten to fifteen milliseconds to five to seven milliseconds; batch-commit p99 changed from seventy-five to two hundred milliseconds to about twenty.

This is a customer-reported result, not a controlled disk-only experiment or a forecast for your workload. We would benchmark your queries, cache behavior and concurrency separately.”

**Advance:** Exact original Postgres-pitch slide, with its original charts, logo, quote, wording and styling. Depot is hidden from the current presentation; its source and script are retained.

## Rehearsal checks

- One problem: fast, predictable query responses as working set and concurrency grow.
- Explain Aurora's actual storage architecture; no provisioned-EBS-IOPS story.
- Keep the cache-miss condition and Optimized Reads nuance.
- Quote Convex's query and batch-commit p99 separately; retain customer-workload qualifications.
- Preserve the capacity tradeoff and two check-ins if shortening for time.
- If uncertain: “I don't know the exact behavior for that configuration. I'd confirm it with our solutions engineer and the current docs.”

Visible storage references use io2 ~400 µs and gp3 ~1 ms at Cole’s request. Treat these as illustrative values, not universal AWS averages or Aurora/network-only measurements. AWS publishes io2 <500 µs average for 16 KiB I/O on Nitro and gp3 single-digit milliseconds. Local NVMe ~50 µs remains an illustrative example.

## Hidden backup — Metal tradeoffs · target 45–60 seconds

“The tradeoff is less storage waiting versus more capacity planning. Metal puts persistent data on local NVMe. A local page read avoids the separate storage network hop, but hardware capacity is still finite.

Choose a drive size upfront, reserve headroom and monitor growth. Drives don't autoscale. Resizing copies data to new drives and generally takes longer than a network-storage resize. Several drive sizes can be available at the same CPU and RAM size.

Aurora's shared persistent volume grows automatically, independently of compute. Its compute instances can resize separately without moving persistent data to a new local drive.

For cost, Metal doesn't require a separate IOPS tier. Aurora Standard charges for read/write I/O; I/O-Optimized doesn't. Compare the complete configuration, including selected capacity and unused headroom, rather than promising savings.

If your working set is cached, storage waiting may be small; eligible Aurora Optimized Reads tiered caches can already reduce remote reads. I would benchmark an I/O-bound workload at realistic concurrency, then weigh query tails and throughput against growth and resizing effort.

Which matters more for this workload: reducing storage waiting or keeping capacity growth automatic?”

**Advance:** All five comparison rows are visible together. No capacity diagrams or fragment sequence. Use “Aurora” in the column header; its shared distributed storage is not an ordinary EBS volume. Confirm version-specific volume limits and resize duration in Q&A.
