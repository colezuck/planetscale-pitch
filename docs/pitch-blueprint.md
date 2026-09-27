# PlanetScale pitch blueprint

Prepared 27 September 2026. Original analysis, followed by the implemented v2 update below.

## Implemented v2 update

The user clarified that hosted Postgres on Metal is the central offer, with speed and reliability first and Neki as the growth path. V2 therefore opens with “Your Postgres. Faster on Metal” and a local-NVMe architecture diagram, while keeping the buyer-oriented discovery question in the spoken introduction. The remaining order follows this blueprint: Vitalize, operated HA platform, Metal performance, Neki architecture, Neki scale, migration close. Durable evidence lives in `customer-case-studies.md` and `postgres-metal-benchmarks.md`.

## Layout refinement

The latest user-approved direction prioritizes screen space. Keep the PlanetScale logo on the opening slide only. All six content slides use single-line headings. Vitalize's secondary vCPU claim belongs over the compute chart. Diagram-heavy slides use the reclaimed header space for larger, readable artwork and separation between elements. This supersedes the longer working headlines below.

The architecture slide now omits the Cash App proof row entirely, at the user's request. Its full content area is reserved for the application endpoints, three-zone topology, replication, and control plane. Cash App remains research context only; the older proposed proof-row placement below is superseded.

## Audience, objective, and constraints

General Postgres prospect. CTO and technical leaders. Seven slides total, with two Neki slides toward the end. Core presentation: 11 minutes 30 seconds, with room for short exchanges within a 15-minute meeting segment. The next step is technical discovery plus a migration assessment.

The buyer should leave understanding what PlanetScale would operate, why the architecture is credible, what evidence merits a workload evaluation, and how their team could assess a migration. The pitch should earn a technical evaluation rather than try to close a platform purchase in one conversation.

Keep the current PlanetScale visual direction: dark backgrounds, original logos, Inter headlines, monospace technical labels, square node outlines, sparse orange highlights, and yellow for Neki. Gong is the reference for sales structure, not visual branding.

## What the Gong presentation actually recommends

Source: Sales Presentation Template.pptx, 27 slides, supplied by the user. All slide text and notes were extracted, and the rendered slides and embedded examples were inspected.

The file offers five slide replacements. It is not a mandatory five-slide sequence or a rule against all technical evidence.

| Gong guidance | Source slides | Application here |
| --- | --- | --- |
| Replace a company introduction with a buyer-relevant insight, called a nexus | 3–6 | Open with the operating work behind growing Postgres, then establish which part matters to this prospect. |
| Replace feature lists with a recognizable problem | 8–11 | Connect each architecture element to a concrete job: routing reads, recovering service, or managing changes. |
| Replace abstract ROI promises with a customer story | 13–16 | Move Vitalize forward. Explain its original deployment, its migration, and its reported results. |
| Replace a feature comparison contest with a clear value proposition | 18–21 | Establish PlanetScale's operating model before showing comparative benchmark evidence. |
| Replace an indiscriminate logo wall with relevant evidence | 23–26 | Vitalize supports the Postgres decision. Cash App supports the team's experience at scale. Keep those roles distinct. |

Gong's percentage claims describe correlations in its material. They do not establish that any individual slide format causes a specific sales result. Its customer-story example also uses numbers prominently. The useful lesson is to explain whose result a number represents and why it matters, not to remove numbers.

## Assessment of the existing deck

The technical material and visual direction are useful. The sequence is doing less sales work than it could:

- The opening introduces PlanetScale and immediately shows a very large Vitess/MySQL customer. A general Postgres buyer has not yet been given a reason to see themselves in the story.
- HA architecture and a competitive benchmark arrive before the relatable Postgres migration story.
- Vitalize's chart shows the result after migration, but its current layout does little to establish the starting situation or explain the change.
- Migration, a major buyer concern and the agreed next step, appears before two more technical slides. That interrupts the path to the close.
- The final slide's dominant memory is 118.5 million QPS. The request for a technical meeting is visually secondary.
- The current timed notes add up to approximately 13 minutes 30 seconds before buyer responses. Neki occupies 3 minutes 30 seconds of that. Its role should be a concise expansion of the story after the immediate Postgres offer is understood.

