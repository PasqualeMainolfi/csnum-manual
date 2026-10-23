#!/usr/bin/env python3
"""Generate the MkDocs sources in docs/ from a csound-numeric checkout.

    python3 scripts/sync.py [path/to/csound-numeric]

The source defaults to $CSNUM_SRC, then to ../csound-numeric. What it writes:

    docs/index.md            README intro (everything before the first ## heading)
    docs/guide/*.md          one page per ## section of the README
    docs/reference/index.md  doc/README.md
    docs/reference/*.md      doc/*.md, one page per opcode plus the topic pages
    docs/reference/ops-index.md  OPS_INDEX.md, opcode names linked
    docs/changelog.md        CHANGELOG.md
    nav.yml                  the site navigation, inherited by mkdocs.yml

Links are rewritten for the new layout: README anchors point into the guide
page that now holds them, GitHub-style anchors become MkDocs anchors, and links
to anything outside the documentation (example/, LICENSE, ...) go to GitHub.
Only the generated paths above are cleaned; anything else in docs/ is kept.
"""

import os
import posixpath
import re
import shutil
import sys
import unicodedata
from pathlib import Path

REPO_URL = "https://github.com/PasqualeMainolfi/csound-numeric"
BRANCH = "main"

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
GENERATED = ["index.md", "changelog.md", "guide", "reference"]

# Short file names for the README sections; a section not listed here gets
# its heading slug as file name.
GUIDE_NAMES = {
    "requirements": "requirements",
    "building": "building",
    "the-model-csnarr-values-not-csound-arrays": "model",
    "what-is-covered": "coverage",
    "numpy-correspondence": "numpy",
    "k-rate-performance-array-versioning": "k-rate",
    "real-time-paths": "real-time",
    "saving-and-loading": "saving-loading",
    "audio": "audio",
    "examples": "examples",
    "development-note": "development",
}

TOPICS = ["indexing", "set-arrays", "string-arrays"]

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LINK_RE = re.compile(r"(\]\()([^)\s]+)(\))")
WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)


