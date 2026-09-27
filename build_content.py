"""Editable deck content and vector diagrams. Run to rebuild slides.js and notes."""
from pathlib import Path
import json, html
R=Path(__file__).resolve().parent
INK='#111111'; PANEL='#111111'; LINE='#dadada'; WHITE='#fafafa'; GRAY='#a5a5a5'; ORANGE='#f35815'; BLUE='#dadada'; YELLOW='#fbca00'
def txt(x,y,s,size=24,color=WHITE,anchor='start',weight=400,mono=True):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" font-family="{("ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" if mono else "Inter,Arial,sans-serif")}">{html.escape(s)}</text>'
def rect(x,y,w,h,fill=PANEL,stroke=LINE,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" rx="{rx}"/>'
def path(d,color=LINE,width=2,dash=False,arrow=None):
    attrs = ' stroke-dasharray="11 9"' if dash else ''
    if arrow: attrs += f' marker-end="url(#{arrow})"'
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{attrs}/>'

def svg(w,h,body,label,mark='arr',color=WHITE):
    patterns=''.join(f'<pattern id="{mark}-{key}" width="7" height="7" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="1.3" height="2.4" fill="{c}"/><rect x="4.5" y="4.5" width="1.3" height="2.4" fill="{c}"/></pattern>' for key,c in [('dots',WHITE),('accent',ORANGE),('yellow',YELLOW)])
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(label)}"><defs>{patterns}<marker id="{mark}" markerWidth="7" markerHeight="7" refX="6.5" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7Z" fill="{color}"/></marker></defs>{body}</svg>'
def db(x,y,w=170,h=94,color=LINE):
    return rect(x,y,w,h,INK,color)+rect(x+4,y+4,w-8,h-8,'none',color)
def stipple_box(x,y,w,h,label,mark,color=WHITE,size=24):
    return rect(x,y,w,h,INK,color)+rect(x+6,y+6,w-12,h-12,f'url(#{mark})','none')+rect(x+w/2-len(label)*size*.33-12,y+h/2-19,len(label)*size*.66+24,38,INK,'none')+txt(x+w/2,y+h/2+size*.34,label,size,color,'middle')

# Opening: the managed Metal cluster is the hero, with a separate operating plane.
b=rect(285,1,964,490,INK,'#555555')
b+=txt(310,35,'PlanetScale Metal',22,WHITE)
b+=txt(1223,35,'Compute + storage, colocated',18,GRAY,'end')
b+=stipple_box(1,125,244,76,'Your application','metal-hero-dots',WHITE,20)
for x,role,color in [(330,'Primary',ORANGE),(635,'Replica',WHITE),(940,'Replica',WHITE)]:
    b+=rect(x-15,64,275,288,INK,'#777777')
    b+=(db(x,86,245,114,color) if role=='Primary' else rect(x,86,245,114,INK,color))
    b+=f'<image href="assets/postgresql.svg" x="{x+21}" y="111" width="42" height="44"/>'
    b+=txt(x+77,131,'Postgres',25,WHITE)+txt(x+77,170,role,20,color)
    b+=path(f'M{x+122.5} 201V244',color,1.8,True,arrow='metal-hero')
    b+=stipple_box(x,256,245,67,'Local NVMe','metal-hero-accent',ORANGE,23)
b+=path('M246 163H328',ORANGE,2,True,arrow='metal-hero')
b+=path('M452.5 353V378H1062.5V354',GRAY,1.5,True,arrow='metal-hero')
b+=path('M757.5 378V354',GRAY,1.5,True,arrow='metal-hero')
b+=txt(757,406,'Replication',19,GRAY,'middle')
b+=rect(310,431,914,43,INK,'#aaaaaa')
b+=txt(329,459,'Control plane',22,WHITE)
b+=txt(1203,458,'Provision / Monitor / Fail over / Upgrade',19,GRAY,'end')
servers=svg(1250,494,b,'Your application connects to a Postgres primary on PlanetScale Metal. Each of the three database nodes pairs Postgres compute with local NVMe storage. The primary replicates to two replicas. A separate PlanetScale control plane operates the infrastructure.',mark='metal-hero')

