const { chromium } = require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 900 });
    for (const path of ['features.html', 'call-up.html', 'index.html']) {
      await page.goto(require('node:url').pathToFileURL(require('node:path').resolve(path)).href);
      await page.screenshot({ path: 'outputs/' + path.replace('.html', '') + '-' + width + '.png' });
      const result = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth > innerWidth,
        brokenImages: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src)
      }));
      console.log(path, width, result);
      if (result.overflow || result.brokenImages.length) errors.push(path + ' layout/assets');
    }
  }
  console.log('Errors:', errors);
  await browser.close();
  if (errors.length) process.exitCode = 1;
})().catch(e => { console.error(e); process.exit(1); });
