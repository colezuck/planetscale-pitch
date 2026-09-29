"""Editable deck content and vector diagrams. Run to rebuild slides.js and notes."""
from pathlib import Path
import json, html, sys
R=Path(__file__).resolve().parent
presenter='--presenter' in sys.argv
speaker_outline=json.loads((R/'private/speaker-outline.json').read_text()) if presenter else {}
class PublicNotes(dict):
    def __missing__(self, key): return ''
speaker_notes=PublicNotes({slide_id: '\n'.join('• '+point for point in points) for slide_id,points in speaker_outline.items()})
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

# HA: full-height architecture makes the query paths and control plane the focus.
b=rect(440,0,370,58)+rect(446,6,38,46,'url(#ha-arrow-dots)','none')+rect(766,6,38,46,'url(#ha-arrow-dots)','none')
b+=txt(625,26,'Application',25,anchor='middle')+txt(625,47,'Selects primary or replica',16,GRAY,'middle')
b+=path('M560 59V83H175V108',ORANGE,2,True,arrow='ha-arrow')+txt(213,106,'Writes + fresh reads',20,ORANGE)
b+=rect(18,113,315,70,stroke=ORANGE)+txt(175,156,'Primary connection',23,anchor='middle')
b+=path('M175 184V278',ORANGE,2,True,arrow='ha-arrow')
b+=path('M690 59V83H888V108',BLUE,2,True,arrow='ha-arrow')+txt(915,106,'Replica reads',20,BLUE)
b+=rect(730,113,315,70,stroke=BLUE)+txt(888,156,'Replica connection',23,anchor='middle')
b+=path('M888 184V209H625V278',BLUE,2,True,arrow='ha-arrow')+path('M888 209H1075V278',BLUE,2,True,arrow='ha-arrow')
for x,label,role,color in [(0,'Availability zone A','Primary',ORANGE),(450,'Availability zone B','Replica',BLUE),(900,'Availability zone C','Replica',BLUE)]:
    b+=rect(x,228,350,177,'none','#555555')+rect(x+12,234,270,24,INK,'none')+txt(x+18,253,label,20,GRAY)
    if role=='Primary':
        b+=db(x+79,280,192,100,color)+txt(x+175,324,'Primary',29,anchor='middle')+txt(x+175,356,'node',21,GRAY,'middle')
    else:
        b+=rect(x+79,280,192,100,INK,color)+txt(x+175,324,role,29,anchor='middle')+txt(x+175,356,'node',21,GRAY,'middle')
b+=path('M271 345H524',GRAY,1.8,True,arrow='ha-arrow')+txt(398,325,'Replication',19,GRAY,'middle')
b+=path('M175 381V429H1075V383',GRAY,1.8,True,arrow='ha-arrow')+txt(628,456,'Semi-synchronous replication',20,GRAY,'middle')
b+=rect(0,484,1250,65,INK,'#aaaaaa')
b+='<svg x="24" y="500" width="33" height="33" viewBox="0 0 454 454" aria-label="PlanetScale"><g fill="#fff"><path d="m0 227c.00001067-125.369 101.631-227.00001067 227-227 92.178.00000806 171.524 54.9423 207.076 133.865l-300.211 300.211c-12.882-5.803-25.126-12.774-36.5966-20.776l186.2996-186.3h-56.568l-160.5132 160.513c-41.0789-41.079-66.48680548-97.829-66.4868-160.513z"/><path d="m454 227.078-226.922 226.922c125.307-.042 226.88-101.615 226.922-226.922z"/></g></svg>'
b+=txt(76,525,'Control plane',27,WHITE,weight=500)
b+=txt(419,525,'Provision',23,GRAY)+txt(674,525,'Fail over',23,GRAY)+txt(884,525,'Resize',23,GRAY)+txt(1060,525,'Upgrade',23,GRAY)
for x in (27,1223):b+=path(f'M{x} 484V406','#777777',1.5,True)
ha=svg(1250,553,b,'One highly available Postgres cluster across three availability zones in one region. The application selects its connection: writes and fresh reads use the primary connection; replica reads use the replica connection. Connection pooling details are omitted. These are application-selected connection paths, not automatic query splitting. Semi-synchronous replication connects the nodes; the separate control plane manages provisioning, failover, resizing, and upgrades.',mark='ha-arrow')

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
for v in [0,400,800,1200]:
    y=438-v/1200*390
    b+=path(f'M62 {y}H575','#3c3c3c',1,True)+txt(48,y+6,f'{v:,} ms',13,GRAY,'end',mono=True)
