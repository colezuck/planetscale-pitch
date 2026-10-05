# Teach-back Q&A preparation

Grounded in the [evidence review](../../context/product/aurora-metal-teach-back.md), checked October 4, 2026.

| Question | Starting answer |
| --- | --- |
| We are fine today. Why change? | You may not need to. Check whether storage waiting is material to the workloads and product experiences you want to grow. |
| Doesn't Aurora already use SSDs? | Yes. Persistent data is in a shared distributed SSD-backed volume. Metal changes its placement to local persistent NVMe. |
| Doesn't Aurora have local NVMe? | Eligible Optimized Reads classes do for temporary data and, with I/O-Optimized, tiered caching. Ask about configuration and cache-hit rates. |
| What is Aurora's average storage latency? | Workload-specific. Measure `os.diskIO.auroraStorage.readLatency` in milliseconds. It is average read-request latency to storage, not an isolated network hop or query p99. The slide’s <500 µs is an AWS io2 EBS reference, and ~50 µs is an illustrative local-NVMe example. Neither is an Aurora measurement or a measured Metal mean. |
| Does scale-up help? | More memory, compute and network capacity can help. Cache misses may decline, but persistent storage remains remote. Diagnose query plans and waits first. |
| Is every I/O a network round trip? | No. Memory/cache hits avoid persistent reads; temporary NVMe and tiered caching also matter. |
| Is IOPS unlimited? | No. The drive and host have finite hardware capacity. No separately purchased IOPS allowance is a different claim. |
| Do writes avoid networking? | No. Local WAL/data access is only part of the write path; HA replication and commit confirmation matter. |
| What if a drive fails? | Managed HA uses separate replicas and failover; local disks alone do not supply service resilience. Confirm recovery objectives, backups and retry behavior. |
| Will p99 fall 70% or QPS rise proportionally? | No promise. Storage placement is one factor among plans, locks, CPU and caching. Benchmark actual workload/concurrency. Vendor throughput tests show different outcomes across workloads. |
| Is Depot’s chart query latency? | No. It is the original stacked CPU usage chart, including I/O wait. The p95/p99 figures are separately reported in its article. CPU configuration also changed; this is not a controlled disk-only experiment. |
| Does Depot prove Aurora improves 8×? | No. Depot used Vitess/MySQL, from PlanetScale EBS to Metal, with a compute configuration change. Its p95 improved 8×; p99 improved about 1.7×. |
| Does removal of Depot retention limits mean unlimited disk? | No. It removed plan-based build analytics metadata limits. Physical capacity still must be planned; no maximum dataset improvement is quantified. |
| Does Aurora charge provisioned IOPS? | Not the conventional EBS provisioned-IOPS setting. Standard charges for consumed I/O; I/O-Optimized changes that model. Compare total configurations. |
| How does Metal storage grow? | Pick a drive size, reserve headroom and monitor it. Resizing copies data and generally takes longer than network storage resizing. Several storage sizes can exist for the same CPU/RAM size. |
| Is migration zero downtime? | Do not promise it. Validate versions, extensions, CDC, cutover, rollback, connections and application behavior. |

Unknown response: “I don't know the exact behavior for that configuration. I'd confirm it with our solutions engineer and the current docs, then include it in the evaluation.”
