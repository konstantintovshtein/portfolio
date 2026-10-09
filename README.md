# Konstantin Tovshtein — Portfolio

Personal portfolio site for Konstantin Tovshtein, BBA student at Simon Fraser University (Management Information Systems and Accounting, minor in Computer Science).

## Development

Static HTML and SCSS, no framework. Open `index.html` in a browser to view it.

```bash
npm install
npm run watch:scss   # recompile css/style.css while editing
npm run build        # compile, autoprefix and minify css/style.css
npm run build:html   # regenerate the eight pages from tools/build_pages.py
```

Page content, the shared header and footer, and the contact form live in `tools/build_pages.py`. Edit them there; the `.html` files are generated.

Two settings in that file:

- `FORMSPREE_ID`: your Formspree form ID, so the contact form can send messages.
- Drop a résumé at `assets/Konstantin-Tovshtein-Resume.pdf` and rebuild to add "Download Résumé" buttons.

Theme colors and fonts live in `sass/abstracts/_theme.scss`.

## Credits and license

Built on [Dopefolio](https://github.com/rammcodes/dopefolio) by Ram Maheshwari, licensed under GPL-3.0.
This version has been modified: dark theme, new typography, accessibility fixes, updated build tooling and personal content.
It is distributed under the same GPL-3.0 license; see [LICENSE](LICENSE).
