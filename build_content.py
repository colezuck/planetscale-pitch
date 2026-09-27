"""Editable deck content and vector diagrams. Run to rebuild slides.js and notes."""
from pathlib import Path
import json, html
R=Path(__file__).resolve().parent
INK='#111111'; PANEL='#111111'; LINE='#dadada'; WHITE='#fafafa'; GRAY='#a5a5a5'; ORANGE='#f35815'; BLUE='#dadada'; YELLOW='#fbca00'
def txt(x,y,s,size=24,color=WHITE,anchor='start',weight=400,mono=True):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" font-family="{("ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" if mono else "Inter,Arial,sans-serif")}">{html.escape(s)}</text>'
def rect(x,y,w,h,fill=PANEL,stroke=LINE,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" rx="{rx}"/>'
def path(d,color=LINE,width=2,dash=False,arrow=None):return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{(" stroke-dasharray=\"11 9\"" if dash else "")}{(" marker-end=\"url(#"+arrow+")\"" if arrow else "")}/>'
def svg(w,h,body,label,mark='arr',color=WHITE):
    patterns=''.join(f'<pattern id="{mark}-{key}" width="7" height="7" patternUnits="userSpaceOnUse"><rect x="1" y="1" width="1.3" height="2.4" fill="{c}"/><rect x="4.5" y="4.5" width="1.3" height="2.4" fill="{c}"/></pattern>' for key,c in [('dots',WHITE),('accent',ORANGE),('yellow',YELLOW)])
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(label)}"><defs>{patterns}<marker id="{mark}" markerWidth="7" markerHeight="7" refX="6.5" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7Z" fill="{color}"/></marker></defs>{body}</svg>'
def db(x,y,w=170,h=94,color=LINE):
    return rect(x,y,w,h,INK,color)+rect(x+4,y+4,w-8,h-8,'none',color)
def stipple_box(x,y,w,h,label,mark,color=WHITE,size=24):
    return rect(x,y,w,h,INK,color)+rect(x+6,y+6,w-12,h-12,f'url(#{mark})','none')+rect(x+w/2-len(label)*size*.33-12,y+h/2-19,len(label)*size*.66+24,38,INK,'none')+txt(x+w/2,y+h/2+size*.34,label,size,color,'middle')

# Opening: a vector server stack, with the original PostgreSQL elephant.
b=''
for i in range(3):
    y=130+i*85
    b+=f'<path d="M42 {y}L133 {y-48}H417L326 {y}Z" fill="#111111" stroke="#bcbcbc"/>'
    b+=rect(42,y,284,65,'#111111','#bcbcbc')
    b+=f'<path d="M326 {y}L417 {y-48}V{y+17}L326 {y+65}Z" fill="#111111" stroke="#bcbcbc"/>'
    b+=path(f'M68 {y+25}H170M68 {y+37}H170','#777',2)
    for j in range(3):b+=f'<circle cx="{264+j*16}" cy="{y+31}" r="3" fill="{ORANGE}"/>'
b+='<image href="assets/postgresql.svg" x="187" y="0" width="151" height="155"/>'
servers=svg(480,410,b,'PostgreSQL on a stack of dedicated servers')

# HA: solid application paths; separate dashed management paths.
b=stipple_box(455,0,340,60,'Application','ha-arrow-dots',WHITE,24)
b+=path('M560 60V88H175V137',ORANGE,2,True,arrow='ha-arrow')+txt(220,111,'Writes + fresh reads',21,ORANGE)
b+=path('M690 60V88H888V137',BLUE,2,True,arrow='ha-arrow')+txt(905,111,'Replica reads',21,BLUE)
b+=rect(25,138,300,54,stroke=ORANGE)+txt(175,172,'Primary endpoint',22,anchor='middle')
b+=rect(730,138,315,54,stroke=BLUE)+txt(888,172,'Replica endpoint',22,anchor='middle')
b+=path('M175 192V258',ORANGE,2,True,arrow='ha-arrow')
b+=path('M888 192V216H625V258',BLUE,2,True,arrow='ha-arrow')+path('M888 216H1075V258',BLUE,2,True,arrow='ha-arrow')
for x,label,role,color in [(0,'ZONE A','Primary',ORANGE),(450,'ZONE B','Replica',BLUE),(900,'ZONE C','Replica',BLUE)]:
    b+=rect(x,238,350,166,'none','#3b3b3b')+txt(x+18,265,label,15,GRAY,mono=True)
    b+=(db(x+79,279,192,85,color) if role=='Primary' else rect(x+79,279,192,85,INK,color))+txt(x+175,330,role,25,anchor='middle')
