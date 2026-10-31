const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const dir='outputs/weekly-rebrand';fs.mkdirSync(dir,{recursive:true});
 const backup='outputs/weekly-images-before-rebrand';fs.mkdirSync(backup,{recursive:true});
 const template=fs.readFileSync('assets/pacific-weekly-template.png').toString('base64');
 const b=await chromium.launch({channel:'msedge',headless:true});
 for(let n=1;n<=18;n++){
  const name=String(n+4).padStart(2,'0')+'Issue'+n+'.png';
  const original=path.join(backup,name);if(!fs.existsSync(original))fs.copyFileSync(path.join('assets',name),original);
  const data=fs.readFileSync(original).toString('base64');
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1550" height="1014" viewBox="0 0 1550 1014"><defs><clipPath id="branding"><rect x="1000" y="5" width="546" height="190"/><rect x="0" y="952" width="1550" height="62"/></clipPath></defs><image href="data:image/png;base64,${data}" width="1550" height="1014"/><image href="data:image/png;base64,${template}" width="1550" height="1014" clip-path="url(#branding)"/></svg>`;
  const file=path.join(dir,'issue-'+n+'.svg');fs.writeFileSync(file,svg);
  const page=await b.newPage({viewport:{width:1550,height:1014},deviceScaleFactor:n===13?2:1});
  await page.goto(pathToFileURL(path.resolve(file)).href);await page.screenshot({path:path.join(dir,name)});await page.close();console.log('Prepared issue '+n);
 }
 await b.close();
})();
