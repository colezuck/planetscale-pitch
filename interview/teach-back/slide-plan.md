# Metal teach-back slide plan

Audience: Aurora PostgreSQL staff engineer. Target: five minutes plus questions. One clean cover and five teaching slides. [Assignment](../brief/README.md), [evidence](../../context/product/aurora-metal-teach-back.md), [script](script-outline.md).

| ID / time | Purpose | Visual and reveal |
| --- | --- | --- |
| `problem` / 0:00–0:15 | Introduce Metal | PlanetScale and Metal on one line. |
| `aurora` / 0:15–1:35 | Current situation and conditional problem | Aurora instance → remote shared SSD volume. Grow the instance taller, with larger CPU and RAM; grow the SSD frame taller. Keep network connector height stable. Aurora volume growth remains independent of compute. Remove cache-miss and storage-growth captions. Headings: AWS Aurora Postgres architecture → Scale up → Network Hop remains → Bottleneck → Network Hop for Storage I/O. Under network connector: io2 ~400 µs and gp3 ~1 ms as illustrative EBS references. Explicitly not Aurora or isolated hop measurements in notes. |
| `metal` / 1:35–2:40 | Explain storage placement | Original pitch EBS/local-NVMe hardware artwork. Title What is Metal? Show io2 ~400 µs, gp3 ~1 ms, and ~50 µs illustrative NVMe access immediately, with no reveal animation; EBS is explicitly named, not mislabeled as Aurora. |
| `benchmark` / brief proof | Benchmark evidence | Exact original “More QPS & Lower p99” slide copied from the Postgres pitch, after What is Metal. Workload-specific result. |
| `convex` / target 45–55 seconds | Aurora customer proof | Exact original Convex slide from Postgres pitch: logo, two original chart panels, query and batch-commit p99 results, quote and styling. No reconstruction. |
| `fit` / target 45–60 seconds | Tradeoff and evaluation | Art-free five-row comparison: local versus network I/O; fixed drive versus automatic volume growth; data-copy resize versus separate compute resize; Metal no separate IOPS tier versus Aurora Standard/I/O-Optimized billing; workload decision. Header uses Aurora, not PostgreSQL or Aurora EBS. All content visible together. |

Stable prior anchors are retained. Footers, side notes, replication and AZ detail are excluded from the visible narrative. Qualifications live in the script, Q&A, accessibility descriptions and evidence. The Depot comparator remains visible because it changes what the result means. No universal storage latency, throughput, cost or percentile improvement is promised.

Review base/reveal/reverse/direct-hash/revisit states and portable delivery at 16:9. Aloud rehearsal remains. Working story and brainstorming: [Notion outline](https://app.notion.com/p/3ef1840cbb9e8105a768d99d5570e754), reconciled October 4, 2026.

Depot is temporarily hidden with `hidden: true` in `content.json`; it is excluded from audience and presenter output. Its art remains in `assets/` and its rehearsal script is saved in [depot-hidden-script.md](depot-hidden-script.md).
