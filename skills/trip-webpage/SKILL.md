---
name: trip-webpage
description: >-
  Generate a mobile-first interactive travel guide webpage from itinerary documents or structured notes, including PDF, Word, Markdown, text, CSV, TSV, and Excel inputs. Use when Codex needs to turn trip plans, route documents, travel spreadsheets, or day-by-day itineraries into a standalone HTML攻略网页 with the same visual style and interactions as the bundled reference page, including full-bleed hero, sticky navigation, Leaflet route map, day cards, spot detail sheet, rating panel, lodging shortlist cards, food cards, and prep checklist.
---

# Trip Webpage

Use this skill to convert travel itinerary materials into a standalone Chinese travel guide webpage, or to update an already-built trip webpage so missing template features become active. Keep the output visually consistent with `assets/trip-template.html`; the template came from the “塔州东海岸 6 日游” page and is the style source of truth.

## New Page Workflow

1. Collect source material.
   - Accept `.pdf`, `.docx`, `.md`, `.txt`, `.csv`, `.tsv`, `.xlsx`, and `.xlsm`.
   - If the user provides multiple files, extract them all and merge the useful itinerary facts.
   - Run `scripts/extract_trip_text.py <input...> --output <workdir>/trip-source.txt` when file extraction is needed.
   - If the source files may contain useful images, add `--media-dir <trip-folder>/assets --media-path-prefix assets`. Extracted document images must live in the trip page’s own `assets/` folder, not in a temporary folder.

2. Convert the source into `trip-data.json`.
   - Follow `references/trip-data-schema.md`.
   - Preserve confirmed dates, flights, hotels, bookings, and warnings exactly.
   - If a spot description is missing from the document, search Wikipedia for that spot and summarize the useful intro into Chinese.
   - If the document does not provide daily sunrise/sunset times, set `page.timeZone` and make sure each `days[]` item has `date`, `lat`, and `lng`; then run `scripts/enrich_sun_times.py trip-data.json --tzid <IANA timezone>`.
   - Keep Chinese as the primary narrative language. For foreign attractions, always keep the English official/common name in `name` and the Chinese translation in `zh`; the page will display them as `English｜中文`.
   - Use the same page sections as the template: route map, daily plan, lodging shortlist when accommodation candidates exist, food/supply, preparation.
   - In each daily timeline, render one scenic spot per row. Use `English｜中文` for foreign scenic spots in the row text, and do not combine multiple spots into one timeline item such as `A / B / C 选 1-2 个`; split them into separate rows or make the non-selected alternatives plain notes.

3. Add coordinates and images.
   - Every map spot must have `lat` and `lng`.
   - Prefer confirmed coordinates from the source, existing knowledge, or explicit user-provided places.
   - Image priority is strict: use images extracted from/provided by the document first; if no suitable document image exists, search the web for relevant images or short local video clips, download them into `<trip-folder>/assets/`, and point `spot.image` plus optional `spot.images[]` entries to local `assets/...` paths.
   - Use `spot.image` as the primary/fallback cover image. When multiple good images or videos exist for one spot, also add `spot.images` as an ordered media carousel list. Each entry may be a string path or an object such as `{ "src": "assets/spot_1.jpg", "caption": "..." }`; video entries may use `{ "src": "assets/spot_clip.mp4", "type": "video", "poster": "assets/spot_cover.jpg", "caption": "..." }`.
   - When using document-extracted images, put every selected image into `<trip-folder>/assets/`, set `spot.image` to the first extracted `assets/...` path, add additional extracted images to `spot.images`, set `imageSourceType` to `document`, and keep `photoCredit` as `用户提供/文档内图片` unless the document states a more specific credit.
   - If a spot intro or image is missing, use `scripts/enrich_from_wikipedia.py trip-data.json` as a first pass, then review and translate/adjust the intro for the page tone.
   - Run `scripts/localize_trip_images.py trip-data.json --assets-dir <trip-folder>/assets` before final render so remote hero media and spot media become local files.
   - For lodging cards, fetch one clear cover image per property. If the user provides a local image, copy it into `<trip-folder>/assets/`; if the user provides a Booking/Airbnb/hotel page or wishlist, open each property page with the available browser/session, use the visible lead/gallery image as the card cover, download it into `<trip-folder>/assets/`, and set `staySections[].cards[].image`. Prefer the property’s own page image over generic city photos.
   - Put lodging card images in `<trip-folder>/assets/` and reference them from `staySections[].cards[].image`. Record `imageCaption` such as `图片：Booking` or `图片：Airbnb`, and keep `imageSource` when the source URL is known. If the user needs to upload a single HTML file where local assets may be lost, set `page.embedStayImages: true` or render with `--embed-stay-images`.
   - Keep image source and credit fields in every spot, especially when downloading from Wikipedia/Wikimedia or another public page.

