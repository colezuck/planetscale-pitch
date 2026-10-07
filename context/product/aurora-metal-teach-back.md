# Aurora and Metal: teach-back evidence

Reviewed October 4, 2026. The staff engineer's storage problem is a hypothesis to test. The architecture slide uses actual Aurora terminology. The comparison uses an explicitly named EBS io2 reference to provide documented storage figures; those figures are not relabeled as Aurora or measured Metal averages.

## Selected customer problem

Maintaining fast, predictable query responses as working set and concurrency grow. Physical read waiting is the mechanism to investigate; capacity growth creates pressure, while throughput and cost are consequences to measure. A cache-resident or CPU-bound workload may benefit less. Low CPU alone does not establish an I/O bottleneck. [AWS read-wait guidance](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/apg-waits.iodatafileread.html).

## Aurora architecture and scaling

Aurora persistent data lives in a shared distributed SSD-backed cluster volume, separate from compute. It is not an ordinary EBS database volume attached to EC2. Storage grows automatically as data grows, independently of compute. Scale-up can add memory, compute and network capacity and reduce cache misses; it does not move the persistent volume onto the host. A remaining physical read uses the remote storage path. The diagram's growth sizes are schematic. [AWS storage and reliability](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html).

Memory/cache hits avoid persistent reads. Eligible Aurora Optimized Reads instances use local NVMe for temporary data and, with I/O-Optimized, tiered caching. Do not imply every Aurora I/O crosses the network or that Aurora has no local disk. [AWS Optimized Reads](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.optimized.reads.html).

