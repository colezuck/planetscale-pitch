# Postgres HA terminology and slide 3

Verified against PlanetScale documentation on 2026-09-27.

## Hierarchy

The deployment is a **Postgres cluster**. The standard HA configuration contains three database **nodes**, also called **instances**: one primary and two replicas. Each runs in a separate **availability zone** within one cloud **region**. An availability zone is a cloud location/failure boundary, not a database node. Additional read replicas can be added. This diagram does not describe a single-node plan.

PlanetScale's [architecture documentation](https://planetscale.com/docs/postgres/postgres-architecture) specifies one primary instance, two replica instances, and distribution across availability zones within a region. Its [operations philosophy](https://planetscale.com/docs/postgres/operations-philosophy) explicitly calls this a three-node configuration.

## Slide labels

- Title: One cluster. Three nodes.
- Outer containers: Availability zone A / B / C. These letters are schematic, not provider-specific AZ identifiers.
- Inner boxes: Primary node / Replica node / Replica node.
- Application choices: Primary connection / Replica connection.
- Management: Control plane, with Custom Kubernetes operator beneath it.

The operator manages creation, version upgrades, resizes, and failovers. It is a management component, not a database node or query hop. The [operations documentation](https://planetscale.com/docs/postgres/operations-philosophy) also confirms semi-sync replication and acknowledges brief disruptions during failovers and changes.

## Connection and replication precision

The [replica documentation](https://planetscale.com/docs/postgres/scaling/replicas) says replica reads require explicit application selection, using a replica credential/username suffix with direct connections on 5432. Default PgBouncer connections on 6432 target the primary; dedicated replica PgBouncers are a separate option. The slide's connections represent routing choices, not separate hostnames or automatic read/write splitting. Replica reads can lag. Successful commits require durable confirmation by at least one replica.

## Availability figure

The [SLA](https://planetscale.com/legal/planetscale-service-level-agreement), updated 2026-08-27, specifies a 99.99% monthly uptime commitment for single-region clusters when incorporated into the customer's agreement. Single-node clusters and beta features are excluded. Keep the slide label “single-region HA SLA”; do not call it an observed uptime measurement or zero-downtime guarantee.