for t in [0,60,120,180,240,300]:b+=txt(62+t/300*513,468,str(t),16,GRAY,'middle',mono=True)
b+='<defs><clipPath id="p99-plot-clip"><rect x="62" y="48" width="513" height="390"/></clipPath></defs><g clip-path="url(#p99-plot-clip)">'
for name,col in [('Supabase 32conns','#88b8a0'),('AlloyDB 32conns','#91abc7'),('Aurora 32conns','#c4c4c4'),('PlanetScale 32conns',ORANGE)]:
    vals=next(s['values'] for s in series if s['name']==name)
    d=' '.join(('M' if i==0 else 'L')+f'{62+i/(len(vals)-1)*513:.2f} {438-v/1200*390:.2f}' for i,v in enumerate(vals))
    b+=path(d,col,2.2 if name.startswith('PlanetScale') else 1.5)
b+='</g>'
b+=txt(575,499,'seconds',16,GRAY,'end',mono=True)
latency=svg(600,505,b,'One-second benchmark p99 latency samples over 300 seconds, 32 connections. PlanetScale 170.48 to 223.34 ms; Aurora 325.98 to 733 ms; AlloyDB 277.21 to 1235.62 ms; Supabase 196.89 to 1561.52 ms. Linear axis from zero to 1200 milliseconds; values above 1200 are clipped.',mark='p99')

# Vitalize: an editorial comparison, with the statistic attached to each result.
b=txt(0,22,'400 GB migrated',20,GRAY)+txt(210,22,'/ 150 million rows',20,GRAY)
b+=txt(0,104,'Supabase',26,WHITE,mono=False,weight=500)
b+=txt(730,104,'PlanetScale Metal',26,ORANGE,mono=False,weight=500)
# A restrained stipple field extends behind the destination, fading toward the type.
b+='<defs><linearGradient id="vitalize-stipple-fade"><stop offset="0" stop-color="white" stop-opacity="0"/><stop offset="1" stop-color="white" stop-opacity=".3"/></linearGradient><mask id="vitalize-stipple-mask"><rect x="730" y="128" width="520" height="197" fill="url(#vitalize-stipple-fade)"/></mask></defs>'
b+='<g mask="url(#vitalize-stipple-mask)">'+rect(730,128,520,197,'url(#vitalize-art-accent)','none')+'</g>'
b+=txt(-5,257,'50',154,WHITE,weight=500,mono=False)+txt(210,255,'s',66,GRAY,mono=False)
b+=txt(722,257,'1.2',154,ORANGE,weight=500,mono=False)+txt(942,255,'s',66,ORANGE,mono=False)
b+=txt(0,304,'Average read',23,GRAY)+txt(730,304,'Maximum read',23,GRAY)
b+=txt(505,174,'200 GB JSONB-heavy table',16,GRAY,'middle')
b+=path('M385 214H587','#777777',2,arrow='vitalize-art')
# Physical CPU blocks make the resource change legible without another chart.
b+=txt(0,438,'Half the vCPUs utilized',27,WHITE,mono=False,weight=500)
for x in [0,40,80,120]:b+=db(x,460,28,34,'#888888')
b+=path('M174 477H235','#777777',1.5,arrow='vitalize-art')
for x in [258,298]:b+=db(x,460,28,34,ORANGE)
b+=txt(730,476,'2 ms',64,ORANGE,mono=False,weight=500)
b+=txt(900,476,'p95',64,WHITE,mono=False,weight=500)
vitalize_art=svg(1250,550,b,'Vitalize moved 400 GB and 150 million rows from Supabase to PlanetScale Metal. On the same 200 GB JSONB-heavy table, Supabase reads averaged 50 seconds and PlanetScale reads maxed out at 1.2 seconds; these are different statistics, not a matched percentile comparison. Compute changed from four to two vCPUs at 16 GB RAM each. After migration, p95 was about two milliseconds.',mark='vitalize-art')

