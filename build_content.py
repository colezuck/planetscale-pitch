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

# Opening: product portfolio and operating foundation, not a node topology.
b=db(1,8,790,288,WHITE)
b+='<image href="assets/postgresql.svg" x="39" y="58" width="69" height="72"/>'
b+=txt(140,112,'Postgres',49,WHITE,weight=500,mono=False)
b+=txt(140,157,'Fully managed',24,GRAY)
b+=rect(20,200,752,77,INK,ORANGE)
b+=rect(26,206,740,65,'url(#metal-hero-accent)','none')
b+=rect(42,217,147,42,INK,'none')+txt(58,248,'Metal',32,ORANGE)
b+=rect(497,222,253,35,INK,'none')+txt(731,247,'Local NVMe storage',22,ORANGE,'end')
b+=path('M791 151H893','#777777',1.5,True)
b+=rect(910,44,339,217,INK,'#77632b')
b+=rect(934,68,48,68,YELLOW,'none')
b+='<image href="assets/neki-cat.svg" x="940" y="72" width="38" height="58"/>'
b+=txt(1000,117,'[ NEKI ]',31,YELLOW)
b+=txt(940,176,'Sharded Postgres',26,WHITE)
b+=txt(940,219,'Horizontal scale',21,GRAY)
b+=path('M396 297V350H1080V262','#777777',1.5)
b+=path('M738 350V380','#777777',1.5)
b+=rect(1,381,1248,109,INK,'#777777')
b+=txt(27,423,'PlanetScale platform',28,WHITE,weight=500,mono=False)
b+=txt(27,463,'Provisioning / Observability / Backups',21,GRAY)
b+=path('M840 400V472','#555555',1)
b+=txt(876,423,'Infrastructure team',28,WHITE,weight=500,mono=False)
b+=txt(876,463,'Migration + operations',21,GRAY)
servers=svg(1250,494,b,'PlanetScale product overview: fully managed Postgres on Metal with local NVMe storage, alongside Neki for sharded Postgres and horizontal scale. The PlanetScale platform and infrastructure team support the database products. This is a product map, not a query path or migration flow.',mark='metal-hero')

# HA: full-height architecture makes the query paths and control plane the focus.
b=stipple_box(470,0,310,52,'Application','ha-arrow-dots',WHITE,25)
b+=path('M560 53V78H175V108',ORANGE,2,True,arrow='ha-arrow')+txt(213,101,'Writes + fresh reads',20,ORANGE)
b+=path('M690 53V78H888V108',BLUE,2,True,arrow='ha-arrow')+txt(915,101,'Replica reads',20,BLUE)
b+=rect(25,113,300,52,stroke=ORANGE)+txt(175,147,'Primary connection',23,anchor='middle')
b+=rect(730,113,315,52,stroke=BLUE)+txt(888,147,'Replica connection',23,anchor='middle')
b+=path('M175 166V272',ORANGE,2,True,arrow='ha-arrow')
b+=path('M888 166V193H625V272',BLUE,2,True,arrow='ha-arrow')+path('M888 193H1075V272',BLUE,2,True,arrow='ha-arrow')
for x,label,role,color in [(0,'Availability zone A','Primary',ORANGE),(450,'Availability zone B','Replica',BLUE),(900,'Availability zone C','Replica',BLUE)]:
    b+=rect(x,228,350,177,'none','#555555')+rect(x+12,234,270,24,INK,'none')+txt(x+18,253,label,20,GRAY)
    b+=(db(x+79,280,192,100,color) if role=='Primary' else rect(x+79,280,192,100,INK,color))+txt(x+175,324,role,29,anchor='middle')+txt(x+175,356,'node',21,GRAY,'middle')
