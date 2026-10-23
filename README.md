# csnum manual

Source of the [csnum manual](https://pasqualemainolfi.github.io/csnum-manual/),
the documentation site of [csound-numeric](https://github.com/PasqualeMainolfi/csound-numeric),
built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

The pages are not written here: `scripts/sync.py` generates `docs/` and `nav.yml`
from a csound-numeric checkout (the README split into guide pages, `doc/*.md` as
the reference, `OPS_INDEX.md`, `CHANGELOG.md`). Edit the documentation in
csound-numeric, then sync.

## Updating

```sh
python3 scripts/sync.py              # source: $CSNUM_SRC, else ../csound-numeric
python3 scripts/sync.py /path/to/csound-numeric
```

Commit `docs/` and `nav.yml`; a push to `main` builds the site and publishes it
to GitHub Pages (`.github/workflows/deploy.yml`).

## Preview

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve               # http://127.0.0.1:8000
.venv/bin/mkdocs build --strict      # what CI runs
```

`mkdocs.yml` holds the site configuration and inherits the navigation from the
generated `nav.yml`. Anything placed in `docs/` outside `index.md`,
`changelog.md`, `guide/` and `reference/` is left alone by the sync.