# Migration close: one destination, with a choice of delivery ownership.
b=db(1,8,380,112,WHITE)
b+='<image href="assets/postgresql.svg" x="27" y="35" width="52" height="54"/>'
b+=txt(103,75,'Your Postgres',29,WHITE)
b+=path('M407 64H707',GRAY,2,True,arrow='m-arrow')
b+=rect(735,8,514,112,INK,ORANGE)
b+=rect(742,15,500,98,'url(#m-arrow-accent)','none')
b+=rect(797,27,390,74,INK,'none')
b+=txt(992,58,'PlanetScale',31,WHITE,'middle')
b+=txt(992,91,'Postgres on Metal',25,ORANGE,'middle')
migration=svg(1250,128,b,'Migrate your existing Postgres database to PlanetScale Postgres on Metal. Both self-service and PlanetScale-led migrations share this destination.',mark='m-arrow')

# Simplified Neki topology, following the official site's shard visual.
b=rect(454,0,342,65,INK,WHITE)+txt(625,42,'Application',26,WHITE,'middle')
b+=path('M625 66V110',WHITE,1.6)
b+=stipple_box(0,110,1250,94,'Neki router','n-arrow-yellow',YELLOW,30)
for i,x in enumerate([0,438,876]):
    b+=path(f'M{x+187} 205V257',YELLOW,1.8)
    b+=rect(x,258,374,228,INK,YELLOW)
    b+=txt(x+38,308,f'SHARD 0{i+1}',20,YELLOW)
    b+=txt(x+38,389,'Postgres',36,WHITE)
    for dx in [38,140,242]:
        b+=rect(x+dx,432,88,14,YELLOW,'none')
neki=svg(1250,510,b,'An application connects to the Neki router, which routes queries to three real Postgres shards. Each shard is shown as a simple Postgres card; internal replication and sidecars are omitted.',mark='n-arrow',color=WHITE)

# A genuine scale series: point-read throughput vs shard count, both logarithmic.
import math
points=[(5,999624,'5 shards','1.0M'),(50,9923900,'50 shards','9.9M'),(512,118538803,'512 shards','118.5M')]
b=''
for i,q in enumerate([1e6,1e7,1e8]):
    y=283-math.log10(q/1e6)*110
    b+=path(f'M60 {y}H758','#494331',1,True)+txt(47,y+5,{1e6:'1M',1e7:'10M',1e8:'100M'}[q],17,'#b9a762','end',mono=True)
coords=[]
for shards,q,lab,val in points:coords.append((85+math.log10(shards/5)*315,283-math.log10(q/1e6)*110))
line=' '.join(('M' if i==0 else 'L')+f'{x:.1f} {y:.1f}' for i,(x,y) in enumerate(coords))
b+=f'<path d="{line} L{coords[-1][0]:.1f} 300 L{coords[0][0]:.1f} 300 Z" fill="url(#scale-arrow-yellow)" opacity=".24"/>'
b+=path(line,YELLOW,4)
for x,y in coords:b+=path(f'M{x} {y+9}V300','#59502d',1,True)
for (x,y),(_,_,lab,val) in zip(coords,points):
    b+=f'<rect x="{x-9}" y="{y-9}" width="18" height="18" fill="#111" stroke="{YELLOW}" stroke-width="2"/><rect x="{x-4}" y="{y-4}" width="8" height="8" fill="{YELLOW}"/>'+txt(x,y-25,val,29,YELLOW,'middle',500,True)+txt(x,328,lab,18,WHITE,'middle',mono=True)
