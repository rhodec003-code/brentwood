#!/usr/bin/env python3
"""Inject Open Graph and Twitter Card metadata into static HTML pages."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://www.brentwoodorganizers.com"
SOCIAL_IMAGE = f"{SITE_URL}/social-preview.jpg"
IMAGE_ALT = "An organized luxury living space by Brentwood Organizers"


SOCIAL_META_RE = re.compile(
    r"^[ \t]*<meta\s+(?:property|name)=\"(?:og:|twitter:)[^>]*>\n?",
    re.MULTILINE,
)


def first_match(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return default
    return html.unescape(match.group(1).strip())


def canonical_for(path: Path, text: str) -> str:
    canonical = first_match(
        r'<link\s+rel="canonical"\s+href="([^"]+)"',
        text,
    )
    if canonical:
        return canonical.replace("https://brentwoodorganizers.com", SITE_URL)

    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return SITE_URL
    if rel.endswith("/index.html"):
        return f"{SITE_URL}/{rel[:-10]}/"
    return f"{SITE_URL}/{rel}"


def page_type(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    is_blog_post = "/blog/" in rel or rel.startswith("blog/")
    is_blog_index = rel.endswith("blog/index.html") or rel == "blog/index.html"
    return "article" if is_blog_post and not is_blog_index else "website"


def locale_for(text: str) -> str:
    lang = first_match(r'<html\s+lang="([^"]+)"', text, "en").lower()
    if lang.startswith("es"):
        return "es_ES"
    if lang.startswith("fr"):
        return "fr_FR"
    if lang.startswith("pt"):
        return "pt_BR"
    return "en_US"


def social_block(path: Path, text: str) -> str:
    title = first_match(r"<title>(.*?)</title>", text, "Brentwood Organizers")
    description = first_match(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        text,
        "White-glove home organization, move-in support, and estate transition services in Miami.",
    )
    url = canonical_for(path, text)
    escaped = {
        "title": html.escape(title, quote=True),
        "description": html.escape(description, quote=True),
        "url": html.escape(url, quote=True),
        "image": html.escape(SOCIAL_IMAGE, quote=True),
        "alt": html.escape(IMAGE_ALT, quote=True),
        "locale": locale_for(text),
        "type": page_type(path),
    }
    return f"""    <meta property="og:type" content="{escaped['type']}">
    <meta property="og:site_name" content="Brentwood Organizers">
    <meta property="og:locale" content="{escaped['locale']}">
    <meta property="og:title" content="{escaped['title']}">
    <meta property="og:description" content="{escaped['description']}">
    <meta property="og:url" content="{escaped['url']}">
    <meta property="og:image" content="{escaped['image']}">
    <meta property="og:image:secure_url" content="{escaped['image']}">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{escaped['alt']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escaped['title']}">
    <meta name="twitter:description" content="{escaped['description']}">
    <meta name="twitter:image" content="{escaped['image']}">
    <meta name="twitter:image:alt" content="{escaped['alt']}">
"""


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = SOCIAL_META_RE.sub("", text)
    block = social_block(path, updated)

    description_re = re.compile(
        r'([ \t]*<meta\s+name="description"\s+content="[^"]*">\n?)',
        re.IGNORECASE,
    )
    if description_re.search(updated):
        updated = description_re.sub(r"\1" + block, updated, count=1)
    else:
        updated = updated.replace("<head>\n", "<head>\n" + block, 1)

    if updated == text:
        return False

    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if inject(path):
            changed += 1
    print(f"Updated {changed} HTML files.")


if __name__ == "__main__":
    main()
