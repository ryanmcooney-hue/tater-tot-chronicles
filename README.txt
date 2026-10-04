FINAL SITE FIX PACKAGE

Replace the included HTML files in the root of your tater-tot-chronicles repository.
Copy the included files from assets/ into your existing assets/ folder; do not delete your existing assets.

This package includes the final QA fixes plus two homepage interaction fixes:
- Browse the PACIFIC archive now opens archive.html.
- April and May homepage recap graphics now open their full-size PNG versions in a new tab.

Then commit to main, push origin, wait for GitHub Pages to deploy, and Ctrl+F5.

STANDALONE PACIFIC ISSUE PAGES

DATA in issue.html is the source for every issue. That file also supplies the
shared layout. Generated pages use styles.css without design changes.

When adding Issue 14, 15, etc.:
1. Add the new numbered entry to DATA in issue.html with n, title, month, level,
   series and note, following the existing entries.
2. Add its PACIFIC image to assets/. Default: assets/18Issue14.png for Issue 14,
   assets/19Issue15.png for Issue 15, etc. For another filename, add
   "image": "assets/your-filename.png" to the entry.
3. Optional: add "socialImage": "assets/your-preview-photo.png" to the entry.
   Without socialImage, its PACIFIC image is used for Facebook and Twitter.
   Issue 13 explicitly uses assets/photo-issue-13.png.
4. From the repository root, run: node scripts/generate-issues.cjs
   Requires Node.js; no npm packages. This generates all issue-N.html pages,
   refreshes Previous/Next links, and adds new archive cards automatically.
5. Review the files, then include issue.html, archive.html, generated pages and
   new assets when committing/publishing. Update archive introductory copy if
   desired; the generator preserves that existing editorial text.

Do not hand-edit issue-N.html; regeneration replaces them. For layout changes,
edit issue.html and regenerate. Old issue.html?issue=N links remain functional.
Share issue-N.html for static social previews.

DEFAULT FOR EVERY NEW ISSUE

Also update both homepage latest-issue features, add the featured photo and caption
to photos.html, and update stats.html season totals plus the new series row.
All three updates are required whenever an issue is requested. See AGENTS.md.