## Recommended seven-slide sequence

| # | Working headline | Purpose | Main visual | Talk time |
| --- | --- | --- | --- | --- |
| 1 | Growing Postgres takes more than compute | Make the operating problem relevant and establish the buyer's priority | Simple application/database schematic showing the operational work around the database | 1:15 |
| 2 | Vitalize: 2 ms p95, half the vCPUs | Give the buyer a credible, relatable customer story | Explicit Supabase/PlanetScale compute comparison plus the actual PlanetScale latency plot | 1:45 |
| 3 | Your Postgres. Operated by PlanetScale | Explain what the platform and team take responsibility for | Three-zone HA diagram, read routing, separate control plane, and a compact Cash App proof row | 2:00 |
| 4 | Postgres on Metal: throughput and p99 | Substantiate the performance proposition | Existing throughput bars and p99 trace, with clear provider and workload labels | 1:45 |
| 5 | Neki: Postgres across shards | Explain the architecture available for the scale discussion | Router, PostgreSQL shard groups, replicas, and control plane | 1:15 |
| 6 | Neki: 118.5M queries per second | Show what the published scale benchmark demonstrated | QPS by shard count; one primary metric and supporting workload labels | 1:00 |
| 7 | Your migration, with our infrastructure team | Resolve the switching question and secure the next meeting | Migration flow with a prominent technical discovery and migration assessment close | 2:30 |

Total core talk track: 11:30. Short buyer exchanges can bring this to 13–15 minutes. Longer technical discussions can extend the meeting or replace detail on subsequent slides.

### 1. Growing Postgres takes more than compute

**Buyer takeaway:** Additional capacity still leaves an operating responsibility.

**Screen:** One headline and a simple technical composition. Show application traffic into Postgres, with the surrounding jobs labeled in familiar terms: latency, failover, and capacity changes. No invented growth curve, prospect baseline, business-impact table, or company-history block. A compact PlanetScale/Postgres identity is sufficient.

**Talk track:** “When database pressure rises, a larger instance is an obvious response. But someone still owns the slow requests, the failover, and the production changes. PlanetScale operates that infrastructure alongside your team.”

**Discovery pause:** “Which of those is taking the most engineering attention today?” Let the response change the emphasis of the pitch. With a general mock prospect, frame these as possible constraints rather than discovered facts.

**Transition:** “Vitalize gives us a concrete Postgres example.”

### 2. Vitalize: 2 ms p95, half the vCPUs

**Buyer takeaway:** A team running a substantial Postgres workload made this move and reported measurable results.

**Screen:** Identify Vitalize as hospital staffing software, with 400 GB and 150 million rows. Make the compute comparison explicit: Supabase 4 vCPU versus PlanetScale 2 vCPU, 16 GB RAM on both. Keep the original latency curve clearly labeled “PlanetScale / after migration.”

**Talk track:** Tell a short sequence: their existing deployment, the difficult workload, the move to PlanetScale Metal, and the reported result. The customer remains the subject of the story.

The article separately reports reads on a 200 GB JSONB-heavy table averaging 50 seconds before and reaching a maximum of 1.2 seconds after. Those statistics are different. They may be spoken with both labels, but should not become a paired latency bar chart or a calculated speedup. No pre-migration p95 is published. A hardware reduction also does not establish a 50% cost saving.

**Transition:** “Here is the infrastructure and operating model behind that result.”

### 3. Your Postgres. Operated by PlanetScale

**Buyer takeaway:** PlanetScale offers an operated database platform, with a defined data path and control plane.

**Screen:** Preserve the three-zone architecture. Show the application endpoints, primary and read replicas, then the separate control plane. Keep the 99.99% single-region HA SLA clearly identified as an SLA. Local NVMe can be labeled at the database layer without adding a second hardware diagram.

