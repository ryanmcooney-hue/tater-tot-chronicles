const {chromium}=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
(async()=>{const b=await chromium.launch({headless:true,channel:'msedge'}); const p=await b.newPage();
for(const width of [1440,390]){await p.setViewportSize({width,height:1000});for(const file of ['index.html','recaps.html']){
await p.goto(pathToFileURL(path.resolve(file)).href);await p.locator(file==='index.html'?'#recaps':'#july').scrollIntoViewIfNeeded();await p.locator('img[src="assets/home-july-recap.webp"]').evaluate(i=>i.decode());
const result=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src),links:[...document.querySelectorAll('[href],[src]')].map(e=>e.getAttribute('href')||e.getAttribute('src'))}));
for(const link of result.links){if(/^(https?:|mailto:|#)/.test(link))continue;const [name,anchor]=link.split('#');const target=path.resolve(name.split('?')[0]);if(!fs.existsSync(target))throw Error('Missing '+link);if(anchor&&!fs.readFileSync(target,'utf8').includes('id="'+anchor+'"'))throw Error('Missing anchor '+link)}
if(result.overflow||result.broken.length)throw Error(JSON.stringify(result));console.log(file,width,'PASS');await p.screenshot({path:path.join(__dirname,`${file}-${width}.png`)});
}}await b.close()})().catch(e=>{console.error(e);process.exit(1)});