4. Render the webpage.
   - Run `scripts/render_trip_webpage.py trip-data.json --output <trip-folder>/index.html`.
   - For single-file upload destinations such as Yuque, run `scripts/render_trip_webpage.py trip-data.json --output <trip-folder>/index.html --embed-stay-images` so lodging card images are embedded in the HTML.
   - Put local images in `<trip-folder>/assets/`.
   - If `enrich_sun_times.py` was used, keep the generated footer attribution to Sunrise-Sunset.org.
   - Name the folder with a readable slug and dates, for example `new-zealand-south-20261103-1114`.

5. Validate the output.
   - Open or inspect the generated HTML.
   - Check that `const spots`, `const days`, `const foods`, and `const prep` are populated.
   - Check that the title, hero, nav, map panel, daily cards, lodging cards when present, food cards, and prep cards still use the bundled template classes.
   - If the page is added to this workspace, update the root `index.html` and `vercel.json` only when the user wants it listed or routed.

## Existing Page Workflow

Use this path when the user provides an already-built trip webpage or asks to make a feature take effect on the current page.

1. Inspect the target HTML and preserve its trip data.
   - Do not regenerate the whole page unless the user explicitly asks.
   - Do not overwrite itinerary arrays, local assets, route details, or manually edited copy.
   - Run `scripts/audit_trip_webpage.py <trip-folder>/index.html` to identify missing known template features.

2. Compare the target page with `assets/trip-template.html`.
   - Copy only the CSS, HTML shell, and JS functions needed for the missing feature.
   - Keep the target page’s existing `spots`, `days`, `foods`, `prep`, `hotels`, `staySections`, `route`, `routeSegments`, and `spotInsights` data.
   - When a feature needs event handlers, verify both desktop and mobile paths.

3. Make the feature active in the current page.
   - Patch the actual page file, not only the template, when the user asks about the current webpage.
   - Also patch `assets/trip-template.html` when the feature should be available for future generated pages.
   - For image-related features, confirm both `.panel-img` and `.rating-image` paths work.
   - For Yuque or any single-HTML upload target, lodging card images must be embedded inside the HTML. On existing pages, run `scripts/embed_stay_images_in_html.py <trip-folder>/index.html` after adding local `assets/stay-*` images, then verify no `staySections[].cards[].image` value still points to `assets/stay-*`.

4. Verify the existing page after patching.
   - Re-run `scripts/audit_trip_webpage.py <trip-folder>/index.html`.
   - Extract the page script and run `node --check` when JavaScript changed.
   - If the page will be uploaded as one HTML file, confirm `staySections` uses `data:image/...;base64,...` for every lodging image and there are zero remaining `"image": "assets/stay-...` references.
   - If possible, open or screenshot the page to confirm the feature is visible and interactive.

## Style Rules

