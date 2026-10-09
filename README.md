# Konstantin Tovshtein — Portfolio

Personal portfolio site for Konstantin Tovshtein, BBA student at Simon Fraser University (Management Information Systems and Accounting, minor in Computer Science).

## Development

Static HTML and SCSS, no framework. Open `index.html` in a browser to view it.

```bash
npm install
npm run watch:scss   # recompile css/style.css while editing
npm run build        # compile, autoprefix and minify css/style.css
npm run build:html   # regenerate the eight pages from tools/build_pages.py
npm run build:font   # rebuild assets/fonts/kt-sans-latin-var.woff2 (needs: pip install fonttools brotli)
```

Preview through a local server, for example `python -m http.server`, rather than opening the files directly: browsers block web fonts on `file://` pages.

Page content, the shared header and footer, and the contact form live in `tools/build_pages.py`. Edit them there; the `.html` files are generated.

Settings in that file:

- `FORMSPREE_ID`: your Formspree form ID, so the contact form can send messages.
- Drop a résumé at `assets/Konstantin-Tovshtein-Resume.pdf` and rebuild to add "Download Résumé" buttons.
- `SITE_URL`: the site's public address, used by the link-preview (`og:`) tags and canonical links. Change it if the site moves.

When a page is shared on LinkedIn, Slack or iMessage, the preview shows `assets/png/share-card.png`. It is rendered from `tools/share-card.html`; the command to re-render it is at the top of that file.

Theme colors live in `sass/abstracts/_theme.scss`. Type roles (sizes, weights, widths) live in `sass/abstracts/_type.scss`.

## Credits and license

Built on [Dopefolio](https://github.com/rammcodes/dopefolio) by Ram Maheshwari, licensed under GPL-3.0.
This version has been modified: dark theme, new typography, accessibility fixes, updated build tooling and personal content.
It is distributed under the same GPL-3.0 license; see [LICENSE](LICENSE).

The site font, KT Sans, is derived from [Mona Sans](https://github.com/github/mona-sans) by GitHub and Degarism Studio. It is subset and renamed by `tools/build_font.py`, as the SIL Open Font License 1.1 requires; see [assets/fonts/LICENSE-kt-sans.txt](assets/fonts/LICENSE-kt-sans.txt).
