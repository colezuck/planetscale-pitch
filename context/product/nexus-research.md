# Nexus: the common managed cloud Postgres model

Verified September 27, 2026.

The slide first establishes a common capacity model: a Postgres compute instance with vCPU/RAM and separately scalable storage reached over a network. It then grows those resources before revealing latency, storage I/O, and availability as discovery topics. It shows only the compute and storage components.

## Evidence for the model

| Source | What it supports | Boundary |
| --- | --- | --- |
| [PlanetScale: IO devices and latency](https://planetscale.com/blog/io-devices-and-latency) | Describes separation of compute and storage as a cloud default, and identifies network storage as the approach used by most cloud database providers. | An engineering explanation by a vendor; does not measure market share. |
| [PlanetScale: Benchmarking Postgres](https://planetscale.com/blog/benchmarking-postgres) | States that the compared services used network-attached storage underneath. The comparison includes major managed Postgres offerings. | Applies to tested configurations; storage implementations and caching layers differ. |
| [Amazon RDS storage](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html) | RDS for PostgreSQL uses EBS storage. Volume performance and instance limits both affect available I/O capacity. | Aurora is a different storage architecture. |
| [Cloud SQL overview](https://docs.cloud.google.com/sql/docs/postgres/introduction), [instance settings](https://docs.cloud.google.com/sql/docs/postgres/instance-settings), [storage options](https://docs.cloud.google.com/sql/docs/postgres/storage-options-overview) | A VM runs Postgres with durable network storage. CPU/memory and storage capacity are configurable; newer series use Hyperdisk network block storage. | Available options depend on machine series and edition. |
| [Azure PostgreSQL storage](https://learn.microsoft.com/en-us/azure/postgresql/compute-storage/concepts-storage), [scaling resources](https://learn.microsoft.com/en-us/azure/postgresql/scale/concepts-scaling-resources) | Flexible Server uses Azure managed disk volumes. Compute tier/SKU and storage tier/size can scale separately. | Premium SSD v2 capacity, IOPS, and throughput can be adjusted independently. |

The independent provider documentation supports the inference that this is a common industry pattern. The diagram avoids a quantified claim that a particular percentage of providers uses an identical topology. It uses no provider logos or EBS labels. It abstracts Aurora/AlloyDB/Neon's more elaborate storage services rather than claiming they expose a literal block volume identical to RDS or Cloud SQL.

## How to frame the challenge

| Topic | Accurate question beyond capacity |
| --- | --- |
| Latency | Which parts of the application or query path drive tail latency, and how does it change under load? CPU/RAM, cache behavior, query plans, locks, and I/O can all matter. |
| Availability | How does the configured HA system handle failure and maintenance, and what does the application experience during recovery? Resizing alone does not answer this. |
| Storage I/O | Is usable I/O performance limited by volume performance, instance bandwidth, workload, or queueing? Capacity and I/O performance are distinct. |

[Cloud SQL's HA documentation](https://docs.cloud.google.com/sql/docs/postgres/high-availability) explicitly describes standby instances, synchronous replication, and automatic failover. Existing managed providers support these capabilities. Removing replicas from this capacity diagram is a visual simplification, not a claim that the services lack HA.

[PlanetScale's Metal explanation](https://planetscale.com/blog/planetscale-metal-theres-no-replacement-for-displacement) motivates local NVMe by the storage network path and its I/O tradeoffs. The later Metal slide should explain that mechanism; the availability slide should explain the operated HA platform. Local NVMe alone is not an HA system.

## Presentation sequence

1. **Arrival:** “How Postgres typically runs and scales in the cloud.” Show server vCPU/RAM and a separate network-attached volume.
2. **First click:** Increase the shapes and label the resource levers: more vCPU, more RAM, more storage. This is a conceptual growth cue, not a fixed specification or a requirement to grow all three together.
3. **Second click:** Change the headline to “More compute doesn’t solve every Postgres bottleneck.” Reveal Latency, Storage I/O, and Availability outside the architecture boundary, then pause for discovery.

Managed operations, backups, maintenance, recovery tests, and connection handling belong in the presenter notes. The current PDF shows the scaled model and bottleneck reveal on separate pages.