# HA: full-height architecture makes the query paths and control plane the focus.
b=stipple_box(470,0,310,52,'Application','ha-arrow-dots',WHITE,25)
b+=path('M560 53V78H175V108',ORANGE,2,True,arrow='ha-arrow')+txt(213,101,'Writes + fresh reads',20,ORANGE)
b+=path('M690 53V78H888V108',BLUE,2,True,arrow='ha-arrow')+txt(915,101,'Replica reads',20,BLUE)
b+=rect(25,113,300,52,stroke=ORANGE)+txt(175,147,'Primary endpoint',24,anchor='middle')
b+=rect(730,113,315,52,stroke=BLUE)+txt(888,147,'Replica endpoint',24,anchor='middle')
b+=path('M175 166V272',ORANGE,2,True,arrow='ha-arrow')
b+=path('M888 166V193H625V272',BLUE,2,True,arrow='ha-arrow')+path('M888 193H1075V272',BLUE,2,True,arrow='ha-arrow')
for x,label,role,color in [(0,'ZONE A','Primary',ORANGE),(450,'ZONE B','Replica',BLUE),(900,'ZONE C','Replica',BLUE)]:
    b+=rect(x,228,350,177,'none','#555555')+txt(x+18,255,label,18,GRAY)
    b+=(db(x+79,280,192,100,color) if role=='Primary' else rect(x+79,280,192,100,INK,color))+txt(x+175,340,role,29,anchor='middle')
b+=path('M272 330H524',GRAY,1.8,True,arrow='ha-arrow')+txt(398,311,'Replication',19,GRAY,'middle')
b+=path('M175 382V429H1075V383',GRAY,1.8,True,arrow='ha-arrow')+txt(628,456,'Semi-synchronous replication',20,GRAY,'middle')
b+=rect(0,484,1250,65,INK,'#aaaaaa')+txt(24,525,'Control plane',27,WHITE,weight=500)
b+=txt(419,525,'Provision',23,GRAY)+txt(674,525,'Fail over',23,GRAY)+txt(884,525,'Resize',23,GRAY)+txt(1060,525,'Upgrade',23,GRAY)
for x in (27,1223):b+=path(f'M{x} 484V406','#777777',1.5,True)
ha=svg(1250,553,b,'A primary and two read replicas across three availability zones. Primary and replica endpoints route application traffic. Semi-synchronous replication connects the nodes. The separate control plane provisions, fails over, resizes and upgrades them.',mark='ha-arrow')

# Throughput bars and real one-second p99 samples, kept as native vector charts.
qps_source=json.loads((R/'qa/benchmark-qps.json').read_text())
providers=[(name, sum(a['values'])/len(a['values']), color) for name,color in [('PlanetScale',ORANGE),('Aurora','#8b8b8b'),('AlloyDB','#707070'),('Supabase','#555555')] for a in qps_source['series'] if a['name']==name+' 32conns']
b=''
for i,(name,value,color) in enumerate(providers):
    y=37+i*83
    b+=txt(0,y,name,22,WHITE if i==0 else '#c5c5c5')+txt(538,y,f'{value/1000:.1f}k',27,WHITE,'end',500)
    b+=rect(0,y+15,538,22,'none','#333333')+rect(0,y+15,538*value/18000,22,f'url(#qps-{"accent" if i==0 else "dots"})',ORANGE if i==0 else '#ababab')
bars=svg(550,355,b,'Average throughput in queries per second: PlanetScale 16.3 thousand, Aurora 10.9 thousand, AlloyDB 10.4 thousand, Supabase 5.3 thousand.',mark='qps')
series=json.loads((R/'qa/benchmark-p99.json').read_text())
b=''
for v in [0,200,400,600,800]:
    y=290-v/800*250
    b+=path(f'M52 {y}H575','#3c3c3c',1,True)+txt(38,y+6,str(v),16,GRAY,'end',mono=True)
