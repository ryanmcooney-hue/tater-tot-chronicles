from pathlib import Path
import xml.etree.ElementTree as E
import base64,io
from PIL import Image
import numpy as np
folder=Path("outputs/road-to-october")
ns="http://www.w3.org/2000/svg"
xl="http://www.w3.org/1999/xlink"
E.register_namespace("",ns);E.register_namespace("xlink",xl)
root=E.fromstring((folder/"Road to October - Refined Editable.svg").read_text(encoding="utf8"))
g=list(root)[0]
navy="#082b50";teal="#005C5C";accent="#38A89B"
def rect(x,y,w,h,fill):
 return E.Element("{"+ns+"}rect",{"x":str(x),"y":str(y),"width":str(w),"height":str(h),"fill":fill})
g.insert(2,rect(2,2,616,51,navy))
roofgroup=next(e for e in g if e.tag.endswith("g") and "opacity" in e.attrib)
roofimage=list(roofgroup)[0]
src=roofimage.get("{"+xl+"}href")
im=Image.open(io.BytesIO(base64.b64decode(src.split(",")[1]))).convert("RGBA")
a=np.array(im)[:,:,3]>100
runs=[]
for y,row in enumerate(a):
 transitions=np.diff(np.r_[False,row,False].astype(int))
 for left,right in zip(np.where(transitions==1)[0],np.where(transitions==-1)[0]):
  runs.append(f"M{left} {y}h{right-left}v1h-{right-left}z")
roofgroup.clear()
roofgroup.set("opacity","0.6")
# Preserve the supplied truss geometry as editable vector paths.
roofgroup.set("transform",f"translate(238.3 7) scale({159.4/im.width} {40/im.height})")
E.SubElement(roofgroup,"{"+ns+"}path",{"d":" ".join(runs),"fill":accent})
for e in g.iter():
 if e.tag.endswith("rect"):
  if e.get("fill")=="#edf2f4": e.set("fill",navy)
  if e.get("fill")=="#b9cecf":e.set("fill",navy)
  if e.get("fill")=="#dce6e7":e.set("fill","#87BDB8")
 if e.tag.endswith("text"):
  y=float(e.get("y","0"))
  if y in (36,67):e.set("fill","white")
for row in g:
 if not row.get("id","").startswith(("division-row","wild-card-row")):continue
 if row.get("id","").endswith("-2"):
  for e in row:
   if e.tag.endswith("rect") and e.get("fill")=="#D4ECE8":e.set("fill",teal)
   if e.tag.endswith("text"):e.set("fill","white")
footer=next(e for e in g if e.get("id")=="Seattle-playoff-estimate")
list(footer)[0].set("fill",navy)
footer.insert(1,rect(2,202,616,2,accent))
footer.insert(2,rect(2,204,7,18,teal))
footer.insert(3,rect(611,204,7,18,teal))
g.append(rect(474,22,62,2,accent));g.append(rect(474,29,44,2,accent))
g.append(rect(2,72,616,1,teal))
g.append(E.Element("{"+ns+"}rect",{"x":"1.5","y":"1.5","width":"617","height":"221","fill":"none","stroke":navy,"stroke-width":"3"}))
out=folder/"Road to October - Navy Editable.svg"
E.ElementTree(root).write(out,encoding="utf-8",xml_declaration=True)
# The styling pass must preserve every text value and its position.
old=E.fromstring((folder/"Road to October - Refined Editable.svg").read_text(encoding="utf8"))
texts=lambda r:[(e.text,e.get("x"),e.get("y")) for e in r.iter("{"+ns+"}text")]
assert texts(root)==texts(old)
print("Verified all text, standings and text positions preserved.")
