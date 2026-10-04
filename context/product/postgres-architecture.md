# Postgres HA terminology and connection paths

Verified against PlanetScale documentation on 2026-09-27.

## Hierarchy

The deployment is a **Postgres cluster**. The standard HA configuration contains three database **nodes**, also called **instances**: one primary and two replicas. Each runs in a separate **availability zone** within one cloud **region**. An availability zone is a cloud location/failure boundary, not a database node. Additional read replicas can be added. This diagram does not describe a single-node plan.

PlanetScale's [architecture documentation](https://planetscale.com/docs/postgres/postgres-architecture) specifies one primary instance, two replica instances, and distribution across availability zones within a region. Its [operations philosophy](https://planetscale.com/docs/postgres/operations-philosophy) explicitly calls this a three-node configuration.

## Slide labels

- Title: Planetscale Postgres Architecture
- Outer containers: Availability zone A / B / C. These letters are schematic, not provider-specific AZ identifiers.
- Inner boxes: Primary node / Replica node / Replica node.
- Application: explicitly selects a primary or replica connection.
- Primary path: Primary connection, used for writes and fresh reads.
- Replica path: Replica connection, explicitly selected by the application.
- Management: Control plane, separate from the query path.

The current art omits connection-pool internals. The sections below preserve the researched connection behavior; they do not describe additional boxes on the slide.

The operator manages creation, version upgrades, resizes, and failovers. It is a management component, not a database node or query hop. The [operations documentation](https://planetscale.com/docs/postgres/operations-philosophy) also confirms semi-sync replication and acknowledges brief disruptions during failovers and changes.

## Connection and replication precision

The [replica documentation](https://planetscale.com/docs/postgres/scaling/replicas) says replica reads require explicit application selection. The [PgBouncer documentation](https://planetscale.com/docs/postgres/connecting/pgbouncer) specifies that local PgBouncer runs on the primary node and serves primary connections on port 6432. It does not inspect queries to automatically send reads to replicas.

Local PgBouncer serves primary connections. The orange path in the simplified diagram carries writes and reads requiring the primary's visibility. Replica reads follow a separately selected connection. An optional dedicated replica PgBouncer can distribute read traffic across replicas; zone affinity affects that distribution. Dedicated pools use port 6432 and a pool-name username suffix. Direct replica access on port 5432 with a `|replica` username suffix is another option. Pool internals and ports are omitted from the current artwork.

Dedicated primary PgBouncers are another optional deployment: application → dedicated primary pool → local PgBouncer → primary Postgres. This additional layer can preserve client connections through more lifecycle events. It is not shown as a default component. Logical query paths and database placement are shown; TLS termination, network proxies, pool redundancy, and provider networking are omitted.

Replica reads can lag. Successful commits require durable confirmation by at least one replica. A fresh-read connection targets the primary; transaction isolation and the application's own snapshots still determine what is visible.

## Availability figure

The [SLA](https://planetscale.com/legal/planetscale-service-level-agreement), updated 2026-08-27, specifies a 99.99% monthly uptime commitment for single-region clusters when incorporated into the customer's agreement. Single-node clusters and beta features are excluded. Keep the slide label “single-region HA SLA”; do not call it an observed uptime measurement or zero-downtime guarantee.
