# Issue update workflow

Whenever the user asks to add a PACIFIC issue, complete all three updates by default:

1. Add the issue to DATA in issue.html, regenerate standalone issue pages and archive links with node scripts/generate-issues.cjs, update archive introductory copy, and feature the latest issue on both desktop and mobile homepages.
2. Extract the featured photo from the supplied issue (or use a supplied original) and add it to photos.html with its caption and issue number. Preserve the original issue image.
3. Update stats.html with the published season totals and a new series row. Attribute the source; flag inconsistent printed rates rather than silently changing them. Do not invent unreported statistics or expose unpublished future games.

Check local links/assets and generated navigation before delivery. Do not hand-edit generated issue-N.html files.

Explicit user exceptions override this default. Issue 16 covers the Futures Game: add its issue and gallery photo, but do not add its exhibition results to stats.html or season totals.

# Approved visual style

For all future Tater Tot Chronicles image generation and animation work, use `assets/tater-family-mariners-postgame-v2.png` as the approved visual style reference. The user explicitly approved and locked this style. Use it as an image reference when generating new artwork, not just a written description.

Match its realistic 3D baseball video-game/cutscene rendering: modeled characters, rendered skin and hair, textured clothing, and game-engine lighting. Apply this style consistently to every person and the environment. Preserve the approved image's level of realism; do not drift into live-action photography, painterly illustration, or exaggerated cartoon styling. The earlier `tater-family-mariners-postgame.png` is not the approved style reference.

Preserve Tater's character design: an adult 5 feet 1 inch tall and 201 pounds, with a short, broad, stocky build, broad chest, thick waist, powerful compact arms and legs, reddish curly hair, prominent broad reddish-brown mutton chops, a separate mustache, and a clean-shaven chin. These canonical measurements were corrected by the user on October 30, 2026. Show his noticeably short stature relative to other adults without shrinking his head or distorting anatomy. Use the gameplay references for additional character details and preserve established family identities. Clothing, setting, composition, and poses may change with the requested scene; the approved rendering style and character identity remain consistent unless the user explicitly changes them.
