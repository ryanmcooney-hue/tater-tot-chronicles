from pathlib import Path
import openpyxl, datetime, json, csv, base64, io
from PIL import Image
from xml.sax.saxutils import escape

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
SOURCE=Path('C:/Users/user/Downloads/Tater Game Log (4).xlsx')
ws=openpyxl.load_workbook(SOURCE,data_only=True)['AAA 2026']
headers=list(next(ws.values))[:20]
rows=[]
for idx,r in enumerate(ws.values,1):
    if isinstance(r[1],datetime.datetime) and r[1].year==2026 and r[1].month==7:
        d=dict(zip(headers,r[:20])); d['source_row']=idx; rows.append(d)
assert len(rows)==20 and rows[0]['Date'].day==1 and rows[-1]['Date'].day==26
keys=['AB','R','H','RBI','BB','SO','HR','2B','3B','SB','HBP','SF']
tot={k:0 for k in keys}; points=[]; discrepancies=[]
def rates(t):
    avg=t['H']/t['AB']; obp=(t['H']+t['BB']+t['HBP'])/(t['AB']+t['BB']+t['HBP']+t['SF'])
    slg=(t['H']+t['2B']+2*t['3B']+3*t['HR'])/t['AB']
    return dict(AVG=avg,OBP=obp,SLG=slg,OPS=obp+slg)
for r in rows:
    assert all(isinstance(r[k],(int,float)) for k in keys)
    assert r['2B']+r['3B']+r['HR']<=r['H']<=r['AB']
    for k in keys: tot[k]+=int(r[k])
    points.append(dict(date=r['Date'].strftime('%Y-%m-%d'),**tot,**rates(tot)))
    calc=rates(r)
    for k,col in [('AVG','AVG'),('OBP','OBP'),('SLG','SLUG'),('OPS','OPS')]:
        if abs(calc[k]-r[col])>0.00001: discrepancies.append(f"Row {r['source_row']} ({r['Date']:%B %d}) {k}: stored {r[col]:.6f}; calculated {calc[k]:.6f}")