Aurora does not sell the conventional EBS provisioned-IOPS setting. Aurora Standard charges for consumed read/write I/O; I/O-Optimized changes that billing and the other prices. Evaluate full configuration cost, not an EBS IOPS-tier narrative. [AWS CreateDBInstance API](https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_CreateDBInstance.html), [Aurora pricing](https://aws.amazon.com/rds/aurora/pricing/).

## Latency and throughput claims

No verified universal average Aurora storage-hop latency is available in these sources. The comparison pairs AWS’s documented io2 Block Express average of **under 500 µs for 16 KiB I/O on Nitro instances** with PlanetScale’s **~50 µs illustrative local-NVMe round trip**. Different evidence bases are labeled on the graphic (AWS average versus illustrative access); do not calculate a measured speedup ratio or call ~50 µs a Metal service average. [AWS EBS FAQ](https://aws.amazon.com/ebs/faqs/), [PlanetScale IO devices and latency](https://planetscale.com/blog/io-devices-and-latency). AWS `os.diskIO.auroraStorage.readLatency` measures average read I/O request latency to Aurora storage in milliseconds. It is not an isolated wire-hop measure and not whole-query p99. PostgreSQL counters such as storage blocks read and read time help assess physical reads; timing requires the applicable tracking configuration. Compare matched workloads and warm/cold cache behavior. [AWS Performance Insights counters](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_PerfInsights_Counters.html).

Metal local persistent NVMe removes the separate storage-network round trip for local page access. Client communication and replication still use networking. Hardware IOPS are finite. Local access latency does not translate proportionally into query latency or QPS. [PlanetScale Postgres architecture](https://planetscale.com/docs/postgres/postgres-architecture), [Metal](https://planetscale.com/docs/metal).

The vendor Aurora benchmark reports roughly 18k versus 12k QPS for its 500 GB TPCC-style test, but roughly equal 35k QPS for its 300 GB read-only test. These vendor tests illustrate workload dependence, not a universal multiplier. [Benchmark and methodology](https://planetscale.com/benchmarks/aurora).

## Depot proof and its limits

Depot's CTO reported March 11, 2025:

| Metric | Before | Metal | Ratio |
| --- | --- | --- | --- |
| Query p95 | 40 ms | 5 ms | 8× faster |
| Query p99 | 50 ms | 30 ms | About 1.7× faster |
| Build analytics metadata retention | 7/30/90 days by plan | Limits removed | Product outcome, not disk capacity |

This is **Vitess/MySQL**, moving from PlanetScale EBS-backed PS-400 (8 CPUs) to Metal M-320 (4 CPUs), not Aurora PostgreSQL and not a controlled disk-only experiment. Depot reported steadier performance at peak hours and disappearing iowait. Removal of retention limits enables more complete historical analytics; the article does not quantify a maximum queryable dataset size or establish infinite retention capacity. [Depot's original report](https://depot.dev/blog/faster-database-with-planetscale-metal).

The current slide uses **Depot’s original stacked CPU chart**, with its axes and legend preserved. CSS inversion/hue rotation adapts its presentation to the dark slide; the stored image is unchanged. Large typography presents the exact reported query measurements separately. The graphic is CPU usage, not a query-latency trace. There is no inferred cutover timestamp. The history timeline is a schematic of a removed product restriction, not measured days or infinite physical capacity. [Asset provenance](../evidence/depot-metal-art.md). The older proportional bars are retained as an unused asset, not current slide evidence.


## Capacity tradeoff

Metal requires selecting a drive size upfront, monitoring usage, leaving headroom and planning a resize. It does not autoscale the disk. Resizing copies data between drives and generally takes longer than network-storage resizing. [Metal documentation](https://planetscale.com/docs/metal).

Newer eligible compute sizes offer several disk capacities, so storage growth does not necessarily require more CPU/RAM. Confirm offered capacities for the chosen configuration. [December 15, 2025 Metal GA announcement](https://planetscale.com/blog/50-dollar-planetscale-metal-is-ga-for-postgres).

The slide compares these tradeoffs to Aurora's automatic volume growth, not PlanetScale's separate EBS product. HA, recovery, extensions, migration and cutover remain evaluation/Q&A topics. No zero-downtime promise, universal savings or guaranteed p99 improvement is made.

## Aurora attention-slide messaging


The Aurora slide and EBS/Metal comparison show the same EBS storage I/O reference: io2 Block Express <500 µs average for 16 KiB I/O on Nitro, and gp3 single-digit millisecond latency. These are not Aurora latency or isolated network-hop measurements. Fixed 400 µs and 1 ms figures are not supported as universal averages by current AWS specifications. [AWS io2](https://docs.aws.amazon.com/ebs/latest/userguide/provisioned-iops.html), [AWS gp3](https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html).

## Tradeoffs slide revision

The current art-free table compares **PlanetScale Metal** with **Aurora**, using local/network storage subtitles rather than the inaccurate “Aurora EBS” name. Aurora persistent data is in its shared distributed cluster volume. EBS references elsewhere remain illustrative, not Aurora measurements.

- Metal: persistent local NVMe, no separate storage-network hop for local page access; finite hardware performance. Aurora: persistent shared volume accessed over the storage network. Cache hits and eligible Optimized Reads tiered caching avoid some remote reads.
- Metal: selected drive capacity, reserved headroom and proactive resize; no disk autoscaling. Aurora: automatic persistent-volume growth, independent of compute, within engine/version limits.
- Metal resizing copies data between drives; allow transfer time, especially for larger datasets. Aurora can change compute separately while persistent data remains in the shared volume. Do not promise a downtime duration for either service.
- Metal has no separately purchased IOPS tier; capacity and configuration still cost money. Aurora Standard bills read/write I/O; I/O-Optimized removes those charges with different instance/storage prices. Compare total cost and unused headroom; do not describe Aurora as an EBS provisioned-IOPS bill.
- Evaluate physical storage waits, cache behavior, realistic concurrency, p95/p99, sustained throughput, and storage-growth forecasts. No blanket performance or savings promise.

Sources: [PlanetScale Metal capacity, resizing and workload fit](https://planetscale.com/docs/metal), [AWS Aurora shared storage, growth and I/O billing](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html), [Aurora pricing](https://aws.amazon.com/rds/aurora/pricing/), [Aurora Optimized Reads](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.optimized.reads.html). Rechecked October 4, 2026.

## Retained customer proof: Convex (hidden)

The retained hidden Convex source uses the exact Convex slide from the Postgres pitch, including its original charts, logo, text, quote and CSS. Query p99: 10–15 ms to 5–7 ms; batch-commit p99: 75–200 ms to ~20 ms. Customer-reported Chef workload results, not a controlled storage-only comparison or a performance forecast. [Original Convex report](https://news.convex.dev/powered-by-planetscale-for-postgres/). Depot is temporarily hidden from audience and presenter builds; its retained section above is evidence for later use, not the current slide narrative.


## Business framing and active proof — October 6, 2026

One problem: growing I/O demand can create storage waits that slow user-facing features and limit how much work completes at peak load. Metal changes the persistent storage path to local NVMe; faster access and higher I/O capacity can improve storage-bound workloads. Business relevance is responsiveness and growth headroom, not guaranteed user counts. The Aurora diagram is now static and has no latency estimate. [Metal documentation](https://planetscale.com/docs/metal).

HA is a managed cluster capability. PlanetScale’s operator detects primary failure and promotes a healthy replica; single-node configurations do not provide that redundancy. Failover can briefly disrupt service and applications need suitable reconnection/retry behavior. Aurora also supports HA; this is not an Aurora availability comparison or an always-up promise. [Operations philosophy](https://planetscale.com/docs/postgres/operations-philosophy).

Intercom replaces Convex as visible customer proof. Its path was Aurora MySQL/custom sharding → PlanetScale Vitess on EBS → Metal. Peak-load IOPS saturation affected Inbox responsiveness, prompting extra capacity/io2 as a workaround. Intercom reports more consistent Inbox loading, 60%+ lower database cost versus its prior EBS io2 setup, and no availability issues caused by migrated databases at the time of its March 2025 report. Maintenance without customer downtime was attributed to Vitess failover. The separate 90%+ query improvement involved materialized-view rewrites and is not a Metal-only result. [Intercom report](https://www.intercom.com/blog/evolving-intercoms-database-infrastructure-lessons-and-progress/); [original art and scope](../evidence/intercom-teach-back.md).


## Centralized comparison — October 6, 2026

The visible flow is now Intro → Impact → Intercom → What is Metal / Aurora comparison → benchmark. The separate Aurora slide is retained but hidden. The combined diagram uses Aurora’s actual DB instance and shared distributed SSD-backed cluster volume, not a conventional EC2/EBS attachment. The earlier io2/gp3 and illustrative local-NVMe latency figures are removed from this direct Aurora comparison; benchmark evidence remains workload-specific. Notes explain Metal first, compare the remote Aurora path, connect storage waits to customer experience and growth headroom, then volunteer capacity planning.


## Storage-access references restored — October 6, 2026

At Cole’s request, the combined diagram again shows ~1 ms beside Network I/O and ~50 µs beside Local I/O. Both are visibly labeled as examples. The ~1 ms comes from a [PlanetScale production workload on network-attached storage](https://planetscale.com/blog/planetscale-metal-theres-no-replacement-for-displacement); the ~50 µs is a [local-NVMe access round-trip example](https://planetscale.com/blog/io-devices-and-latency). They come from different evidence bases. Neither establishes Aurora storage latency, isolated network-hop timing, a measured Metal mean or a controlled speedup ratio. The left diagram still depicts actual Aurora shared storage; its network-storage workload reference is explicitly an example.
