from pathlib import Path
import xml.etree.ElementTree as E
import base64, io
from PIL import Image
from xml.sax.saxutils import escape
folder=Path("outputs/road-to-october")
root=E.fromstring((folder/"Road to October.svg").read_text(encoding="utf8"))
images=root.findall(".//{http://www.w3.org/2000/svg}image")
href="{http://www.w3.org/1999/xlink}href"
navy="#082b50";teal="#005C5C"
league=Image.open(Path.home()/"Downloads"/"American_League_logo.svg.webp")
buffer=io.BytesIO()
league.save(buffer,format="PNG")
league_uri="data:image/png;base64,"+base64.b64encode(buffer.getvalue()).decode()
parts=[]
def rect(x,y,w,h,fill):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'
def text(s,x,y,size=17,fill=navy,anchor="start",weight="bold"):
 return f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>'
def image(i,x,y,w,h):
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="{images[i].get(href)}"/>'
parts += [rect(0,0,620,224,navy),rect(2,2,616,220,"white"),rect(2,2,616,36,navy),image(2,12,4,30,32),text("ROAD TO OCTOBER",54,27,23,"white"),f'<image x="570" y="4" width="38" height="32" preserveAspectRatio="xMidYMid meet" xlink:href="{league_uri}"/>']
parts += [rect(2,39,270,27,"#e9eff1"),rect(274,39,344,27,"#e9eff1"),rect(272,39,2,183,navy)]
parts += [text("AL WEST",13,58,15),text("W–L",171,58,13,anchor="middle"),text("GB",258,58,13,anchor="end"),text("WILD CARD",286,58,15),text("W–L",482,58,13,anchor="middle"),text("GB",604,58,13,anchor="end")]
for i,(im,record,gap) in enumerate([(1,"67–46","—"),(2,"62–51","5.0")]):
 y=66+i*39
 parts += [f'<g id="division-row-{i+1}">',rect(2,y,270,39,"#D4ECE8" if i==1 else "white"),text(str(i+1),15,y+26,15,teal),image(im,62,y+4,34,31),text(record,171,y+26,21,anchor="middle"),text(gap,258,y+26,20,anchor="end"),"</g>"]
parts += ['<g id="Seattle-playoff-estimate">',rect(2,146,270,76,teal),text("SEATTLE PLAYOFF ODDS",14,165,14,"white"),text("ESTIMATED",14,207,12,"#d2eeea"),text("80%",259,210,39,"white","end"),"</g>"]
for i,(im,rank,record,gap) in enumerate([(4,"WC1","64–50","+3.5"),(5,"WC2","62–51","+2.0"),(6,"WC3","60–53","—"),(7,"4","59–54","1.0"),(8,"5","57–57","3.5")]):
 y=66+i*31
 parts += [f'<g id="wild-card-row-{i+1}">',rect(274,y,344,31,"#D4ECE8" if i==1 else ("#f4f6f7" if i%2 else "white")),text(rank,286,y+21,14,teal),image(im,359,y+2,34,27),text(record,482,y+22,20,anchor="middle"),text(gap,604,y+22,20,anchor="end"),"</g>"]
svg='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="620" height="224" viewBox="0 0 620 224"><g id="Road-to-October">'+''.join(parts)+'</g></svg>'
(folder/"Road to October - Compact Editable.svg").write_text(svg,encoding="utf8")