with (OUT/'july-aaa-chart-data.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=points[0].keys()); w.writeheader(); w.writerows(points)
(OUT/'source-audit.txt').write_text('Source: '+str(SOURCE)+'\nSheet: AAA 2026; rows 22–41. July 1–26 only. No other sheet included.\n\n'+json.dumps(tot,indent=2)+'\n'+json.dumps(rates(tot),indent=2)+'\n\nAVG = H/AB. OBP = (H+BB+HBP)/(AB+BB+HBP+SF). SLG = (H+2B+2*3B+3*HR)/AB. OPS = OBP+SLG. All rates calculated from counting stats; no averaging of game rates.\n\nStored rate discrepancies:\n'+'\n'.join(discrepancies)+'\n\nGame of the Month: July 4, 10 total bases (highest July AAA total), two HR and a double. July 21: nine total bases and three RBI.\nFinal six games: 9-for-28 (.321). Seven-game hitting streak July 18–25.\nCanon: Section 6 confirms July 4 and July 21 two-HR games. Local Canon predates Seattle promotion. Call-up conclusion supplied explicitly by user; no exact promotion date asserted.\nGame results/scores are not present in the source; none invented or included.\nDesign: April recap PNG and April remaster Affinity master; current PACIFIC logo preserved.\n',encoding='utf8')

NAVY='#0b174e'; TEAL='#006653'; LINE='#a9ccd8'; LIGHT='#e1e7eb'
parts=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1536" height="1024" viewBox="0 0 1536 1024">','<title>PACIFIC July 2026 Recap — Tacoma AAA</title>']
def rect(x,y,w,h,fill,stroke=None):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
def line(x,y,x2,y2,color=LINE,width=1): parts.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
def text(s,x,y,size=18,color=NAVY,font='Arial',weight='normal',anchor='start'):
    if font=='Impact':
        font='Arial'; scale=.77
        parts.append(f'<text transform="translate({x} {y}) scale({scale} 1)" x="0" y="0" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
    else:
        parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
def lines(ss,x,y,size=18,gap=26,**kwargs):
    for i,s in enumerate(ss): text(s,x,y+i*gap,size,**kwargs)
def pic(im,x,y,w,h):
    b=io.BytesIO(); im.save(b,format='PNG'); uri='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
    parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="{uri}"/>')
def fmt(v): return f'{v:.3f}'.lstrip('0')
def banner(s,x,y,w,color=TEAL):
    if y==798:
        parts.append(f'<path d="M{x},{y+7} L{x+24},{y+1} L{x+w-29},{y} L{x+w},{y+7} L{x+w-16},{y+17} L{x+w-2},{y+23} L{x+w-42},{y+28} L{x+40},{y+28} L{x+11},{y+24} L{x+25},{y+19} Z" fill="{color}"/>')
    else: rect(x,y,w,32,color)
    text(s,x+w/2,y+24,26,'white','Impact','bold','middle')

rect(0,0,1536,1024,'white')
text('PACIFIC',28,37,24,NAVY,'Impact','bold'); line(122,21,122,42); text('JULY RECAP',141,37,24,TEAL,'Impact','bold')
text('A MONTHLY RECAP OF TATER TOT McGEE’S FIRST PRO SEASON',28,63,14)
pic(Image.open(ROOT/'assets/pacific-recap-logo.png'),608,4,300,67)
text('TATER TOT CHRONICLES',1509,35,21,NAVY,'Impact','bold','end'); text('SUMMER 2026',1509,63,21,TEAL,'Impact','bold','end')
line(26,79,1510,79,TEAL,3)
april=Image.open(ROOT/'assets/april-recap.png')
pic(april.crop((29,94,156,220)),29,94,127,126)
pic(april.crop((1019,94,1147,223)),1019,94,128,129)
from PIL import ImageFont
headline='TATER’S FINAL TACOMA CHAPTER'
headline_width=ImageFont.truetype('C:/Windows/Fonts/impact.ttf',96).getlength(headline)
parts.append(f'<text transform="translate(187 179) scale({817/headline_width} 1)" fill="{NAVY}" font-family="Impact" font-size="96">{headline}</text>')
text('Tater Tot McGee’s final month in Triple-A before his promotion to Seattle.',197,221,21)
line(26,237,1149,237); line(1172,98,1172,967)

def chart(metric,x,y,w,h,maximum,step,color,large=False):
    parts.append(f'<g id="cumulative-july-aaa-{metric.lower()}">')
    rect(x,245 if large else 564,83 if large else 65,34 if large else 29,color); text(metric,x+10,270 if large else 587,29,'white','Impact','bold')
    for i in range(round(maximum/step)+1):
        v=i*step; yy=y+h-v/maximum*h
        line(x,yy,x+w,yy,LIGHT,.8); text(fmt(v),x-12,yy+4,13,NAVY,anchor='end')
    line(x,y,x,y+h,'#9ca6ae'); line(x,y+h,x+w,y+h,'#9ca6ae')
    coords=[(x+i*w/(len(points)-1),y+h-p[metric]/maximum*h) for i,p in enumerate(points)]
    parts.append('<polyline fill="none" stroke="'+color+'" stroke-width="2.2" points="'+' '.join(f'{a:.3f},{b:.3f}' for a,b in coords)+'"/>')
    for i,(a,b) in enumerate(coords):
        parts.append(f'<circle cx="{a:.3f}" cy="{b:.3f}" r="{3 if large else 2}" fill="white" stroke="{color}" stroke-width="1.7"/>')
        line(a,y+h,a,y+h+5,'#9ca6ae')
    for i in [0,2,4,6,8,10,12,14,16,19]:
        text(str(i+1),x+i*w/19,y+h+19,12,anchor='middle')
    text('GAME',x-40,y+h+19,12,NAVY,'Impact','bold')
    text('JULY / AAA',x+w/2,y+h+44,18,color,'Impact','bold','middle')
    a,b=coords[-1]; bw=77 if large else 67
    parts.append(f'<polygon points="{a+10},{b} {a+22},{b-18} {a+bw},{b-18} {a+bw},{b+18} {a+22},{b+18}" fill="{color}"/>')
    text(fmt(points[-1][metric]),a+bw-6,b+9,28,'white','Impact','bold','end')
    parts.append('</g>')

chart('AVG',80,259,758,230,.4,.05,NAVY,True)
text('FINISHED STRONG',1036,314,24,TEAL,'Impact','bold','middle')
lines(['Hit .321 (9-for-28)','in his final six games','at Reno, with two homers','and five RBI.'],936,352,18,28)
text('CUMULATIVE JULY AAA STATS',1038,481,13,TEAL,'Impact','bold','middle')
line(26,555,1149,555)
chart('OBP',72,597,255,138,.4,.05,TEAL)
chart('SLG',461,597,232,138,.8,.1,TEAL)
chart('OPS',828,597,240,138,1.2,.2,NAVY)
line(410,568,410,773); line(773,568,773,773); line(26,793,1149,793)

text('JULY SLASH LINE',1344,116,24,TEAL,'Impact','bold','middle'); line(1208,124,1493,124)
text(' / '.join(fmt(points[-1][m]) for m in ['AVG','OBP','SLG']),1344,178,48,NAVY,'Impact','bold','middle')
text('AVG  /  OBP  /  SLG',1344,206,21,TEAL,'Impact','bold','middle'); line(1220,218,1477,218,NAVY,1.5)
text(fmt(points[-1]['OPS']),1344,270,54,TEAL,'Impact','bold','middle'); text('OPS',1344,301,24,NAVY,'Impact','bold','middle')
banner('JULY AT A GLANCE',1192,315,304,NAVY)
for i,(label,value) in enumerate([('GAMES',20),('HITS',tot['H']),('DOUBLES',tot['2B']),('TRIPLES',tot['3B']),('HOME RUNS',tot['HR']),('RBI',tot['RBI']),('WALKS',tot['BB']),('STRIKEOUTS',tot['SO']),('STOLEN BASES',tot['SB'])]):
    yy=371+i*25; text(label,1200,yy,18,NAVY,'Impact','bold'); text(str(value),1468,yy,19,NAVY,'Arial','bold','end'); line(1192,yy+9,1496,yy+9,LIGHT)
line(1192,588,1496,588)
pic(april.crop((1423,594,1495,703)),1423,594,72,109)
text('CALL-UP / PROMOTION',1199,618,23,TEAL,'Impact','bold')
text('TACOMA TO SEATTLE',1199,651,29,NAVY,'Impact','bold')
lines(['July closed with a promotion','to the Seattle Mariners.'],1199,676,18,24)
banner('GAME OF THE MONTH',1192,713,304)
rect(1192,745,304,222,'white',LIGHT)
text('July 4 vs. Reno',1344,774,23,TEAL,'Impact','bold','middle')
lines(['3-for-5 (.600)','1 Double','2 Runs','0 Strikeouts'],1210,804,17,27)
lines(['2 Home Runs','2 RBI','0 Walks','0 Stolen Bases'],1352,804,17,27)
text('10 total bases: his July AAA high.',1344,918,14,NAVY,anchor='middle')
text('2.600 OPS',1344,953,29,TEAL,'Arial','bold','middle')

june=Image.open(ROOT/'assets/june-recap.png')
pic(june.crop((121,887,198,965)),45,810,145,147)
rect(223,803,473,164,'white',LIGHT); banner('JULY HIGHLIGHTS',235,798,449)
line(457,839,457,953,LIGHT); line(236,898,684,898,LIGHT)
for x,y,title,body in [(288,847,'TWO-HOMER GAMES',['July 4: two HR and a double.','July 21: two HR, three RBI.']), (520,847,'SEVEN STRAIGHT',['Hit safely July 18–25.','12-for-31 (.387) in that span.']), (288,920,'EXTRA-BASE IMPACT',['Four doubles and four HR','among his 25 July hits.']), (520,920,'RENO SEND-OFF',['9-for-28 in his final series,','with two HR and five RBI.'])]:
    text(title,x,y,16,TEAL,'Impact','bold'); lines(body,x,y+19,12,15)
# Editable highlight icons, matching the established monthly visual vocabulary.
parts.append(f'<path d="M258 838 C266 850 269 850 265 862 C277 856 277 869 271 878 C265 891 245 886 244 873 C241 863 250 854 249 849 C251 854 255 855 255 860 C260 853 260 845 258 838 Z" fill="{TEAL}"/>')
rect(478,842,29,35,TEAL); rect(481,850,23,24,'white'); text('7',492,870,23,TEAL,'Arial','bold','middle'); line(484,837,484,846,TEAL,4); line(502,837,502,846,TEAL,4)
for xx,yy,hh in [(240,936,15),(252,925,26),(264,914,37)]: rect(xx,yy,9,hh,TEAL)
for rr in [17,11,5]: parts.append(f'<circle cx="491" cy="934" r="{rr}" fill="none" stroke="{TEAL}" stroke-width="2"/>')
parts.append(f'<path d="M490 935 L511 914 M503 913 L512 912 L511 921" fill="none" stroke="{TEAL}" stroke-width="4"/>')
rect(718,803,431,164,'white',LIGHT); banner('KEY JULY MILESTONES',730,798,407)
for i,(date,copy) in enumerate([('JUL 4','First Triple-A two-home-run game.'),('JUL 21','Second two-homer game for Tacoma.'),('JUL 26','Final Triple-A appearance.'),('JULY','Promoted to the Seattle Mariners.')]):
    yy=850+i*28; text(date,733,yy,15,TEAL,'Impact','bold'); text(copy,815,yy,14); line(730,yy+9,1137,yy+9,LIGHT)
parts.append(f'<path d="M22 980 H1388 L1374 1016 H22 Z" fill="{NAVY}"/>')
text('TRIPLE-A / PACIFIC COAST LEAGUE',35,1005,21,'white','Impact','bold')
parts.append(f'<circle cx="440" cy="998" r="7" fill="{TEAL}"/>')
text('THROUGH JULY 26, 2026',460,1005,21,'white','Impact','bold')
import math
for cx in [1252,1295,1337]:
    vertices=[(cx+(14 if i%2==0 else 5.5)*math.cos(-math.pi/2+i*math.pi/5),998+(14 if i%2==0 else 5.5)*math.sin(-math.pi/2+i*math.pi/5)) for i in range(10)]
    parts.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in vertices)+f'" fill="{TEAL}"/>')
for i in range(5):
    x=1390+i*23; parts.append(f'<path d="M{x} 1016 l14 -36 h12 l-14 36 Z" fill="{TEAL if i%2==0 else NAVY}"/>')
text('Source: Tater Game Log (4).xlsx • AAA 2026 • July-only cumulative rates calculated from game counting stats.',28,975,9,'#526879')
parts.append('</svg>')
(OUT/'PACIFIC July 2026 Recap - Matched.svg').write_text('\n'.join(parts),encoding='utf8')
print(json.dumps({'games':len(rows),'totals':tot,'rates':rates(tot),'stored_rate_discrepancies':len(discrepancies)},indent=2))

