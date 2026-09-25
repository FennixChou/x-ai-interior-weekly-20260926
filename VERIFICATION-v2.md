# v2 verification

- 14 unique X status URLs, 9 author accounts; all dates within 2026-09-21 00:00 to 2026-09-26 03:55 Asia/Taipei.
- Primary posts read in authenticated X browser. CAD publisher table and methodology read separately. No downloaded CAD/model artifact was reproduced.
- Existing root index.html unchanged; v2 added separately.
- JSON parsing, JavaScript syntax, generated HTML, local server and source anchor checks passed.
- Browser category counts: CAD 3, SketchUp 4, interior modeling 7, style image generation 1, rendering 5; all 14. Categories overlap.
- Search Astra: 5. No-match message passed. Real keyboard clear restored correct counts. Browser automation fill with an empty string did not clear the DOM field; this was an automation issue, not an application defect.
- Reload: 14 case cards, 14 primary X links, zero broken internal anchors, zero captured console errors.
- Desktop screenshot review: title, overview, table and case cards readable; no overlap or broken images. Report contains no embedded third-party images.
- Mobile viewport 390x844: document width 375 (scrollbar excluded), no page overflow; filtering/search passed. Mobile screenshot capture timed out twice; alternate non-surface capture was unsupported. Mobile visual review is incomplete; no full visual PASS claimed. Viewport restored.
- Content review clarified CAD scores as points, not success percentages, and limited improvement claims. Third-party performance, costs and editability remain attributed claims.

Publication requires a successful Pages build and byte-level comparison of live v2 assets with local files. Final deployment evidence is recorded separately in the workspace after publishing.
