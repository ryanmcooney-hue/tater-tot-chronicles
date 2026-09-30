const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const write = (name, html) => fs.writeFileSync(path.join(root, name), html);
const template = read('issue.html');
const match = template.match(/const DATA=(\{.*?\});let n=/s);
if (!match) throw new Error('Expected JSON DATA followed by ;let n= in issue.html');
const data = JSON.parse(match[1]);
const numbers = Object.keys(data).map(Number).sort((a, b) => a - b);
const escape = value => String(value).replace(/[&<>"']/g, c => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c]));
const base = 'https://tatertotchronicles.com/';
const imageFor = n => data[n].image || 'assets/' + String(n + 4).padStart(2, '0') + 'Issue' + n + '.png';
const socialFor = n => data[n].socialImage || imageFor(n);
const checkAsset = value => {
  if (!/^https?:\/\//.test(value) && !fs.existsSync(path.join(root, value))) throw new Error('Missing image: ' + value);
};
const pages = [];
for (const n of numbers) {
  const x = data[n];
  if (!Number.isInteger(n) || n < 1 || x.n !== n) throw new Error('Invalid issue number: ' + n);
  for (const field of ['title', 'month', 'level', 'note']) {
    if (typeof x[field] !== 'string') throw new Error('Missing ' + field + ' for issue ' + n);
  }
  checkAsset(imageFor(n));
  checkAsset(socialFor(n));
  const title = 'Issue ' + n + ' · ' + x.title + ' | Tater Tot Chronicles';
  const url = base + 'issue-' + n + '.html';
  const image = new URL(socialFor(n), base).href;
  let html = template.replace(/<script>const DATA=.*?<\/script>/s, '');
  html = html.replace(/<title>.*?<\/title>/, '<title>' + escape(title) + '</title>')
    .replace(/<meta name="description" content="[^"]*">/, '<meta name="description" content="' + escape(x.note) + '">');
  const metadata = [
    ['property', 'og:title', title], ['property', 'og:description', x.note],
    ['property', 'og:image', image], ['property', 'og:url', url],
    ['property', 'og:type', 'article'], ['name', 'twitter:card', 'summary_large_image'],
    ['name', 'twitter:title', title], ['name', 'twitter:description', x.note],
    ['name', 'twitter:image', image], ['name', 'twitter:url', url]
  ].map(([attr, key, value]) => '<meta ' + attr + '="' + key + '" content="' + escape(value) + '">').join('\n');
  html = html.replace('</head>', '\n' + metadata + '\n<link rel="canonical" href="' + url + '">\n</head>');
  for (const [id, value] of Object.entries({
    ikicker: 'PACIFIC · Issue ' + n + ' · ' + x.month,
    ititle: x.title, inote: x.note, ilevel: x.level, iseries: x.series || ''
  })) {
    const pattern = new RegExp('(<[^>]+\\bid="' + id + '"[^>]*>)[^<]*(</[^>]+>)');
    if (!pattern.test(html)) throw new Error('Missing template element: ' + id);
    html = html.replace(pattern, (_, start, end) => start + escape(value) + end);
  }
  html = html.replace(/(<img\b[^>]*\bid="issueimg"[^>]*)(>)/, (_, start, end) => start + ' src="' + escape(imageFor(n)) + '"' + end)
    .replace(/(<a\b[^>]*\bid="full"[^>]*)(>)/, (_, start, end) => start + ' href="' + escape(imageFor(n)) + '"' + end);
  for (const [id, neighbor] of [['prev', n - 1], ['next', n + 1]]) {
    const pattern = new RegExp('(<a\\b[^>]*\\bid="' + id + '"[^>]*href=")[^"]*("[^>]*>)');
    html = html.replace(pattern, (_, start, end) => start + (data[neighbor] ? 'issue-' + neighbor + '.html' : '#') +
      (data[neighbor] ? end : end.slice(0, -1) + ' style="visibility:hidden">'));
  }
  pages.push(['issue-' + n + '.html', html]);
}
let archive = read('archive.html').replace(/href="issue\.html\?issue=(\d+)"/g, 'href="issue-$1.html"');
const cards = numbers.slice().reverse().filter(n => !archive.includes('href="issue-' + n + '.html"')).map(n => {
  const x = data[n];
  return '<a class="archivecard" href="issue-' + n + '.html"><img src="' + escape(imageFor(n)) +
    '" alt="' + escape('PACIFIC Issue ' + n + ' — ' + x.title) + '"><div class="copy"><div class="kicker">Issue ' +
    n + ' · ' + escape(x.month) + '</div><h2>' + escape(x.title) + '</h2><p>' + escape(x.note) +
    '</p><div class="labelrow"><span class="pill green">' + escape(x.level) + '</span><span class="pill">' +
    escape(x.series || '') + '</span></div></div></a>';
}).join('');
if (!archive.includes('<div class="archivegrid">')) throw new Error('Missing archive grid');
archive = archive.replace('<div class="archivegrid">', '<div class="archivegrid">' + cards);
for (const [name, html] of pages) write(name, html);
write('archive.html', archive);
console.log('Generated ' + pages.length + ' standalone issue pages and updated archive links.');
