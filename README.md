# novila.app

The website for Novila: the home page, the privacy policy and the terms of use, in English and Swedish. It lives
here, in its own repository, because the app repository (`joeldenke/Novila`) is private.

```sh
python3 tools/site/build_site.py   # builds build/site, standard library only
```

`Website` (`.github/workflows/pages.yml`) builds the site on every pull request and publishes it with GitHub Pages
on a merge to `main`. The custom domain and HTTPS are set under Settings → Pages (source: GitHub Actions), not in a
`CNAME` file.

## Copied from the app

The site shows the app as it is, so some files are copies from `joeldenke/Novila`, at the same paths, so the
builder is the same script in both repositories:

- `site/`, `tools/site/build_site.py` – the pages and the builder
- `docs/privacy-policy.md`, `docs/terms-of-use.md` – the policy and the terms (the app links to novila.app)
- `docs/play-icon.png` – the icon
- `core/designsystem/src/main/res/font/hanken_grotesk_*.ttf` and its licence in `core/designsystem/src/main/assets`
- `feature/*/src/test/screenshots/…` – the app's screenshot references the phones, the tablet and the foldable show
  (`SCREENS` in the builder)

When one of them changes in the app, copy it here in a pull request. The page addresses (`PAGES` in the builder) are
public and in Play Console; never move one.