b='<g transform="translate(22 0)">'+b+'</g>'
b+=txt(69,28,'QPS',17,'#b9a762','end',mono=True)
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
 dict(id='opening',label='PlanetScale Postgres on Metal',theme='opening',html='<div class="opening-hero"><div class="cover-brand"><img src="assets/planetscale-white.svg" alt="PlanetScale"></div><h1>Postgres on <span class="accent">Metal</span></h1></div>',notes=speaker_notes['opening']),
 dict(id='nexus',label='More compute doesn’t solve every Postgres bottleneck.',theme='nexus',html='<div class="nexus-headline"><h2 class="nexus-meta-title" aria-hidden="false">How <span class="accent">Postgres</span> typically runs and scales in the cloud</h2><h2 class="nexus-challenge-title" aria-hidden="true">More compute doesn’t solve <span class="accent">every Postgres bottleneck.</span></h2></div><div class="nexus-art">'+(R/'assets/nexus.svg').read_text()+'</div>',notes=speaker_notes['nexus']),
 dict(id='vitalize',label='Vitalize: 2 ms p95, half the vCPUs',theme='vitalize',html=f'''<div class="case-heading vitalize-heading"><span class="vitalize-title-symbol"><img src="assets/vitalize-symbol.svg" alt=""></span><h2>Vitalize migrated from Supabase to Metal</h2></div><div class="vitalize-art">{vitalize_art}</div>''',notes=speaker_notes['vitalize']),
 dict(id='availability',label='Planetscale Postgres Architecture',theme='availability',html=f'''<div class="title-with-stat"><h2>Planetscale Postgres Architecture</h2><div class="sla"><strong>99.99<span>%</span></strong><p>single-region HA SLA</p></div></div><div class="ha-diagram">{ha}</div>''',notes=speaker_notes['availability']),
 dict(id='metal',label='Postgres on Metal: throughput and p99',theme='metal',html=f'''<div class="metal-heading"><h2>More QPS &amp; Lower p99 on <span class="metal-title-brand"><span class="metal-title-symbol"><img src="assets/planetscale-white.svg" alt="PlanetScale"></span><span class="accent">Metal</span></span></h2></div><div class="benchmark-grid"><div><h3>Throughput (QPS)</h3>{bars}</div><div><h3>p99 latency</h3><div class="chart-legend"><span class="ps-dot">PlanetScale</span><span class="aurora-dot">Aurora</span><span class="alloydb-dot">AlloyDB</span><span class="supabase-dot">Supabase</span></div>{latency}</div></div>''',notes=speaker_notes['metal']),
 dict(id='neki',label='Neki: Horizontal Scaling for Postgres',theme='neki',html=f'''<div class="neki-heading"><h2>Neki: Horizontal Scaling for Postgres</h2><div class="neki-lockup"><img src="assets/neki-cat.svg" alt="Neki"></div></div><div class="neki-topology">{neki}</div>''',notes=speaker_notes['neki']),
 dict(id='neki-scale',label='Neki: 118.5M queries per second',theme='neki neki-scale',html=f'''<div class="neki-heading"><h2><span class="yellow">118.5M</span> queries / second</h2><div class="neki-lockup"><img src="assets/neki-cat.svg" alt="Neki"></div></div><div class="scale-layout"><div><div class="scale-chart">{scale}</div></div><div class="scale-metrics"><div><strong>1.22 <span>PiB</span></strong><p>data</p></div><div><strong>512</strong><p>shards</p></div><div><strong>6.06 <span>ms</span></strong><p>router p99</p></div></div></div>''',notes=speaker_notes['neki-scale']),
 dict(id='convex',label='Convex reduced p99 query latency by over 50%',theme='customer-case convex',html=f'''<div class="case-heading convex-heading"><img class="convex-title-symbol" src="assets/convex-symbol-color.svg" alt=""><h2>Convex reduced p99 query latency by over 50%</h2></div><div class="convex-curves">{convex_plot}</div><div class="convex-quote"><q>p50 is the new p99.</q><span>Jamie Turner | CEO of Context</span></div>''',notes=speaker_notes['convex']),
 dict(id='intercom',label='Intercom: Faster Inbox, 60%+ Lower Cost',theme='customer-case intercom',html='''<div class="case-heading intercom-heading"><img src="assets/intercom-symbol.svg" alt=""><h2>Intercom: Faster Inbox, <span class="accent">60%+ Lower Cost</span></h2></div>
<div class="intercom-stage">
<div class="intercom-before fragment fade-out" data-fragment-index="1">'''+(R/'assets/intercom-story.svg').read_text()+'''</div>
<div class="intercom-results fragment" data-fragment-index="1">
<figure class="intercom-cost-chart"><div class="intercom-chart-labels"><span>Previous EBS io2 setup</span><span class="accent">PlanetScale Metal</span></div><img src="assets/intercom-original-cost-full.jpg" alt="Intercom’s original hourly database cost chart, showing a sharp drop as PlanetScale Metal went live. The published chart does not include numeric axis labels."><figcaption>Hourly database cost</figcaption></figure>
</div>
</div>
''',notes=speaker_notes['intercom']),
 dict(id='autumn',label='Autumn: two days to PlanetScale Metal',theme='customer-case autumn',html=f'''<div class="case-heading autumn-heading"><div class="autumn-title-symbol"><img src="assets/autumn.svg" alt=""></div><h2>Autumn migrated to PlanetScale Metal in two days</h2></div><div class="autumn-evidence"><div>{autumn_plot}</div><div class="autumn-migration"><div class="migration-number"><strong>2<span> days</span></strong><p>Migration</p></div><div class="cutover-number"><strong>Seconds</strong><p>Cutover downtime</p></div><div class="migration-assist"><span class="migration-team-symbol"><img src="assets/planetscale-white.svg" alt="PlanetScale"></span><p>Migration team<br><span>Copy + cutover support</span></p></div></div></div>''',notes=speaker_notes['autumn']),
 dict(id='migration',label='Migrate to PlanetScale',theme='migration',html=f'''<h2>Migrate to PlanetScale</h2><div class="migration-diagram">{migration}</div><div class="migration-paths" role="group" aria-label="Migration options"><div class="migration-path self-service"><div class="migration-path-heading"><h3>Self-service migration</h3></div></div><span class="migration-option-slash" aria-hidden="true">/</span><div class="migration-path planetscale-led"><div class="migration-path-heading"><span class="migration-team-symbol"><img src="assets/planetscale-white.svg" alt=""></span><h3>PlanetScale-led migration</h3></div></div></div><div class="migration-close"><strong>Technical discovery + migration assessment</strong></div>''',notes=speaker_notes['migration']),
 ]