b+=path('M272 330H524',GRAY,1.8,True,arrow='ha-arrow')+txt(398,311,'Replication',19,GRAY,'middle')
b+=path('M175 382V429H1075V383',GRAY,1.8,True,arrow='ha-arrow')+txt(628,456,'Semi-synchronous replication',20,GRAY,'middle')
b+=rect(0,484,1250,65,INK,'#aaaaaa')
b+='<svg x="24" y="500" width="33" height="33" viewBox="0 0 454 454" aria-label="PlanetScale"><g fill="#fff"><path d="m0 227c.00001067-125.369 101.631-227.00001067 227-227 92.178.00000806 171.524 54.9423 207.076 133.865l-300.211 300.211c-12.882-5.803-25.126-12.774-36.5966-20.776l186.2996-186.3h-56.568l-160.5132 160.513c-41.0789-41.079-66.48680548-97.829-66.4868-160.513z"/><path d="m454 227.078-226.922 226.922c125.307-.042 226.88-101.615 226.922-226.922z"/></g></svg>'
b+=txt(76,525,'Control plane',27,WHITE,weight=500)
b+=txt(419,525,'Provision',23,GRAY)+txt(674,525,'Fail over',23,GRAY)+txt(884,525,'Resize',23,GRAY)+txt(1060,525,'Upgrade',23,GRAY)
for x in (27,1223):b+=path(f'M{x} 484V406','#777777',1.5,True)
ha=svg(1250,553,b,'One highly available Postgres cluster in a single region, containing three database nodes. Each availability zone contains one node: a primary in zone A and replicas in zones B and C. Application connections select the primary or replicas. Semi-synchronous replication connects the nodes. The separate control plane manages provisioning, failover, resizing, and upgrades.',mark='ha-arrow')

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

# Display the original customer charts without rebuilding or modifying their pixels.
# CSS viewports show the two panels from the unchanged source screenshot.
convex_plot = '''<div class="convex-original-grid"><div><div class="source-provider-row"><span>AWS Aurora</span><span>PlanetScale Postgres</span></div><div class="convex-source-frame"><img src="assets/convex-original-results.png" alt="Original Convex index query latency chart. All five percentile curves, original axes and legend are preserved; values are in seconds."></div><div class="convex-result"><span>Query p99</span><div>10–15 ms <i>→</i> <strong>5–7 ms</strong></div></div></div><div><div class="source-provider-row"><span>AWS Aurora</span><span>PlanetScale Postgres</span></div><div class="convex-source-frame commit-source"><img src="assets/convex-original-results.png" alt="Original Convex database commit latency chart. All five percentile curves, original axes and legend are preserved; values are in seconds."></div><div class="convex-result"><span>Batch-commit p99</span><div>75–200 ms <i>→</i> <strong>~20 ms</strong></div></div></div></div>'''

# Autumn reports approximate latency, not a percentile or a sampled time series.
b=txt(0,27,'Query latency',25,WHITE)
b+=txt(0,107,'Previous provider',21,WHITE)+txt(880,107,'~100 ms',40,WHITE,'end')
b+=rect(0,131,880,86,'url(#autumn-latency-dots)',WHITE)
b+=txt(0,287,'PlanetScale Metal',21,ORANGE)+txt(880,287,'<10 ms',48,ORANGE,'end')
b+=rect(0,311,88,86,'url(#autumn-latency-accent)','none')
b+=path('M0 311H88V397H0Z',ORANGE,1.5,True)
b+=path('M0 431H880','#555555',1)
for v in [0,25,50,75,100]:
    x=v/100*880
    b+=path(f'M{x} 431V437','#777777',1)+txt(x,465,str(v),17,GRAY,'middle')
b+=txt(880,500,'milliseconds',17,GRAY,'end')
autumn_plot=svg(905,510,b,'Autumn query latency: approximately 100 milliseconds at an unnamed previous provider, consistently below 10 milliseconds on PlanetScale Metal. Dashed orange bar shows the 10 millisecond upper bound, not an exact measured value.',mark='autumn-latency')