def strip_md(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.replace("`", "").replace("*", "")


def gh_slug(text):
    """Anchor GitHub generates for a heading."""
    text = re.sub(r"[^\w\- ]", "", strip_md(text).strip().lower())
    return text.replace(" ", "-")


def md_slug(text):
    """Anchor Python-Markdown's toc extension generates (MkDocs default)."""
    text = unicodedata.normalize("NFKD", strip_md(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def outside_fences(lines):
    """Yield (index, line, in_fence) for each line."""
    fence = None
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            if fence is None:
                fence = m.group(1)
                yield i, line, True
                continue
            if fence == m.group(1):
                fence = None
                yield i, line, True
                continue
        yield i, line, fence is not None


def headings(lines):
    for i, line, in_fence in outside_fences(lines):
        if not in_fence:
            m = HEADING_RE.match(line)
            if m:
                yield i, len(m.group(1)), m.group(2)


class Page:
    def __init__(self, out, src, lines):
        self.out = out  # path under docs/, posix
        self.src = src  # path in the csound-numeric repo, posix
        self.lines = lines
        self.anchors = {}  # GitHub slug -> MkDocs slug
        gh_seen, md_seen = {}, {}
        for _, _, text in headings(lines):
            gh = unique(gh_slug(text), gh_seen, "-")
            self.anchors[gh] = unique(md_slug(text), md_seen, "_")


def unique(slug, seen, sep):
    n = seen.get(slug, 0)
    seen[slug] = n + 1
    return slug if n == 0 else f"{slug}{sep}{n}"


def read_lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def split_readme(src):
    """README intro -> index.md, each ## section -> guide/<name>.md."""
    lines = read_lines(src / "README.md")
    cuts = [i for i, level, _ in headings(lines) if level == 2]
    pages = [Page("index.md", "README.md", lines[: cuts[0]] if cuts else lines)]
    nav = []
    for start, end in zip(cuts, cuts[1:] + [len(lines)]):
        title = HEADING_RE.match(lines[start]).group(2)
        name = GUIDE_NAMES.get(md_slug(title), md_slug(title))
        body = lines[start:end]
        # The section heading becomes the page title: lift every heading one level.
        for i, level, text in list(headings(body)):
            body[i] = "#" * (level - 1) + " " + text
        pages.append(Page(f"guide/{name}.md", "README.md", body))
        nav.append((strip_md(title), f"guide/{name}.md"))
    # README anchors are unique across the whole file on GitHub, not per page.
    readme_anchors, gh_seen = {}, {}
    for page in pages:
        md_seen = {}
        for _, _, text in headings(page.lines):
            gh = unique(gh_slug(text), gh_seen, "-")
            readme_anchors[gh] = (page.out, unique(md_slug(text), md_seen, "_"))
    return pages, nav, readme_anchors


def reference_nav(lines):
    """Families and opcode pages from doc/README.md."""
    families, current = [], None
    item = re.compile(r"^- \[([^\]]+)\]\(([\w-]+\.md)\)")
    for i, line, in_fence in outside_fences(lines):
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 2:
            current = (strip_md(m.group(2)), [])
            families.append(current)
            continue
        m = item.match(line)
        if m and current is not None:
            current[1].append((m.group(1), f"reference/{m.group(2)}"))
    return [f for f in families if f[1]]


def linkify_ops_index(lines, opcodes):
    def repl(m):
        name = m.group(1)
        return f"- [**{name}**](doc/{name}.md)" if name in opcodes else m.group(0)

    return [re.sub(r"^- \*\*(csn\w+)\*\*", repl, line) for line in lines]


def fix_fences(lines):
    """Full .csd examples highlight with the csound-document lexer."""
    out = list(lines)
    for i, line, in_fence in outside_fences(lines):
        if line.strip() == "```csound" and i + 1 < len(lines):
            if lines[i + 1].lstrip().startswith("<CsoundSynthesizer>"):
                out[i] = line.replace("```csound", "```csound-document")
    return out


def rewrite_links(page, by_src, readme_anchors, src_root):
    def resolve(href):
        if re.match(r"^[a-z][a-z0-9+.-]*:", href):
            return href
        path, _, anchor = href.partition("#")
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page.src), path)) if path else page.src
        if target == "README.md":
            if anchor:
                if anchor not in readme_anchors:
                    warn(f"{page.src}: unknown README anchor #{anchor}")
                    out, anchor = "index.md", anchor
                else:
                    out, anchor = readme_anchors[anchor]
            else:
                out = "index.md"
        elif target in by_src:
            dest = by_src[target]
            out = dest.out
            if anchor:
                if anchor in dest.anchors:
                    anchor = dest.anchors[anchor]
                else:
                    warn(f"{page.src}: unknown anchor {target}#{anchor}")
        else:
            if not (src_root / target).exists():
                warn(f"{page.src}: link to missing {target}")
            kind = "tree" if (src_root / target).is_dir() else "blob"
            url = f"{REPO_URL}/{kind}/{BRANCH}/{target}"
            return url + (f"#{anchor}" if anchor else "")
        rel = posixpath.relpath(out, posixpath.dirname(page.out) or ".")
        if out == page.out:
            rel = ""
        return rel + (f"#{anchor}" if anchor else "")

    out = list(page.lines)
    for i, line, in_fence in outside_fences(page.lines):
        if in_fence:
            continue
        # Leave inline code alone: rewrite only the text between backtick spans.
        parts = re.split(r"(`[^`]*`)", line)
        for j in range(0, len(parts), 2):
            parts[j] = LINK_RE.sub(lambda m: m.group(1) + resolve(m.group(2)) + m.group(3), parts[j])
        out[i] = "".join(parts)
    page.lines = out


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_nav(guide_nav, families, orphans):
    out = ["# Generated by scripts/sync.py: do not edit.", "nav:", "  - Home: index.md", "  - Guide:"]
    out += [f"      - {yaml_str(t)}: {p}" for t, p in guide_nav]
    out += [
        "  - Reference:",
        "      - reference/index.md",
        "      - Opcode index: reference/ops-index.md",
        "      - Topics:",
    ]
    out += [f"          - reference/{t}.md" for t in TOPICS]
    for family, items in families:
        out.append(f"      - {yaml_str(family)}:")
        out += [f"          - {yaml_str(name)}: {path}" for name, path in items]
    if orphans:
        out.append("      - Other:")
        out += [f"          - {yaml_str(Path(p).stem)}: {p}" for p in orphans]
    out.append("  - Changelog: changelog.md")
    (ROOT / "nav.yml").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CSNUM_SRC", str(ROOT.parent / "csound-numeric"))
    src = Path(arg).resolve()
    if not (src / "README.md").is_file() or not (src / "doc").is_dir():
        sys.exit(f"sync: {src} does not look like a csound-numeric checkout")

    readme_pages, guide_nav, readme_anchors = split_readme(src)
    pages = list(readme_pages)

    doc_files = sorted((src / "doc").glob("*.md"))
    opcodes = {p.stem for p in doc_files if p.stem != "README"}
    for p in doc_files:
        out = "reference/index.md" if p.stem == "README" else f"reference/{p.name}"
        pages.append(Page(out, f"doc/{p.name}", read_lines(p)))
    pages.append(Page("reference/ops-index.md", "OPS_INDEX.md", linkify_ops_index(read_lines(src / "OPS_INDEX.md"), opcodes)))
    if (src / "CHANGELOG.md").is_file():
        pages.append(Page("changelog.md", "CHANGELOG.md", read_lines(src / "CHANGELOG.md")))

    by_src = {p.src: p for p in pages if p.src != "README.md"}
    for page in pages:
        rewrite_links(page, by_src, readme_anchors, src)
        page.lines = fix_fences(page.lines)

    families = reference_nav(read_lines(src / "doc" / "README.md"))
    in_nav = {path for _, items in families for _, path in items}
    in_nav |= {f"reference/{t}.md" for t in TOPICS} | {"reference/index.md"}
    orphans = sorted(f"reference/{p.name}" for p in doc_files if p.stem != "README" and f"reference/{p.name}" not in in_nav)
    for o in orphans:
        warn(f"{o} is not listed in doc/README.md; put under Reference > Other")

    for name in GENERATED:
        target = DOCS / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    for page in pages:
        dest = DOCS / page.out
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("\n".join(page.lines).rstrip("\n") + "\n", encoding="utf-8")
    write_nav(guide_nav, families, orphans)

    print(f"sync: {len(pages)} pages from {src}")
    for w in WARNINGS:
        print(f"warning: {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
