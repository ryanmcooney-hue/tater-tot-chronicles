const {chromium}=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');const path=require('node:path');
(async()=>{const b=await chromium.launch({channel:'msedge',headless:true});const p=await b.newPage({viewport:{width:1550,height:1014},deviceScaleFactor:2});await p.goto(pathToFileURL(path.resolve('assets/pacific-weekly-template.svg')).href);await p.screenshot({path:'assets/pacific-weekly-template.png'});await b.close()})();