slides=[
 dict(id='opening',label='PlanetScale Postgres on Metal',theme='opening',html=f'''<h1>Postgres on <span class="accent">Metal</span></h1><div class="opening-architecture">{servers}</div>''',notes="1:15. “PlanetScale brings together the database, the hardware, and the team operating it. For your workload, we are proposing fully managed Postgres on Metal, with local NVMe storage. Our platform handles database operations, and our infrastructure team works with you on migration and production.” Point to Neki briefly: “For workloads that eventually outgrow one machine, Neki is our sharded Postgres product.” This is a product overview, not a query path or an automatic upgrade flow. Do not describe replica topology or control-plane internals here; slide 3 covers the architecture. Neki is in Platform Preview and requires a separate compatibility and migration assessment. The immediate offer remains hosted Postgres on Metal. Ask: “Where is your team spending the most time with Postgres today?” Transition: “Vitalize is one Postgres team that made this move.” Sources: https://planetscale.com/metal ; https://planetscale.com/docs/neki ; https://planetscale.com/blog/benchmarking-postgres."),
 dict(id='vitalize',label='Vitalize: 2 ms p95, half the vCPUs',theme='vitalize',html=f'''<h2>Vitalize: <span class="accent">2 ms p95</span></h2><div class="customer-story"><span>Hospital staffing software</span><span>400 GB / 150 million rows</span></div><div class="customer-move"><span>Supabase</span><span class="move-line"></span><strong>PlanetScale Metal</strong></div><div class="vitalize-charts"><div>{vitalize_latency}</div><div>{vitalize_compute}</div></div>''',notes='1:45. “Vitalize runs hospital staffing software. They moved a 400 GB Postgres database with 150 million rows from Supabase to PlanetScale Metal. They report about 2 ms p95 on half the vCPUs, with the same 16 GB of RAM.” Tell the customer story before explaining the graphs: demanding database reads, the move, then the result. The latency plot is their actual PlanetScale Query Insights capture after migration, not a paired before/after percentile. No comparable Supabase p95 is published. The 200 GB JSONB-heavy table comparison separately reports 50-second average reads before and 1.2-second maximum reads after; do not calculate a speedup from unlike statistics. The cutover included taking the app offline. These are customer-reported outcomes, not a guarantee. Transition: “Here is the platform operating that database.” Source: https://vitalize.care/blog/from-supabase-to-planetscale . Other cases and suitable alternatives: docs/customer-case-studies.md.'),
 dict(id='availability',label='Postgres Cluster Architecture',theme='availability',html=f'''<div class="title-with-stat"><h2>Postgres Cluster Architecture</h2><div class="sla"><strong>99.99<span>%</span></strong><p>single-region HA SLA</p></div></div><div class="ha-diagram">{ha}</div>''',notes="2:00. “This is one highly available Postgres cluster: three database nodes, each in a different availability zone within the same region. One node is primary; the other two are replicas.” A node (also called an instance in PlanetScale documentation) is an individual database server. An availability zone is the cloud location and failure boundary hosting that node. The whole deployment is a cluster, not one node. A, B, and C are schematic zone labels, not literal provider zone IDs. This depicts the standard three-node HA configuration; additional replicas are possible. Trace application connections, then replication, then operations. The two connection boxes are logical routing choices, not a claim of separate DNS endpoints. Replica reads are explicitly selected with a replica credential/username suffix on direct port 5432; reads must tolerate replication lag. Default PgBouncer connections on 6432 route to the primary; dedicated replica PgBouncers are a separate option. Semi-synchronous replication requires durable confirmation from at least one replica before commit success is returned. PlanetScale's custom Kubernetes operator manages the cluster's provisioning, health, failover, resizing, and upgrades; it is outside the SQL query path. Failovers can interrupt connections, so applications need retries. The 99.99% figure is the single-region monthly uptime commitment under the applicable SLA; it excludes single-node clusters and beta features. Hosted Postgres on Metal remains the offer. Transition: “Local NVMe is the hardware foundation. Let's look at its performance under load.” Verified 2026-09-27. Sources: https://planetscale.com/docs/postgres/postgres-architecture ; https://planetscale.com/docs/postgres/operations-philosophy ; https://planetscale.com/docs/postgres/scaling/replicas ; https://planetscale.com/legal/planetscale-service-level-agreement . Durable terminology: docs/postgres-architecture.md."),
 dict(id='metal',label='Postgres on Metal: throughput and p99',theme='metal',html=f'''<div class="metal-heading"><h2>More throughput. Lower p99</h2><p class="metal-line">Postgres on Metal</p></div><div class="benchmark-grid"><div><h3>Throughput <span>mean queries / second</span></h3>{bars}</div><div><h3>p99 latency <span>milliseconds / 1-second intervals</span></h3><div class="chart-legend"><span class="ps-dot">PlanetScale</span><span class="aurora-dot">Aurora</span></div>{latency}</div></div><p class="workload">TPCC-like / 500 GB / 32 connections / 5-minute run</p>''',notes="1:45. “In this mixed read/write benchmark, Postgres on Metal delivers more throughput and lower p99 than these tested configurations. We can evaluate the same questions against your application.” Left: arithmetic mean QPS across 300 one-second samples with 32 concurrent connections: PlanetScale 16,338.6276; Aurora 10,908.9315; AlloyDB 10,355.0109; Supabase 5,270.2068. Right: one-second interval p99 samples from the same TPCC-like benchmark, not an aggregate run-wide percentile. PlanetScale ranges 170.48–223.34 ms; Aurora 325.98–733 ms. Higher QPS and lower p99 are distinct findings. PlanetScale M-320 has 4 vCPU, 32 GB RAM, and 937 GB local NVMe; Aurora and AlloyDB use 4 vCPU/32 GB; Supabase uses 8 vCPU/32 GB and 12k IOPS. Clients run in each provider's cloud region; AlloyDB uses GCP, the others AWS. Work is sent to the primary, not summed across replicas. These are vendor-run synthetic results with different hardware and infrastructure, not isolated proof that NVMe causes every difference. The site's rounded ~18k headline spans other runs; this deck deliberately uses a single concurrency and exact samples. A separate read-only test has roughly equal average throughput for Aurora and PlanetScale, so do not claim every workload is faster by this ratio. Ask: “Which workload would we need to reproduce for this to matter to you?” Validate p95/p99, throughput, errors, and resource use in discovery. Transition: “When one machine becomes the constraint, Neki extends the architecture across Postgres shards.” Sources: https://planetscale.com/benchmarks ; https://planetscale.com/benchmarks/aurora ; https://planetscale.com/benchmarks/alloydb ; https://planetscale.com/benchmarks/supabase . Data definitions: docs/postgres-metal-benchmarks.md."),
 dict(id='neki',label='Neki: Horizontal Scaling for Postgres',theme='neki',html=f'''<div class="neki-heading"><h2>Neki: Horizontal Scaling for Postgres</h2><div class="neki-lockup"><img src="assets/neki-cat.svg" alt="Neki"></div></div><div class="neki-topology">{neki}</div>''',notes="1:15. “Neki is our sharded Postgres architecture. Every shard is real Postgres, with routing and operations managed as one database.” Walk from the application to the router, then one shard group, then the control plane. Sidecars pool connections; shard primaries and replicas carry data. The diagram represents replicated HA shard groups, not the primary-only benchmark on the next slide. Say that Neki is available in Platform Preview as of the verified documentation on 27 September 2026; it is not covered by an SLA. The public site's “now available” wording does not mean general availability. Cross-shard transactions remain listed as coming soon. Evaluate shard keys, query/transaction compatibility and the transition from the current database with the team. Do not imply an automatic in-place conversion from ordinary PlanetScale Postgres. The immediate sale remains hosted Postgres on Metal. Transition: “The benchmark demonstrates how far this architecture can scale for a defined workload.” Sources: https://neki.dev/ ; https://planetscale.com/docs/neki ; https://planetscale.com/blog/the-architecture-of-neki ."),
 dict(id='neki-scale',label='Neki: 118.5M queries per second',theme='neki neki-scale',html=f'''<div class="neki-heading"><h2><span class="yellow">118.5M</span> queries / second</h2><span class="neki-wordmark">[ NEKI ]</span></div><div class="scale-layout"><div><div class="scale-chart">{scale}</div><p class="neki-workload">Read-only point selects / Primary-only shards</p></div><div class="scale-metrics"><div><strong>1.22 <span>PiB</span></strong><p>data</p></div><div><strong>512</strong><p>shards</p></div><div><strong>6.06 <span>ms</span></strong><p>router p99</p></div></div></div>''',notes="1:00. “The published Neki run sustained 118.5 million queries per second across 512 shards over a 1.22 PiB dataset.” Follow the 5-, 50-, and 512-shard series and stop. Exact QPS: 999,624; 9,923,900; 118,538,803. Both axes are logarithmic. Workload: read-only, one-row primary-key point selects sent to a single shard. The measured configuration had 512 primary-only shards and 480 routers, without replicas or a failover event, for 16 minutes. It does not establish write performance or HA behavior. The 6.06 ms p99 is at the router; client p99 was 13.95 ms. These metrics do not share the TPCC workload or Vitalize workload and should not be compared on a common chart. Transition: “For your team, the next step is assessing today's Postgres workload and planning the migration.” Source: https://planetscale.com/blog/118-million-queries-per-second-on-neki ."),
 dict(id='migration',label='Your migration with our infrastructure team',theme='migration',html=f'''<h2>Migrate with our infrastructure team</h2><div class="migration-diagram">{migration}</div><div class="migration-steps"><div><span>01</span><strong>Assess</strong><p>Schema, extensions, workload</p></div><div><span>02</span><strong>Rehearse</strong><p>Replication, p95 / p99, recovery</p></div><div><span>03</span><strong>Cut over</strong><p>Validate, switch, monitor</p></div></div><div class="migration-close"><strong>Technical discovery + migration assessment</strong><span>Your team + our database engineers</span></div>''',notes="2:30. “We start with your existing Postgres, assess the dependencies, and rehearse the move with your team.” The source serves traffic during the initial copy and change replication. Validate data and critical queries before agreeing on a cutover. Assess schemas, extensions, write rate, permissions, auth dependencies, connection patterns, recovery requirements, and networking. Compare a representative workload's p95/p99 and throughput. The final synchronization, application connection switch, downtime, and rollback strategy depend on source configuration and any target-side writes. This is a workflow, not a claim that all providers support the same automated importer or universal zero downtime. Close: “Can we schedule a technical discovery with your database and infrastructure leads to scope the migration assessment?” Establish compatibility questions, target deployment, success criteria, and the work needed for a migration plan. If relevant, Autumn reports a two-day migration with seconds of cutover downtime and direct help from PlanetScale; that is an example, not a delivery promise. Source: https://useautumn.com/blog/migrating-to-planetscale ; other references in docs/customer-case-studies.md. Core pitch time: 11 minutes 30 seconds, plus short buyer exchanges."),
 dict(id='convex',label='Convex migrated from Aurora to PlanetScale Postgres Metal',theme='customer-case convex',html=f'''<div class="case-heading convex-heading"><img class="convex-title-symbol" src="assets/convex-symbol-color.svg" alt=""><h2>Convex migrated from Aurora to PlanetScale Postgres Metal</h2></div><div class="convex-curves">{convex_plot}</div><div class="convex-quote"><q>p50 is the new p99.</q><span>Jamie Turner / Convex</span></div>''',notes="1:15. Convex provides backend infrastructure for developers. Its Chef product stores message histories and project snapshots in a Convex backend. The team moved that workload from AWS Aurora to PlanetScale for Postgres. Query p99 moved from a noisy 10–15 ms to a steadier 5–7 ms; batch-commit p99 had spiked between 75 and 200 ms and subsequently stayed around 20 ms. Both panels display the unchanged original customer screenshot, cropped only at the panel boundary through CSS. A CSS invert/hue-rotation filter adapts its light background to dark mode. All percentile lines, original axis values, and legends are preserved. The source chart vertical axes are in seconds; the numeric p99 summaries below are in milliseconds and use the article’s explicit reported ranges. The original query chart clips peaks above 0.02 seconds. Provider labels indicate the before/after portions around the visible step near 23:55, not a separately verified cutover timestamp. Each chart has its own vertical scale. The closing quote, “p50 is the new p99,” is Jamie Turner’s wording in the customer post. Treat it as a qualitative summary of the improvement, not a claim that every old p50 exactly equals every new p99. Preserve the approximate qualifier on 20 ms. Do not imply that all Convex workloads achieved these results, identify the prior Aurora engine without evidence, or claim a controlled hardware comparison. The article discusses Metal as the motivation but does not specify the measured cluster tier; label the destination PlanetScale for Postgres. Gong structure: infrastructure buyer's need, one named production workload, the change, and the measured outcome. Ask which tail-latency path matters most to the prospect. Source: https://news.convex.dev/powered-by-planetscale-for-postgres/ . This candidate slide is appended for review; the original Vitalize slide remains."),
 dict(id='autumn',label='Autumn: two days to PlanetScale Metal',theme='customer-case autumn',html=f'''<div class="case-heading"><h2>Two days to PlanetScale Metal</h2><img class="autumn-logo" src="assets/autumn.svg" alt="Autumn"></div><p class="case-context">Billing infrastructure / real-time access + credit checks</p><div class="autumn-evidence"><div>{autumn_plot}</div><div class="autumn-migration"><div class="migration-number"><strong>2<span> days</span></strong><p>Migration</p></div><div class="cutover-number"><strong>Seconds</strong><p>Cutover downtime</p></div><div class="migration-assist"><span class="assist-node"></span><p>PlanetScale<br>migration team</p></div></div></div>''',notes="1:15. Autumn provides billing infrastructure for AI companies, including real-time access and credit checks in the request path. Its previous provider had connection-pooling issues and inconsistent latency. The team expected migration to take weeks; it reports completing it in two days with seconds of cutover downtime. PlanetScale's team helped with replication and recommended its pgcopydb fork. General query latency moved from approximately 100 ms to consistently below 10 ms after the move to PlanetScale Metal. These values have no published percentile; do not call them p95 or p99. The previous provider is unnamed. A separate later support engagement involved query/index changes and a p99 improvement from around 200 ms to under 50 ms; that separate optimization is intentionally excluded from this slide. The white bar uses the approximate 100 ms baseline; the dashed orange bar depicts an upper bound of 10 ms, not a measured 10 ms value. Autumn’s original Insights screenshot is a later post-migration view, so it is not presented as the migration before/after comparison. The official current Autumn logo is monochrome; no invented color version is used. Timings are Autumn's experience, not a migration promise. Gong structure: business-critical workload, concerns about switching, assisted migration, observed result. Transition to technical discovery and migration assessment: assess the prospect's dependencies, workload, and cutover needs. Source: https://useautumn.com/blog/migrating-to-planetscale . This candidate slide is appended for review; the existing migration closing slide remains."),
]
(R/'slides.js').write_text('window.PITCH_BRAND = '+json.dumps((R/'assets/planetscale-white.svg').read_text())+';\nwindow.PITCH_SLIDES = '+json.dumps(slides,ensure_ascii=False,indent=2)+';\n')
(R/'qa/content.json').write_text(json.dumps([{'id':s['id'],'label':s['label']} for s in slides],indent=2))
(R/'qa/links.json').write_text('{}\n')
(R/'speaker-notes.md').write_text('# PlanetScale Postgres — speaker notes\n\nNine-slide working deck · General Postgres prospect · Final selection pending\n\n'+'\n\n'.join(f'## {i}. {s["label"]}\n\n{s["notes"]}' for i,s in enumerate(slides,1))+'\n')
print(f'Built {len(slides)} slides, vector diagrams and speaker notes.')