for t in [0,60,120,180,240,300]:b+=txt(52+t/300*523,321,str(t),16,GRAY,'middle',mono=True)
for name,col in [('Aurora 32conns','#c4c4c4'),('PlanetScale 32conns',ORANGE)]:
    vals=next(s['values'] for s in series if s['name']==name)
    d=' '.join(('M' if i==0 else 'L')+f'{52+i/(len(vals)-1)*523:.2f} {290-v/800*250:.2f}' for i,v in enumerate(vals))
    b+=path(d,col,1.8)
b+=txt(575,352,'seconds',16,GRAY,'end',mono=True)
latency=svg(600,355,b,'p99 latency in milliseconds during the same 300-second benchmark. PlanetScale stays between 170 and 224 ms; Aurora ranges from 326 to 733 ms.',mark='p99')

# Vitalize: the customer's original Query Insights plot, not an invented series.
b=txt(0,24,'PlanetScale / after migration',22,WHITE)
b+=rect(618,12,11,11,'#00b6ec','none')+txt(638,24,'p95',19,GRAY)+rect(715,12,11,11,'#00b868','none')+txt(735,24,'p50',19,GRAY)
b+='<defs><clipPath id="vitalize-plot-clip"><rect x="87" y="63" width="737" height="245"/></clipPath></defs><image href="assets/vitalize-query-latency.png" x="12.124" y="-185.969" width="829.865" height="593.918" preserveAspectRatio="none" clip-path="url(#vitalize-plot-clip)"/>'
for v in [0,0.8,1.6,2.4]:
    y=308-v/2.4*245
    b+=txt(70,y+6,f'{v:.1f}',19,GRAY,'end')
b+=txt(0,49,'ms',16,GRAY)
for i,label in enumerate(['21:00','00:00','03:00','06:00','09:00','12:00','15:00','18:00']):
    source_tick=[282,556,830,1103.5,1377,1652,1926,2200][i]
    b+=txt(87+(source_tick-225)*737/2215,337,label,17,GRAY,'middle')
vitalize_latency=svg(850,350,b,'Vitalize published 24-hour Query Insights plot: p95 in blue, p50 in green. The original plotted image is preserved.',mark='v-latency')
b=txt(0,24,'Half the vCPUs',26,WHITE)+txt(0,56,'vCPU',16,GRAY)
for x,n,provider,col,pat in [(42,4,'Supabase',WHITE,'dots'),(217,2,'PlanetScale',ORANGE,'accent')]:
    top=260-n*44
    b+=rect(x,top,98,n*44,f'url(#v-compute-{pat})',col)+txt(x+49,top-17,str(n),38,col,'middle')+txt(x+49,291,provider,17,WHITE,'middle')
b+=path('M19 260H340','#777777',1)+txt(180,336,'16 GB RAM on both',18,GRAY,'middle')
vitalize_compute=svg(360,350,b,'Compute comparison: Supabase 4 vCPU, PlanetScale Metal 2 vCPU. Both have 16 GB RAM.',mark='v-compute')

# Migration: customer continues running while data is copied and WAL is streamed.
b=stipple_box(0,0,258,84,'Application','m-arrow-dots',WHITE,24)+path('M129 84V152',GRAY,2,arrow='m-arrow')
b+=db(23,167,212,146)+txt(129,249,'Your Postgres',24,anchor='middle')
b+=path('M258 238H453',ORANGE,2,True,arrow='m-arrow')+txt(355,195,'Initial copy',20,GRAY,'middle')+txt(355,282,'Stream changes',20,ORANGE,'middle')
b+=db(478,167,242,146,ORANGE)+txt(599,249,'PlanetScale',27,anchor='middle')
b+=path('M745 238H842',GRAY,2,True,arrow='m-arrow')+rect(863,176,369,128,INK,WHITE)+txt(894,222,'Validate / cut over',26)+txt(894,265,'Switch the connection.',22,GRAY)
b+=path('M258 42H599V158',ORANGE,2,True,arrow='m-arrow')+txt(464,31,'Application cutover',18,ORANGE,'middle')
migration=svg(1250,338,b,'Keep the source database serving traffic while copying data and streaming changes to PlanetScale. Validate the target, then switch the application connection.',mark='m-arrow')