**Talk track:** Explain the picture in this order: application connection; primary and replica reads; replication and recovery; the operator's responsibilities. Provisioning, failover, resizing, and upgrades should connect to the responsibilities introduced on slide 1. Avoid reading every component label aloud.

**Cash App:** Move the existing proof from the opening to a compact row here. Use the logo, an explicit “Vitess / MySQL” label, and at most two numbers, such as roughly 400 TiB and 3–4 million peak QPS. Verbally identify this as evidence of PlanetScale's experience operating databases at scale. It is not evidence that Cash App runs PlanetScale Postgres or Neki. Protect diagram space rather than retaining all three original Cash App metrics.

**Transition:** “The storage architecture matters when we look at tail latency under load.”

### 4. Postgres on Metal: throughput and p99

**Buyer takeaway:** There is a concrete performance hypothesis worth testing against their workload.

**Screen:** Retain the existing published provider throughput chart and PlanetScale/Aurora p99 trace. Keep provider names, units, and the workload definition visible. Treat those as essential chart context rather than filler. Do not introduce a feature matrix, an unqualified fastest claim, or an assumed financial return.

**Talk track:** Explain local NVMe briefly. Point to the throughput comparison, then the tail latency behavior. Finish with the proposed evaluation: representative queries, p95/p99, errors, concurrency, and resource use. The configuration differences and precise methodology belong in notes and should be explained when relevant.

**Buyer pause:** “Which workload would we need to reproduce for this to be meaningful to you?”

**Transition:** “If the constraint eventually becomes the capacity of one database machine, the next architecture is sharding.”

### 5. Neki: Postgres across shards

**Buyer takeaway:** PlanetScale can have a concrete technical discussion about growth beyond a single Postgres machine.

**Screen:** Black and yellow. Keep the Neki logo and technical diagram. The router and repeated shard groups should be understandable before the audience studies smaller labels. Show replicas and the separate control plane without turning this into a component inventory.

**Talk track:** The application speaks to a router; work reaches the relevant PostgreSQL shards; the control plane manages topology and operational workflows. Connect the architecture to capacity growth. Do not imply the prospect must shard now or that arbitrary single-node Postgres queries and transactions carry over unchanged.

Current availability, preview status, query compatibility, and migration boundaries must be verified before presentation and communicated verbally where relevant. These belong in speaker notes rather than generic marketing caveats across the slide.

**Transition:** “The published benchmark lets us put numbers behind that architecture.”

### 6. Neki: 118.5M queries per second

**Buyer takeaway:** There is measured evidence behind the scale discussion, with a defined workload.

**Screen:** Keep the 5, 50, and 512-shard series. Make 118.5M QPS the dominant figure. Retain the read-only point-select and primary-only workload labels. The 1.22 PiB dataset is a useful supporting scale metric. If the 6.06 ms number remains, label it router p99; it is not application end-to-end p99.

**Talk track:** Spend about a minute. Explain what was measured, what scaling the number of shards demonstrated, and why it is relevant to the long-term architecture discussion. This is a synthetic benchmark, distinct from the replicated HA topology on the previous slide and from Cash App's production case.

**Transition:** “For your team, the immediate question is the current workload and the path to moving it.”

### 7. Your migration, with our infrastructure team

**Buyer takeaway:** There is a specific, collaborative next step with concrete evaluation outputs.

**Screen:** Reuse the migration flow. Show the source serving during copy and change replication, target validation, and the eventual application cutover. Give “Technical discovery + migration assessment” its own strong visual position. Keep the rest of the copy short.

**Talk track:** Rehearse before cutover. Assess schema, extensions, and application dependencies. Agree on representative performance tests and success criteria. Map the final synchronization, validation, application change, and rollback approach to the actual source setup. Do not promise universal zero downtime or an automatic migration to Neki.