# Local and remote data I/O paths; durability is covered on the HA slide.
slides.append(dict(id='metal-path', label='What is Metal?', theme='metal-path', html='<h2>What is <span class="accent">Metal</span>?</h2><div class="metal-path-art">'+(R/'assets/metal-path.svg').read_text()+'</div>', notes=speaker_notes['metal-path']))


# Optional cloud/account discovery slide immediately before the migration close.
slides.append(dict(id='cloud', label='Planetscale on your cloud', theme='cloud-offerings', html='''<h2><span class="accent">Planetscale</span> on your cloud</h2>
<div class="cloud-providers" role="group" aria-label="Supported clouds: AWS and Google Cloud">
<img class="cloud-aws-logo" src="assets/aws.svg" alt="AWS"><div class="cloud-google-lockup"><img src="assets/google-cloud-symbol.png" alt=""><span>Google Cloud</span></div>
</div>
<div class="cloud-deployments" role="group" aria-label="Two deployment choices, both operated by PlanetScale">
<div class="cloud-deployment hosted"><div class="cloud-account"><h3>PlanetScale-hosted</h3><div class="cloud-database"><img src="assets/planetscale-symbol-white.svg" alt=""><span>Postgres</span></div></div></div>
<div class="cloud-deployment byoc"><div class="cloud-account"><h3>Your cloud account <span>(BYOC)</span></h3><div class="cloud-database"><img src="assets/planetscale-symbol-white.svg" alt=""><span>Postgres</span></div><p class="cloud-enterprise">Enterprise</p></div></div>
</div>
<div class="cloud-shared-path" aria-hidden="true"><i></i><i></i></div>
<div class="cloud-operations"><strong>Your database <span>operated by PlanetScale</span></strong></div>
''', notes=speaker_notes['cloud']))

# Gong flow: problem, customer story, solution mechanism, evidence, then operating confidence and further proof.
slide_order=['opening','nexus','convex','intercom','metal-path','metal','availability','vitalize','autumn','neki','neki-scale','cloud','migration']
slides_by_id={slide['id']:slide for slide in slides}
assert set(slide_order)==set(slides_by_id) and len(slide_order)==len(slides)
slides=[slides_by_id[slide_id] for slide_id in slide_order]
if presenter: assert set(speaker_outline)==set(slides_by_id)
else:
    for slide in slides: slide.pop('notes', None)
content_output=R/'private' if presenter else R
content_output.mkdir(exist_ok=True)
(content_output/'slides.js').write_text('window.PITCH_BRAND = '+json.dumps((R/'assets/planetscale-white.svg').read_text())+';\nwindow.PITCH_SLIDES = '+json.dumps(slides,ensure_ascii=False,indent=2)+';\n')
(R/'qa/content.json').write_text(json.dumps([{'id':s['id'],'label':s['label']} for s in slides],indent=2))
(R/'qa/links.json').write_text('{}\n')
if presenter:
    (content_output/'speaker-notes.md').write_text('# PlanetScale Postgres — outline script\n\n'+'\n\n'.join(f'## {i}. {s["label"]}\n\n'+'\n'.join('- '+point for point in speaker_outline[s['id']]) for i,s in enumerate(slides,1))+'\n')
print(f'Built {len(slides)} slides ({"local presenter" if presenter else "public, no notes"}).')