# Neki topology: terminal-style line work adapted from PlanetScale's ASCII language.
b=rect(454,0,342,45,INK,WHITE)+txt(625,30,'Application',23,WHITE,'middle')
b+=path('M625 46V75',WHITE,1.6,True,arrow='n-arrow')
b+=stipple_box(256,82,738,69,'Neki router','n-arrow-yellow',YELLOW,27)
b+=path('M625 152V180H187V211',WHITE,1.8,True,arrow='n-arrow')
b+=path('M625 180V211',WHITE,1.8,True,arrow='n-arrow')
b+=path('M625 180H1063V211',WHITE,1.8,True,arrow='n-arrow')
for i,x in enumerate([0,438,876]):
    b+=txt(x+187,236,f'SHARD 0{i+1}',18,YELLOW,'middle')
    b+=db(x+66,252,242,86,WHITE)+txt(x+187,286,'Primary',25,WHITE,'middle')+txt(x+187,316,'Postgres + sidecar',17,GRAY,'middle')
    b+=path(f'M{x+187} 340V364H{x+83}V386',WHITE,1.6,True,arrow='n-arrow')
    b+=path(f'M{x+187} 364H{x+291}V386',WHITE,1.6,True,arrow='n-arrow')
    for rx in [x,x+208]:
        b+=rect(rx,394,166,58,INK,WHITE)+txt(rx+83,431,'Replica',23,WHITE,'middle')
    b+=path(f'M{x+187} 488V462','#5d5d5d',1.3,True)
b+=rect(0,489,1250,55,INK,'#7b7b7b')+txt(23,525,'Control plane',23,WHITE)+txt(483,525,'Topology / failover / resharding',22,GRAY)
neki=svg(1250,550,b,'An application connects to a Neki router. The router routes to three shards. Each shard has a real Postgres primary with a sidecar and two replicas. The control plane manages topology, failover and resharding.',mark='n-arrow',color=WHITE)

# A genuine scale series: point-read throughput vs shard count, both logarithmic.
import math
points=[(5,999624,'5 shards','1.0M'),(50,9923900,'50 shards','9.9M'),(512,118538803,'512 shards','118.5M')]
b=''
for i,q in enumerate([1e6,1e7,1e8]):
    y=283-math.log10(q/1e6)*110
    b+=path(f'M60 {y}H758','#494331',1,True)+txt(47,y+5,{1e6:'1M',1e7:'10M',1e8:'100M'}[q],17,'#b9a762','end',mono=True)
coords=[]
for shards,q,lab,val in points:coords.append((85+math.log10(shards/5)*315,283-math.log10(q/1e6)*110))
b+=path(' '.join(('M' if i==0 else 'L')+f'{x:.1f} {y:.1f}' for i,(x,y) in enumerate(coords)),YELLOW,3)
for x,y in coords:b+=path(f'M{x} {y+9}V300','#59502d',1,True)
for (x,y),(_,_,lab,val) in zip(coords,points):
    b+=rect(x-5,y-5,10,10,YELLOW,YELLOW)+txt(x,y-23,val,27,YELLOW,'middle',500,True)+txt(x,328,lab,18,'#d0c79c','middle',mono=True)