**Close:** “Can we schedule a technical discovery with your database and infrastructure leads? We can use your workload, latency targets, and availability requirements to scope the migration assessment.”

The proposed session should establish compatibility questions, a target deployment to evaluate, success criteria, and the next work needed for a migration plan. A fixed implementation date is not the request being sold here.

## Tempo and delivery rules

- Use the first 75 seconds to establish relevance and invite a short response. Do not spend it on vendor credentials.
- Show a recognizable customer by slide 2. The buyer should know why the technical explanation matters before the HA diagram appears.
- Alternate story and explanation. Let diagrams support the spoken narrative rather than read their labels as a feature list.
- Cap the two Neki slides at 2:15 total in the core talk track. Keep the scale discussion proportional to a general Postgres prospect's immediate needs.
- Reserve the final 2:30 for migration and the proposed meeting. If time runs short, compress architecture detail rather than rush the close.
- Pause briefly after a customer result or a large benchmark number. State the takeaway, then let the audience inspect the visual.
- Use purposeful reveals for complex data flows if they improve comprehension. Avoid automatic animation or transitions that control the speaker's tempo.
- Keep essential metric definitions on screen. Keep references, technical detail, and longer qualifications in speaker notes. Avoid generic section labels and presenter coaching on slides.

## Proposed changes to the current build

1. Rewrite the current opening around the operating problem and remove the Cash App proof row from it.
2. Move Vitalize to position 2 and make its customer story explicit in the spoken track.
3. Move availability to position 3 and add a concise, clearly separated Cash App operating-experience proof row.
4. Keep Metal at position 4, framed as evidence supporting a workload evaluation.
5. Move the two Neki sections to positions 5 and 6 and shorten their spoken track.
6. Move migration to position 7 and make the concrete next step its close.
7. Rebuild notes with the timing and transitions above. Preserve existing slide IDs so direct browser links remain useful.

No new company overview, agenda, ROI calculator, logo wall, or thank-you slide is needed. The seven-slide constraint is met without combining migration and Neki into the same closing slide.


## Opening revision — product introduction

Slide 1 introduces the offer: fully managed Postgres on Metal, Neki as the horizontal scaling product, and the PlanetScale platform and infrastructure team beneath both. This product map supersedes the opening node diagram. Reserve replicas, replication paths, and control-plane topology for slide 3. Keep the opening to 75 seconds; emphasize Postgres on Metal now and briefly introduce Neki before moving to Vitalize. The product relationship does not imply an automatic migration to Neki.


## Availability terminology verified

Slide 3 now uses “Postgres Cluster Architecture” with a primary node and two replica nodes inside explicitly named availability-zone containers. This preserves the distinction between database instances and cloud failure boundaries. The connection boxes describe application routing choices rather than separate DNS endpoints. The slide labels the management layer “Control plane”; operator implementation details stay in speaker notes. Research and exact connection/SLA qualifications live in `docs/postgres-architecture.md` and the speaker notes.


## Customer-story candidates — current working deck

The user asked to build Convex and Autumn as additional slides and defer final selection. The original seven slides, including Vitalize and the migration close, are preserved. Convex and Autumn are appended in positions 8 and 9. This supersedes the seven-slide limit for the working version only; it is not a claim that the final sequence or timing is settled.

Convex follows the Gong customer-story structure: an infrastructure buyer's need, Chef's named workload, the move from Aurora, then reported p99 ranges. Autumn connects a critical billing workload and migration concern to a guided two-day move, seconds of cutover downtime, and observed Metal latency. References and qualifications stay in notes.


## Current closing sequence

The nine-slide working order now finishes with Convex (7), Autumn (8), and migration (9). Autumn’s assisted migration naturally sets up the prospect’s own assessment. Close on technical discovery plus migration assessment, leaving the migration slide visible during the discussion. This supersedes the appended-candidate order above; no slides were removed. The current scripted timing is about 14 minutes before buyer exchanges, so final story selection or shorter delivery is still useful for a 10–15 minute meeting.
