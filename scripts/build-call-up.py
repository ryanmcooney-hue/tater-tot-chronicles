"""Build the call-up web edition from the supplied magazine PDF."""
from pathlib import Path
from pypdf import PdfReader
from PIL import Image
import re, html

root = Path(__file__).resolve().parent.parent
pdf = PdfReader(root / 'assets/23Call up feature.pdf')
for page, index, name in [(0,1,'call-up-mlb-family'),(1,0,'call-up-fans'),(2,0,'call-up-aa-family'),(5,0,'call-up-tacoma-family')]:
    pdf.pages[page].images[index].image.convert('RGB').save(root / f'assets/{name}.webp', quality=88)
Image.open(root / 'assets/call-up-cover.png').convert('RGB').save(root / 'assets/call-up-cover.webp', quality=88)

source = (root / 'recaps.html').read_text(encoding='utf-8')
header = source.split('<section class="pagehero">')[0]
header = header.replace('class="active" href="recaps.html"', 'class="" href="recaps.html"').replace('class="" href="features.html"', 'class="active" href="features.html" aria-current="page"')
footer = '<footer>' + source.split('<footer>',1)[1]
def shell(title, description, body, slug):
    head = re.sub(r'<title>.*?</title>', f'<title>{title} | Tater Tot Chronicles</title>', header)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', head)
    head = head.replace('</head>', f'<link rel="canonical" href="https://tatertotchronicles.com/{slug}"><meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:image" content="https://tatertotchronicles.com/assets/call-up-mlb-family.webp"><link rel="stylesheet" href="features.css"></head>')
    return head + '<main>' + body + '</main>' + footer
def figure(name, caption):
    return f'<figure class="feature-photo"><a href="assets/{name}.webp"><img src="assets/{name}.webp" alt="{html.escape(caption)}" width="1536" height="1024" loading="lazy"></a><figcaption>{html.escape(caption)}</figcaption></figure>'
def text(page):
    return pdf.pages[page].extract_text().replace('\ufffd','f').strip()
def para(s):
    return '<p>' + html.escape(re.sub(r'\s+', ' ', s).strip()) + '</p>'
intro = text(0).split('The last time')[1].split('Welcome to the Show')[0]
intro = para('The last time'+intro)
second = text(1).split('Soon is now.')[0].replace('fast-\ntracked','fast-tracked').replace('Double-\nA','Double-A')
for start in ['Tater’s rapid ascent', 'So as he sits']:
    second = second.replace(start, '\n\n'+start)
intro += ''.join(para(s) for s in second.split('\n\n'))
qa = '\n'.join(text(i) for i in [2,3,4])
qa = re.sub(r'Tater Tot McGee with his family and girlfriend after his first Double-A game\.', '', qa)
qa = re.sub(r'(?m)^\d+\s*$', '', qa)
parts = re.split(r'(PACIFIC:|TATER:)', qa)
interview = ''.join('<p class="'+('question' if parts[i]=='PACIFIC:' else 'answer')+'"><strong>'+parts[i]+'</strong> '+html.escape(re.sub(r'\s+',' ',parts[i+1]).strip())+'</p>' for i in range(1,len(parts),2))
closing = text(5).split('The Tacoma limb')[0]
body = '<section class="pagehero"><div class="wrap"><a class="kicker" href="features.html">Features · PACIFIC Sunday Magazine</a><h1 class="h1">Welcome to the Show</h1><p class="dek">In his first professional season, No. 1 overall pick Tater Tot McGee has gone from Triple-A right into the middle of an MLB pennant race.</p><p>By Ryan Cooney · <time datetime="2026-08-02">August 2, 2026</time></p><a class="btn ghost" href="assets/23Call%20up%20feature.pdf">Open original magazine · PDF</a></div></section>'
body += '<article class="feature-article">'+figure('call-up-mlb-family','McGee with his family and girlfriend after his first big-league game.')+intro+figure('call-up-fans','Soon is now.')+'<h2>The call to Seattle</h2>'+interview+figure('call-up-aa-family','Tater Tot McGee with his family and girlfriend after his first Double-A game.')+para(closing)+figure('call-up-tacoma-family','The Tacoma limb of the family tree and Dad in his hat.')+'<p class="source-note">Web edition of the August 2, 2026 PACIFIC feature. Story and captions reproduced from the original magazine.</p><a class="btn" href="features.html">All features →</a></article>'
(root/'call-up.html').write_text(shell('Welcome to the Show','Tater Tot McGee talks family, his call to Seattle and joining a pennant race. A PACIFIC feature by Ryan Cooney.',body,'call-up.html'),encoding='utf-8')
cards = '<section class="pagehero"><div class="wrap"><div class="kicker">PACIFIC Sunday Magazine</div><h1 class="h1">Features</h1><p class="dek">The people, places and turning points behind Tater Tot McGee’s baseball journey.</p></div></section><div class="wrap feature-grid">'
for href,img,date,title,desc in [('call-up.html','call-up-mlb-family.webp','August 2, 2026','Welcome to the Show','The call to Seattle, the first phone calls home, and the pressure of joining a pennant race.'),('mcgee-story.html','family-farm-display.webp','Summer 2025','Tater Tot McGee: A Family Story','Irish roots, an Idaho potato farm and six generations of baseball.')]:
    cards += f'<a class="feature-card" href="{href}"><img src="assets/{img}" alt="" loading="lazy"><div><span class="kicker">{date}</span><h2>{title}</h2><p>{desc}</p><span class="feature-read">Read feature →</span></div></a>'
cards += '</div>'
(root/'features.html').write_text(shell('Features','Long-form PACIFIC stories from the Tater Tot McGee archive.',cards,'features.html'),encoding='utf-8')
print('Built Features and call-up web edition with four published photos.')
