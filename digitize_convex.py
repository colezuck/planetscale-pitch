"""Extract an approximate p99 trace from the customer-published chart.

This is chart digitization, not raw telemetry. Requires Pillow.
The source image is retained unchanged; missing/clipped pixels stay missing.
"""
from pathlib import Path
import json
from PIL import Image
R=Path(__file__).resolve().parent
im=Image.open(R/'assets/convex-original-results.png').convert('RGB')
# Digitize only the red p99 trace, preserving gaps where the source clips peaks.
series=[]
for name,top,bottom,xmin,xmax,maximum in [('query',114,522,121,1433,20),('commit',784,1191,106,1433,200)]:
 points=[]
 for x in range(xmin,xmax+1):
  ys=[y for y in range(top,bottom+1) if (lambda c:c[0]>205 and c[1]<115 and 55<c[2]<145 and c[0]-c[1]>100)(im.getpixel((x,y)))]
  points.append([x,round(sum(ys)/len(ys),2) if ys else None])
 series.append(dict(name=name,top=top,bottom=bottom,xmin=xmin,xmax=xmax,max_ms=maximum,points=points))
(R/'qa/convex-p99-digitized.json').write_text(json.dumps({'source':'assets/convex-original-results.png','method':'Red p99 trace extracted at source-pixel resolution. Approximate visual reconstruction, not raw telemetry. Missing/clipped pixels remain gaps; no invented samples.','series':series},indent=2))
