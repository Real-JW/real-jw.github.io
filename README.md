# Jiawen Wu's personal website

GitHub Pages serves the generated HTML files at the repository root. Every page
contains its navigation and content before JavaScript runs, including the homepage
biography, education, and publications. The existing card layout, colors,
responsive typography, dark mode, and logo interaction are retained.

## Edit and build

Python 3.9+ is the only build dependency. Run from this repository:

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 scripts/check_site.py
```

Commit the generated root HTML files, `sitemap.xml`, and `robots.txt` together with
source changes before deploying. The GitHub Actions check rejects stale output
and validates the public pages. Existing GitHub Pages hosting can continue to
publish the repository root; no hosting migration or JavaScript runtime is needed.

| Source | Purpose |
| --- | --- |
| `data/profile.json` | Biography, research interests, education, public profiles, and last-updated date |
| `data/publications.json` | Publication titles, authors, venues, and links |
| `data/blog.json` | Research news and projects |
| `data/site.json` | Site URL, unique page titles/descriptions, Google verification filename or optional HTML-tag token |
| `_templates/*.html` | Page layouts; edit these instead of the generated root HTML files |
| `includes/*.html` | Shared component templates and SEO metadata |
| `assets/css/` | Existing visual styling |
| `assets/js/` | Dark-mode and logo interactions; content does not depend on these |

Set `profile.json`'s `lastUpdated` when editing the profile. News dates render in
English without browser timezone shifts. Items with no destination URL render as
text instead of links that reload the current page. The build escapes content and
checks link protocols before inserting it into HTML.

The Jekyll configuration excludes build sources from the published site. The
sitemap lists only the five public pages, using `/` as the homepage canonical.
The generated crawler rules permit all crawlers, including AI search and training
crawlers, and allow CSS, JavaScript, images, and public PDFs. Crawler permission is
not a guarantee of indexing, rankings, or inclusion in AI answers.

## Google Search Console

Ownership and indexing must be verified against the deployed site using your
Google account; local checks cannot confirm Google's index.

1. Open [Google Search Console](https://search.google.com/search-console) and add
   the URL-prefix property `https://real-jw.github.io/`.
2. Choose **HTML file** verification. The supplied file is already stored in
   `data/googlec205ab2e97d1722b.html`, and `googleSiteVerificationFile` in
   `data/site.json` tells the build to copy it unchanged to the site root.
   HTML-tag verification is also supported through `googleSiteVerification`.
3. Rebuild and deploy the site through your normal GitHub Pages process. Check
   `https://real-jw.github.io/googlec205ab2e97d1722b.html`, then return to Search
   Console and click **Verify**. Keep this file deployed after verification.
4. Submit `sitemap.xml` in **Sitemaps**.
5. Use **URL Inspection** on the homepage and the other four pages. Run **Test
   live URL**, review the retrieved HTML, and request indexing where appropriate.
6. Monitor indexing and search impressions for your name, ZKP hardware, hardware
   security, and LLM agents for EDA.

Validate the deployed profile markup with Google's
[Rich Results Test](https://search.google.com/test/rich-results).

Google's instructions:
[ownership verification](https://support.google.com/webmasters/answer/9008080),
[URL inspection](https://support.google.com/webmasters/answer/9012289), and
[sitemap submission](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