b+=txt(60,365,'QUERIES / SECOND',15,'#b9a762',mono=True)+txt(756,365,'LOG SCALES',13,'#84784c','end',mono=True)
scale=svg(820,380,b,'Neki read-only point-select benchmark: 5 shards delivered 999,624 QPS; 50 shards delivered 9,923,900 QPS; 512 shards delivered 118,538,803 QPS. Both axes use logarithmic scales.',mark='scale-arrow',color=YELLOW)

slides=[
 dict(id='opening',label='PlanetScale Postgres on Metal',theme='opening',html=f'''<h1>Postgres on <span class="accent">Metal</span></h1><div class="opening-architecture">{servers}</div>''',notes="1:15. “You already run Postgres. We bring the hardware and the operating platform.” Trace the application into the primary, then down to local NVMe. “Compute and storage run together on each machine. We replicate across nodes, and our control plane operates the cluster.” This is a simplified view of an HA Metal cluster; the availability slide adds zones, endpoints, and replication detail. The control plane is separate from the application query path. Connect the architecture to the buyer: faster requests, less infrastructure work, and a path to horizontal scale when needed. Ask: “Which is taking the most engineering attention today: performance, availability, or operating the database?” Keep detailed failover and sizing discussion for later. The immediate offer is hosted Postgres on Metal. Unlimited IOPS is PlanetScale's product wording, not infinite physical throughput. Transition: “Vitalize is one Postgres team that made this move.” Sources: https://planetscale.com/metal and https://planetscale.com/blog/benchmarking-postgres."),
 dict(id='vitalize',label='Vitalize: 2 ms p95, half the vCPUs',theme='vitalize',html=f'''<h2>Vitalize: <span class="accent">2 ms p95</span></h2><div class="customer-story"><span>Hospital staffing software</span><span>400 GB / 150 million rows</span></div><div class="customer-move"><span>Supabase</span><span class="move-line"></span><strong>PlanetScale Metal</strong></div><div class="vitalize-charts"><div>{vitalize_latency}</div><div>{vitalize_compute}</div></div>''',notes='1:45. “Vitalize runs hospital staffing software. They moved a 400 GB Postgres database with 150 million rows from Supabase to PlanetScale Metal. They report about 2 ms p95 on half the vCPUs, with the same 16 GB of RAM.” Tell the customer story before explaining the graphs: demanding database reads, the move, then the result. The latency plot is their actual PlanetScale Query Insights capture after migration, not a paired before/after percentile. No comparable Supabase p95 is published. The 200 GB JSONB-heavy table comparison separately reports 50-second average reads before and 1.2-second maximum reads after; do not calculate a speedup from unlike statistics. The cutover included taking the app offline. These are customer-reported outcomes, not a guarantee. Transition: “Here is the platform operating that database.” Source: https://vitalize.care/blog/from-supabase-to-planetscale . Other cases and suitable alternatives: docs/customer-case-studies.md.'),
 dict(id='availability',label='Your Postgres. Operated by PlanetScale',theme='availability',html=f'''<div class="title-with-stat"><h2>Postgres across three zones</h2><div class="sla"><strong>99.99<span>%</span></strong><p>single-region HA SLA</p></div></div><div class="ha-diagram">{ha}</div>''',notes="2:00. “We operate a primary and two replicas across three availability zones. Your application has a primary endpoint and a replica endpoint; our control plane manages health and production changes.” Trace application traffic first, replication second, management last. Use replicas for reads that tolerate replication lag. Semi-synchronous streaming replication acknowledges from at least one replica. The control plane is outside the SQL query path and handles provisioning, failover, resizing, and upgrades. Backups and point-in-time recovery complement HA. Automatic failover can interrupt connections, so applications need retries. The diagram is a simplified HA topology. 99.99% is the single-region HA SLA under the applicable agreement, not a guarantee of no interruption. It excludes single-node and beta offerings. Hosted infrastructure is the main offer; if data location requires it, assess single-tenancy or PlanetScale Managed in the customer's own AWS/GCP account. Transition: “Local NVMe is the hardware foundation. Let's look at its performance under load.” Sources: https://planetscale.com/blog/benchmarking-postgres ; https://planetscale.com/legal/planetscale-service-level-agreement ; https://planetscale.com/docs/plans/managed ."),
 dict(id='metal',label='Postgres on Metal: throughput and p99',theme='metal',html=f'''<div class="metal-heading"><h2>More throughput. Lower p99</h2><p class="metal-line">Postgres on Metal</p></div><div class="benchmark-grid"><div><h3>Throughput <span>mean queries / second</span></h3>{bars}</div><div><h3>p99 latency <span>milliseconds / 1-second intervals</span></h3><div class="chart-legend"><span class="ps-dot">PlanetScale</span><span class="aurora-dot">Aurora</span></div>{latency}</div></div><p class="workload">TPCC-like / 500 GB / 32 connections / 5-minute run</p>''',notes="1:45. “In this mixed read/write benchmark, Postgres on Metal delivers more throughput and lower p99 than these tested configurations. We can evaluate the same questions against your application.” Left: arithmetic mean QPS across 300 one-second samples with 32 concurrent connections: PlanetScale 16,338.6276; Aurora 10,908.9315; AlloyDB 10,355.0109; Supabase 5,270.2068. Right: one-second interval p99 samples from the same TPCC-like benchmark, not an aggregate run-wide percentile. PlanetScale ranges 170.48–223.34 ms; Aurora 325.98–733 ms. Higher QPS and lower p99 are distinct findings. PlanetScale M-320 has 4 vCPU, 32 GB RAM, and 937 GB local NVMe; Aurora and AlloyDB use 4 vCPU/32 GB; Supabase uses 8 vCPU/32 GB and 12k IOPS. Clients run in each provider's cloud region; AlloyDB uses GCP, the others AWS. Work is sent to the primary, not summed across replicas. These are vendor-run synthetic results with different hardware and infrastructure, not isolated proof that NVMe causes every difference. The site's rounded ~18k headline spans other runs; this deck deliberately uses a single concurrency and exact samples. A separate read-only test has roughly equal average throughput for Aurora and PlanetScale, so do not claim every workload is faster by this ratio. Ask: “Which workload would we need to reproduce for this to matter to you?” Validate p95/p99, throughput, errors, and resource use in discovery. Transition: “When one machine becomes the constraint, Neki extends the architecture across Postgres shards.” Sources: https://planetscale.com/benchmarks ; https://planetscale.com/benchmarks/aurora ; https://planetscale.com/benchmarks/alloydb ; https://planetscale.com/benchmarks/supabase . Data definitions: docs/postgres-metal-benchmarks.md."),
 dict(id='neki',label='Neki: Postgres beyond a single machine',theme='neki',html=f'''<div class="neki-heading"><h2>Postgres beyond one machine</h2><div class="neki-lockup"><img src="assets/neki-cat.svg" alt="Neki cat"><span class="neki-wordmark">[ NEKI ]</span></div></div><div class="neki-topology">{neki}</div>''',notes="1:15. “Neki is our sharded Postgres architecture. Every shard is real Postgres, with routing and operations managed as one database.” Walk from the application to the router, then one shard group, then the control plane. Sidecars pool connections; shard primaries and replicas carry data. The diagram represents replicated HA shard groups, not the primary-only benchmark on the next slide. Say that Neki is available in Platform Preview as of the verified documentation on 27 September 2026; it is not covered by an SLA. The public site's “now available” wording does not mean general availability. Cross-shard transactions remain listed as coming soon. Evaluate shard keys, query/transaction compatibility and the transition from the current database with the team. Do not imply an automatic in-place conversion from ordinary PlanetScale Postgres. The immediate sale remains hosted Postgres on Metal. Transition: “The benchmark demonstrates how far this architecture can scale for a defined workload.” Sources: https://neki.dev/ ; https://planetscale.com/docs/neki ; https://planetscale.com/blog/the-architecture-of-neki ."),
 dict(id='neki-scale',label='Neki: 118.5M queries per second',theme='neki neki-scale',html=f'''<div class="neki-heading"><h2><span class="yellow">118.5M</span> queries / second</h2><span class="neki-wordmark">[ NEKI ]</span></div><div class="scale-layout"><div><div class="scale-chart">{scale}</div><p class="neki-workload">Read-only point selects / Primary-only shards</p></div><div class="scale-metrics"><div><strong>1.22 <span>PiB</span></strong><p>data</p></div><div><strong>512</strong><p>shards</p></div><div><strong>6.06 <span>ms</span></strong><p>router p99</p></div></div></div>''',notes="1:00. “The published Neki run sustained 118.5 million queries per second across 512 shards over a 1.22 PiB dataset.” Follow the 5-, 50-, and 512-shard series and stop. Exact QPS: 999,624; 9,923,900; 118,538,803. Both axes are logarithmic. Workload: read-only, one-row primary-key point selects sent to a single shard. The measured configuration had 512 primary-only shards and 480 routers, without replicas or a failover event, for 16 minutes. It does not establish write performance or HA behavior. The 6.06 ms p99 is at the router; client p99 was 13.95 ms. These metrics do not share the TPCC workload or Vitalize workload and should not be compared on a common chart. Transition: “For your team, the next step is assessing today's Postgres workload and planning the migration.” Source: https://planetscale.com/blog/118-million-queries-per-second-on-neki ."),
 dict(id='migration',label='Your migration with our infrastructure team',theme='migration',html=f'''<h2>Migrate with our infrastructure team</h2><div class="migration-diagram">{migration}</div><div class="migration-steps"><div><span>01</span><strong>Assess</strong><p>Schema, extensions, workload</p></div><div><span>02</span><strong>Rehearse</strong><p>Replication, p95 / p99, recovery</p></div><div><span>03</span><strong>Cut over</strong><p>Validate, switch, monitor</p></div></div><div class="migration-close"><strong>Technical discovery + migration assessment</strong><span>Your team + our database engineers</span></div>''',notes="2:30. “We start with your existing Postgres, assess the dependencies, and rehearse the move with your team.” The source serves traffic during the initial copy and change replication. Validate data and critical queries before agreeing on a cutover. Assess schemas, extensions, write rate, permissions, auth dependencies, connection patterns, recovery requirements, and networking. Compare a representative workload's p95/p99 and throughput. The final synchronization, application connection switch, downtime, and rollback strategy depend on source configuration and any target-side writes. This is a workflow, not a claim that all providers support the same automated importer or universal zero downtime. Close: “Can we schedule a technical discovery with your database and infrastructure leads to scope the migration assessment?” Establish compatibility questions, target deployment, success criteria, and the work needed for a migration plan. If relevant, Autumn reports a two-day migration with seconds of cutover downtime and direct help from PlanetScale; that is an example, not a delivery promise. Source: https://useautumn.com/blog/migrating-to-planetscale ; other references in docs/customer-case-studies.md. Core pitch time: 11 minutes 30 seconds, plus short buyer exchanges."),
]
(R/'slides.js').write_text('window.PITCH_BRAND = '+json.dumps((R/'assets/planetscale-white.svg').read_text())+';\nwindow.PITCH_SLIDES = '+json.dumps(slides,ensure_ascii=False,indent=2)+';\n')
(R/'qa/content.json').write_text(json.dumps([{'id':s['id'],'label':s['label']} for s in slides],indent=2))
(R/'qa/links.json').write_text('{}\n')
(R/'speaker-notes.md').write_text('# PlanetScale Postgres — speaker notes\n\nSeven slides · General Postgres prospect · 10–15 minutes\n\n'+'\n\n'.join(f'## {i}. {s["label"]}\n\n{s["notes"]}' for i,s in enumerate(slides,1))+'\n')
print('Built seven slides, vector diagrams and speaker notes.')
