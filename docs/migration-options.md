# Postgres migration options

Verified 2026-09-27. Sources belong in the notes; the closing slide stays concise.

## Self-service migration

The customer’s engineers run the assessment, choose an appropriate documented migration method, validate, and cut over. PlanetScale offers migration guides and tooling. This is not a universal one-click Postgres importer. Methods include dump and restore, WAL streaming using logical replication, and pgcopydb. Source-provider capabilities determine which approach is appropriate.

## PlanetScale-led migration

PlanetScale’s migration specialists can support the full process, from assessment and a custom strategy through environment setup, data transfer, validation, and cutover. Agree on ownership, scope, timing, and commercial terms during the assessment. “PlanetScale-led” is deck wording for these services, not a formal plan name.

These services are not restricted to Enterprise customers. PlanetScale advertises complimentary migrations for eligible YC and select high-growth companies, and variable pricing by workload complexity, database size, and timeline. Do not promise universal free service, a fixed duration, or guaranteed zero downtime.

## Closing structure

- Title: Migrate to PlanetScale
- Shared destination: PlanetScale Postgres on Metal
- Paths: Self-service migration / PlanetScale-led migration
- One next step: Technical discovery + migration assessment
- Session outcome: Confirm compatibility, performance targets, and the migration approach

After Autumn’s customer evidence, this slide gives the buyer control over delivery ownership and a concrete next meeting. It replaces the previous detailed migration mechanism and three-step row.

The source may continue serving traffic during initial copy and replication, depending on the method. WAL-streaming cutover includes stopping source writes, waiting for replication to catch up, and changing application connections. Recovery and rollback must account for target-side writes. The compact slide arrow conveys destination only.

## Sources

- [Migration services and self-service options](https://planetscale.com/migrate)
- [WAL streaming migration guide](https://planetscale.com/docs/postgres/imports/postgres-migrate-walstream)
- [Postgres Discovery Tool](https://planetscale.com/docs/postgres/imports/discovery-tool)
- [Migration guides and open-source scripts announcement](https://planetscale.com/changelog/postgres-migration-guides-scripts)
