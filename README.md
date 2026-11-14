# novila.app

The website for Novila: the home page, questions and answers, the privacy policy and the terms of use, in English
and Swedish. It lives
here, in its own repository, because the app repository (`joeldenke/Novila`) is private.

```sh
python3 tools/site/build_site.py   # builds build/site, standard library only
```

`Website` (`.github/workflows/pages.yml`) builds the site on every pull request and publishes it with GitHub Pages
on a merge to `main`. The custom domain and HTTPS are set under Settings → Pages (source: GitHub Actions), not in a
`CNAME` file.

## Nordic light

The site looks like the app: Nordic light (`docs/design/nordic-light-2026-11.md` in the app repository), a dark ink
ground with the app's lights drawn as radial gradients, cream text, glass cards and one cream stone for the main
action. The start page's light and the horizon under its title follow the visitor's hour (a small script in
`site/layout.html` that stores and sends nothing; dusk without it). Every picture on the site is one of the app's own
screens; there are no painted scenes or stock photos.

## Copied from the app

The site shows the app as it is, so some files are copies from `joeldenke/Novila`, at the same paths, so the
builder is the same script in both repositories:

- `site/`, `tools/site/build_site.py` – the pages and the builder

The questions and answers (`site/faq.*.html`, at `/faq/` and `/sv/fragor/`) are the site's own, not a copy. Each
answer is a `<section class="faq-item" id="…">` with an `<h3>` and a `<div class="faq-answer">`; the builder turns
them into FAQPage structured data and fails on one it can't read. The ids are linked from the home page, so keep them.
When the app changes something an answer describes (a setting's name, what Health Connect reads, the price), change
the answer in the same pull request as the copied files.
- `docs/privacy-policy.md`, `docs/terms-of-use.md` – the policy and the terms (the app links to novila.app)
- `docs/play-icon.png` – the icon
- `core/designsystem/src/main/res/font/hanken_grotesk_*.ttf` (all text) and
  `bricolage_grotesque_{light,medium,semibold}.ttf` (the h1 and h2 headings, as titles in the app), with their
  licences in `core/designsystem/src/main/assets`
- `site/screens/*.webp` – the app's screens the phones, the tablet, the foldable and the widget show. Not copied as
  they are: `python3 tools/site/screens.py ../Novila` (needs Pillow) cuts each screenshot reference to what the
  device shows, scales it to twice the size the page sets it at and saves it as WebP (`SCREENS` in the script)

When one of them changes in the app, copy it here in a pull request. The page addresses (`PAGES` in the builder) are
public and in Play Console; never move one.
