#!/usr/bin/env python3
"""Generate bilingual sitemap.xml for brentwoodorganizers.com.

Usage:
    python3 scripts/generate_sitemap.py

Outputs sitemap.xml to the project root with English and Spanish URLs,
including hreflang alternate tags for each entry.
"""

import os
from datetime import datetime, timezone

DOMAIN = "https://brentwoodorganizers.com"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGE_FREQ_DEFAULT = "monthly"
PRIORITY_HOME = "1.0"
PRIORITY_SERVICE = "0.9"
PRIORITY_LOCATION = "0.8"
PRIORITY_BLOG_INDEX = "0.8"
PRIORITY_BLOG_POST = "0.7"
PRIORITY_OTHER = "0.6"

# Pages that should be excluded from the sitemap
EXCLUDED = {
    "faqs.html",  # faqs/index.html is the canonical version at /faqs
}

# Paths to skip (duplicates of canonical URLs)
EXCLUDED_PATHS = {
    "blog/home-organization-tips/how-to-organize-before-the-holidays/index.html",
}


def file_to_url(filepath: str) -> str:
    """Convert a file path relative to project root to a URL path."""
    rel = filepath
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("/index.html")]
    elif rel.endswith(".html"):
        return "/" + rel
    return "/" + rel


def get_priority(filepath: str) -> str:
    """Assign priority based on page type."""
    if filepath == "index.html":
        return PRIORITY_HOME
    elif filepath in ("services.html", "consultation.html", "locations.html"):
        return PRIORITY_SERVICE
    elif filepath == "blog/index.html":
        return PRIORITY_BLOG_INDEX
    elif filepath.startswith("blog/"):
        return PRIORITY_BLOG_POST
    elif filepath.startswith("faqs/"):
        return PRIORITY_OTHER
    elif filepath.endswith(".html"):
        base = os.path.basename(filepath)
        if base in ("luxury-move-in.html", "home-organization.html",
                     "estate-transitions.html", "blogs.html"):
            return PRIORITY_SERVICE
        return PRIORITY_LOCATION
    return PRIORITY_OTHER


def collect_pages() -> list[tuple[str, str, str]]:
    """Return list of (loc, lastmod, priority) tuples for English pages only."""
    pages = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip hidden dirs, es/ directory, and node_modules etc.
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "es"]

        for fname in files:
            if not fname.endswith(".html"):
                continue

            full = os.path.join(root, fname)
            rel = os.path.relpath(full, PROJECT_ROOT)

            if fname in EXCLUDED or rel in EXCLUDED_PATHS:
                continue

            url = file_to_url(rel)
            priority = get_priority(rel)
            pages.append((DOMAIN + url, now, priority))

    priority_order = {
        PRIORITY_HOME: 0, PRIORITY_SERVICE: 1, PRIORITY_LOCATION: 2,
        PRIORITY_BLOG_INDEX: 3, PRIORITY_BLOG_POST: 4, PRIORITY_OTHER: 5,
    }
    pages.sort(key=lambda p: (priority_order.get(p[2], 99), p[0]))
    return pages


def generate_sitemap(pages: list[tuple[str, str, str]]) -> str:
    """Generate sitemap XML with hreflang alternates for EN/ES."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
    )

    for en_loc, lastmod, priority in pages:
        es_loc = en_loc.replace(DOMAIN, DOMAIN + "/es")

        # English entry
        lines.append("  <url>")
        lines.append(f"    <loc>{en_loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{CHANGE_FREQ_DEFAULT}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="es" href="{es_loc}"/>'
        )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en_loc}"/>'
        )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en_loc}"/>'
        )
        lines.append("  </url>")

        # Spanish entry
        lines.append("  <url>")
        lines.append(f"    <loc>{es_loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{CHANGE_FREQ_DEFAULT}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en_loc}"/>'
        )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="es" href="{es_loc}"/>'
        )
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en_loc}"/>'
        )
        lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    pages = collect_pages()
    xml = generate_sitemap(pages)
    out = os.path.join(PROJECT_ROOT, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)
    total = len(pages) * 2
    print(f"Generated sitemap.xml with {total} URLs ({len(pages)} EN + {len(pages)} ES)")


if __name__ == "__main__":
    main()