b+=path('M272 320H524',GRAY,1.7,True,arrow='ha-arrow')+txt(398,304,'Replication',16,GRAY,'middle')
b+=path('M180 375V426H1075V375',GRAY,1.7,True,arrow='ha-arrow')+txt(628,451,'Semi-synchronous replication',18,GRAY,'middle')
b+=rect(0,479,1250,64,INK,'#9b9b9b')+txt(28,520,'Control plane',24,WHITE,weight=500)
b+=txt(420,520,'Provision',21,GRAY)+txt(679,520,'Fail over',21,GRAY)+txt(875,520,'Resize',21,GRAY)+txt(1065,520,'Upgrade',21,GRAY)
for x in (27,1223):b+=path(f'M{x} 479V404','#686868',1.5,True)
ha=svg(1250,547,b,'Application routes writes and fresh reads to a primary in zone A, replica reads to replicas in zones B and C. Semi-synchronous replication connects the nodes. A separate control plane provisions, fails over, resizes and upgrades them.',mark='ha-arrow')

# Throughput bars and real one-second p99 samples, kept as native vector charts.
providers=[('PlanetScale',16338.6,ORANGE),('Aurora',10908.9,'#8b8b8b'),('AlloyDB',10355.0,'#707070'),('Supabase',5270.2,'#555555')]
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
b=txt(0,24,'Compute / vCPU',23,WHITE)
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
 dict(id='opening',label='Your Postgres. Our infrastructure.',theme='opening',html=f'''<div class="hero"><div><h1>Your Postgres.<br>Our infrastructure.</h1><p class="lead">Postgres on Metal.<br>Operated by PlanetScale.</p></div><div class="server-art">{servers}</div></div><div class="cash-proof"><div class="customer"><img src="assets/cash-app.svg" alt="Cash App"><span>Vitess / MySQL</span></div><div><strong>~400 TiB</strong><span>data</span></div><div><strong>~400</strong><span>shards</span></div><div><strong>3–4M</strong><span>peak queries / second</span></div></div>''',notes='1:30. Open as the PlanetScale representative: “We operate the database infrastructure so your engineers can build the product. We will show you what that looks like for the Postgres you already use, how we move it, and where we can take it as you grow.” Cash App is proof of the team’s operational experience: roughly 400 TiB, 400 shards and 3–4 million peak queries per second. Be explicit that Cash App’s published case is Vitess/MySQL, not PlanetScale Postgres or Neki. Ask which constraint matters most today: latency, reliability, operating effort or growth. This is a general-prospect pitch; do not assert a discovered pain that the buyer has not confirmed.'),
 dict(id='availability',label='Postgres availability and control plane',theme='availability',html=f'''<div class="title-with-stat"><h2>Available across<br>three zones.</h2><div class="sla"><strong>99.99<span>%</span></strong><p>single-region HA SLA</p></div></div><div class="ha-diagram">{ha}</div>''',notes='2:00. Follow the solid paths first. The application uses the primary endpoint for writes and reads that need the freshest data; the replica endpoint is for reads that can tolerate lag. Connection pooling sits in the data path. A production HA cluster has one primary and two replicas in three availability zones, with semi-synchronous streaming replication acknowledged by at least one replica. The control plane is outside the SQL traffic path. Our operator provisions the cluster, monitors health, replaces failed nodes and orchestrates failover, resizing and upgrades. Automatic failover can briefly interrupt connections: applications need sensible retries. Backups and point-in-time recovery complement HA. The diagram is simplified, not a physical networking map. 99.99% is the published monthly single-region SLA when included in the applicable agreement; single-node and beta offerings are excluded. Do not promise zero interruption, zero loss in every failure mode, or automatic CPU autoscaling.'),
 dict(id='metal',label='Metal throughput and p99',theme='metal',html=f'''<h2>More throughput.<br>Lower tail latency.</h2><p class="metal-line">Postgres + local NVMe</p><div class="benchmark-grid"><div><h3>Throughput <span>queries / second</span></h3>{bars}</div><div><h3>p99 latency <span>milliseconds</span></h3><div class="chart-legend"><span class="ps-dot">PlanetScale</span><span class="aurora-dot">Aurora</span></div>{latency}</div></div><p class="workload">TPCC-like · 500 GB · 32 connections · 5-minute run</p>''',notes='2:00. Metal places Postgres data on local NVMe, reducing dependence on network-attached storage for the database I/O path. In PlanetScale’s published TPCC-like benchmark, the chart on the left uses the average of the 300 one-second throughput samples at 32 connections for all four providers. Exact means: PlanetScale 16,338.6; Aurora 10,908.9; AlloyDB 10,355.0; Supabase 5,270.2 QPS. The right chart plots each one-second interval’s p99, not an average mislabeled as a run-wide p99. PlanetScale’s 32-connection series ranges 170.48–223.34 ms; Aurora’s ranges 325.98–733 ms. These are vendor-run synthetic results, not a guarantee for the prospect’s workload. PlanetScale M320 used 4 vCPU / 32 GB RAM / 937 GB local NVMe; Aurora db.r8g.xlarge 4 vCPU / 32 GB; AlloyDB 4 vCPU / 32 GB; Supabase 8 vCPU / 32 GB. Benchmark clients were in the same cloud region as the respective database, with AWS us-east-1 and GCP us-central1. These are not identical CPU configurations. Explain that we will validate p95, p99, throughput, errors and compute under the prospect’s representative workload during the technical evaluation.'),
 dict(id='vitalize',label='Vitalize Postgres migration',theme='vitalize',html=f'''<h2>Vitalize: <span class="accent">2 ms p95.</span><br>Half the vCPUs.</h2><p class="customer-context">400 GB · 150 million rows · Hospital staffing software</p><div class="vitalize-charts"><div>{vitalize_latency}</div><div>{vitalize_compute}</div></div>''',notes='1:30. Vitalize migrated 400 GB and 150 million rows from Supabase to PlanetScale Metal. The graph is PlanetScale after migration: their actual 24-hour Query Insights plot, with unchanged curves and larger labels. The article reports about 2 ms p95; the screenshot shows an instantaneous 2.2 ms. No comparable pre-migration Supabase p95 is published. Separately, reads on their 200 GB table with heavy JSONB averaged 50 seconds on Supabase and maxed out at 1.2 seconds on PlanetScale. Average and maximum are different statistics: state both labels and do not claim a calculated speedup. Compute fell from 4 to 2 vCPUs with 16 GB RAM on both. These are customer-reported results. Cutover included taking the app offline; do not promise literal zero downtime. Ask which workload and migration dependencies the prospect needs assessed.'),
 dict(id='migration',label='Migration with the PlanetScale team',theme='migration',html=f'''<h2>Your migration.<br>Our team alongside yours.</h2><div class="migration-diagram">{migration}</div><div class="migration-steps"><div><span>01</span><strong>Assess</strong><p>Schema, extensions, workload</p></div><div><span>02</span><strong>Rehearse</strong><p>Replication, p95 / p99, recovery</p></div><div><span>03</span><strong>Cut over</strong><p>Validation, connection, rollback plan</p></div></div>''',notes='2:00. This is the engagement to sell: technical discovery plus a migration assessment with our team. First inventory size, write rate, extensions, permissions, auth dependencies, connections and availability requirements. Run the discovery tooling and identify incompatibilities before promising dates. The source continues serving during initial copy and change replication. Rehearse the final synchronization and application connection change, validate counts and critical workflows, compare p95 / p99 and errors, and agree on a rollback plan appropriate to the cutover and any target-side writes. The drawing is a migration workflow, not a claim that every source supports the same automated import mechanism. Exact tooling, downtime and rollback strategy depend on the source configuration and workload. The next meeting should include whoever owns the database, infrastructure and application deployment. Deliverables: compatibility findings, target cluster, success criteria and a proposed migration path. Do not promise a fixed migration duration or universal zero downtime.'),
 dict(id='neki',label='Neki architecture',theme='neki',html=f'''<div class="neki-heading"><h2>Sharded Postgres.</h2><div class="neki-lockup"><img src="assets/neki-cat.svg" alt="Neki cat"><span class="neki-wordmark">[ NEKI ]</span></div></div><div class="neki-topology">{neki}</div>''',notes='2:00. When a single Postgres machine becomes the constraint, Neki provides our sharded Postgres architecture. Every shard runs real PostgreSQL. The application speaks the Postgres wire protocol to the router; the router uses shard configuration to send work to the right shards and assemble results. Each shard has a sidecar for pooling and operational control. The control plane manages topology, health and workflows such as online resharding. Normal HA deployments place a primary and replicas across availability zones; the diagram shows a primary and two replicas per shard. Sidecars and PostgresManager exist on each instance; only the primary sidecar label is repeated for readability. Start with shard-key choice and tenant access patterns. Discuss query compatibility and cross-shard work rather than claiming every query is transparently equivalent to single-node PostgreSQL. At the time of this research Neki is in platform preview, intended for evaluation with non-production data; breaking changes are possible. Say that verbally when introducing it. Cross-shard transactions are listed as coming soon. Do not promise a seamless in-place conversion of any existing PlanetScale Postgres database. This is the forward-looking scale discussion, not a requirement to shard on day one.'),
 dict(id='neki-scale',label='Neki demonstrated scale and next step',theme='neki neki-scale',html=f'''<div class="neki-heading"><h2><span class="yellow">118.5M</span> queries / second.</h2><span class="neki-wordmark">[ NEKI ]</span></div><div class="scale-layout"><div><div class="scale-chart">{scale}</div><p class="neki-workload">Read-only point selects · Primary-only shards</p></div><div class="scale-metrics"><div><strong>1.22 <span>PiB</span></strong><p>data</p></div><div><strong>512</strong><p>shards</p></div><div><strong>6.06 <span>ms</span></strong><p>router p99</p></div></div></div><div class="close-ask"><span>Let’s map your workload.</span><strong>Technical discovery + migration assessment <span>↗</span></strong></div>''',notes='1:30. This is a measured Neki benchmark, not a customer production deployment. The published run sustained 118,538,803 queries per second for 16 minutes across 512 shards and 480 routers, over a 1.22 PiB dataset. The 5-shard run delivered 999,624 QPS; the 50-shard run 9,923,900 QPS. Axes are logarithmic. The displayed 6.06 ms p99 is measured at the router; client p99 was 13.95 ms. Workload: one-row primary-key point selects routed to a single shard, no writes, joins or cross-shard queries. This benchmark used primary-only shards, no replicas and no failover during the measured window. It does not establish write performance, HA failover performance, or the prospect’s production latency. Transition: “We can support the Postgres you need now, and have a concrete architecture for scale beyond one machine. Let’s bring our infrastructure team together with yours for technical discovery and a migration assessment.” Confirm participants, current deployment, dataset size, write rate, latency baseline and a suitable meeting time. Total talk track target: roughly 12–13 minutes plus questions.')
]
(R/'slides.js').write_text('window.PITCH_BRAND = '+json.dumps((R/'assets/planetscale-white.svg').read_text())+';\nwindow.PITCH_SLIDES = '+json.dumps(slides,ensure_ascii=False,indent=2)+';\n')
(R/'qa/content.json').write_text(json.dumps([{'id':s['id'],'label':s['label']} for s in slides],indent=2))
(R/'qa/links.json').write_text('{}\n')
(R/'speaker-notes.md').write_text('# PlanetScale Postgres — speaker notes\n\nSeven slides · General Postgres prospect · 10–15 minutes\n\n'+'\n\n'.join(f'## {i}. {s["label"]}\n\n{s["notes"]}' for i,s in enumerate(slides,1))+'\n')
print('Built seven slides, vector diagrams and speaker notes.')
