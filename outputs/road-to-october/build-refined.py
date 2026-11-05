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

parts += [rect(0,0,620,224,navy),rect(2,2,616,220,"white"),rect(2,2,616,3,teal)]
parts += ['<g opacity="0.12">',image(0,198,7,240,40),'</g>',image(2,15,10,32,36),text("ROAD TO OCTOBER",65,36,24),f'<image x="568" y="8" width="40" height="39" preserveAspectRatio="xMidYMid meet" xlink:href="{league_uri}"/>',rect(14,50,592,2,teal)]
parts += [rect(2,53,270,20,"#edf2f4"),rect(274,53,344,20,"#edf2f4"),rect(272,53,2,149,"#b9cecf")]
parts += [text("AL WEST",14,67,13),text("W–L",168,67,11,anchor="middle"),text("GB",257,67,11,anchor="end"),text("WILD CARD",286,67,13),text("W–L",482,67,11,anchor="middle"),text("GB",604,67,11,anchor="end")]
for i,(im,record,gap) in enumerate([(1,"67–46","—"),(2,"62–51","5.0")]):
 y=73+i*64.5
 parts += [f'<g id="division-row-{i+1}">',rect(2,y,270,64.5,"#D4ECE8" if i==1 else "white"),rect(2,y,4,64.5,teal if i==1 else "white"),text(str(i+1),16,y+39,14,teal),image(im,56,y+12,35,40),text(record,168,y+40,23,anchor="middle"),text(gap,257,y+40,21,anchor="end"),"</g>"]
for i,(im,rank,record,gap) in enumerate([(4,"WC1","64–50","+3.5"),(5,"WC2","62–51","+2.0"),(6,"WC3","60–53","—"),(7,"4","59–54","1.0"),(8,"5","57–57","3.5")]):
 y=73+i*25.8
 parts += [f'<g id="wild-card-row-{i+1}">',rect(274,y,344,25.8,"#D4ECE8" if i==1 else "white"),rect(274,y,3,25.8,teal if i==1 else "white"),text(rank,287,y+18,12,teal),image(im,357,y+2,32,22),text(record,482,y+18.5,18,anchor="middle"),text(gap,604,y+18.5,18,anchor="end")]
 if i<4:parts += [rect(285,y+25,321,.6,"#dce6e7")]
 parts += ["</g>"]
parts += ['<g id="Seattle-playoff-estimate">',rect(2,202,616,20,teal),text("PLAYOFF ODDS • 80%",310,216.5,13,"white","middle"),text("EST.",605,216,9,"#d2eeea","end"),"</g>"]
svg='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="620" height="224" viewBox="0 0 620 224"><g id="Road-to-October">'+''.join(parts)+'</g></svg>'
(folder/"Road to October - Refined Editable.svg").write_text(svg,encoding="utf8")