- Keep the original template’s warm paper background, green/blue/orange palette, 8px radius, full-bleed hero media layer, sticky desktop nav, mobile bottom nav, map/detail split layout, and mobile bottom sheet.
- Keep hero media driven by `page.heroImage`: image paths render as `<img>`, while `.mp4`, `.webm`, `.mov`, and `.m4v` paths render as muted autoplay looping video. Use `page.heroPoster` when a hero video needs a poster frame.
- Keep the built-in image lightbox behavior: spot detail images and rating-panel images are clickable and keyboard-accessible for enlarged preview.
- Keep the built-in spot media carousel behavior: when `spot.images` contains multiple entries, the detail panel and enlarged lightbox both show left/right controls, dots, touch swipe, keyboard arrows, synchronized active media state, and mixed image/video playback.
- Do not replace the template with a generic report page or landing page.
- Do not introduce a new framework.
- Keep cards compact and itinerary-focused.
- Keep lodging cards operational and comparable. Use the same detail labels across candidates where possible: `房型 / 床型`, `取消 / 付款`, `早餐 / 洗衣`, `停车`, `入住 / 离店`, and `机场班车`.
- Use `Day 0` only for arrival evening or pre-trip staging; otherwise start at `Day 1`.
- Put urgent operational notes in `notice`, day `alerts`, or prep groups.

## Data Authoring Rules

- Create a spot for each meaningful map/timeline place, not for every meal or generic drive segment.
- For foreign spots, set `name` to the English official/common name and `zh` to the Chinese name. Do not put only the Chinese name in `name`.
- For China/domestic Chinese spots, `name` may be Chinese and `zh` can be omitted unless an English display name is useful.
- Make `id` values lowercase ASCII with underscores.
- Keep timeline items as `[time, text, optionalSpotId]`.
- Make every timeline `optionalSpotId` match a real `spots[].id`.
- Put at most one scenic spot ID in each timeline row. If the day visits three spots, write three timeline rows.
- If a timeline row references a foreign spot, write the display text as `English｜中文` and bind the matching spot ID.
- Keep `route` as the ordered travel path through spot IDs.
- Use `routeSegments` to distinguish `drive`, `ferry`, `walk`, or `flight` legs when known.
- Include `hotels` for lodging areas, even if the exact hotel is unknown.
- Use `staySections` when the page should compare concrete accommodation candidates. Put one section per overnight city/area, use one card per property, and keep user-confirmed bookings marked with `selected: true` plus a `confirmed` tag.
- For airport shuttle details in `staySections[].cards[].details`, write either `无班车。` or split service by direction: `接机服务：价格 + 时间` and `送机服务：价格 + 时间`. Include currency such as `AUD`.
- Put area-level transport fallbacks, such as “Mascot 附近可坐 420 公交往返机场”, in `staySections[].notices` instead of repeating them in every lodging card.
- Use local lodging images in `staySections[].cards[].image`; embed them with `page.embedStayImages: true` or `--embed-stay-images` when the final HTML must survive single-file uploads.
- For existing pages headed to Yuque, do not stop at local files in `assets/`; convert lodging image paths to data URIs in the HTML itself. Local assets alone will not display after a single-file upload.
- When collecting lodging images from booking platforms, use the property detail page’s lead/gallery photo, save it under a descriptive `assets/stay-...` filename, and avoid unrelated destination or stock-like images. If the visible image cannot be downloaded directly, use the browser/page asset export path available in the current environment, then point `staySections[].cards[].image` at the saved file.
- Use `spotInsights` to add “景观特色” and “背景 / 历史” cards for important spots.
- Track downloaded or extracted image provenance with `imageSourceType`, `photoSource`, and `photoCredit`.

## Bundled Resources

- `assets/trip-template.html`: the locked visual and interaction template.
- `references/trip-data-schema.md`: JSON shape expected by the renderer.
- `scripts/extract_trip_text.py`: extracts text and optional embedded images from itinerary source files into the trip page’s `assets/` folder.
- `scripts/enrich_from_wikipedia.py`: fills missing spot introductions and missing image URLs from Wikipedia.
- `scripts/enrich_sun_times.py`: fills missing `days[].sunrise` and `days[].sunset` using date, day coordinates, and an IANA timezone.
- `scripts/localize_trip_images.py`: downloads remote hero media, spot media, and lodging card images into local assets and rewrites JSON paths.
- `scripts/embed_stay_images_in_html.py`: embeds existing-page lodging card images from `assets/stay-*` into the HTML as data URIs for Yuque or other single-file uploads.
- `scripts/render_trip_webpage.py`: injects `trip-data.json` into the template and writes `index.html`.
- `scripts/audit_trip_webpage.py`: checks an existing HTML page for known template features that may be missing.
