# Issue update workflow

Whenever the user asks to add a PACIFIC issue, complete all three updates by default:

1. Add the issue to DATA in issue.html, regenerate standalone issue pages and archive links with node scripts/generate-issues.cjs, update archive introductory copy, and feature the latest issue on both desktop and mobile homepages.
2. Extract the featured photo from the supplied issue (or use a supplied original) and add it to photos.html with its caption and issue number. Preserve the original issue image.
3. Update stats.html with the published season totals and a new series row. Attribute the source; flag inconsistent printed rates rather than silently changing them. Do not invent unreported statistics or expose unpublished future games.

Check local links/assets and generated navigation before delivery. Do not hand-edit generated issue-N.html files.
