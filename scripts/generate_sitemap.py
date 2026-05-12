#!/usr/bin/env python3
"""Generate multilingual sitemap.xml for brentwoodorganizers.com.

Usage:
    python3 scripts/generate_sitemap.py

Outputs sitemap.xml to the project root with English, French, and Spanish URLs,
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

LANGUAGES = {
    "": "en",
    "fr": "fr",
    "es": "es",
}

# Pages that should be excluded from the sitemap
EXCLUDED = {
    "faqs.html",
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


def collect_pages_in_dir(base_dir: str) -> list[str]:
    """Collect relative paths of HTML files under a directory, skipping excluded."""
    pages = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in LANGUAGES]

        for fname in files:
            if not fname.endswith(".html"):
                continue

            full = os.path.join(root, fname)
            rel = os.path.relpath(full, base_dir)

            if fname in EXCLUDED or rel in EXCLUDED_PATHS:
                continue

            pages.append(rel)
    return pages


def file_exists_in_lang(rel: str, lang_prefix: str) -> bool:
    """Check if a file exists under a language directory."""
    if not lang_prefix:
        return True
    return os.path.isfile(os.path.join(PROJECT_ROOT, lang_prefix, rel))


def collect_all_pages() -> list[tuple[str, str, str, dict[str, str]]]:
    """Return list of (en_loc, lastmod, priority, lang_urls) tuples.

    lang_urls maps language code to its full URL, only for languages
    where the file actually exists on disk.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    en_files = collect_pages_in_dir(PROJECT_ROOT)

    results = []
    for rel in en_files:
        en_url = file_to_url(rel)
        es_url = file_to_url(f"es/{rel}")
        fr_url = file_to_url(f"fr/{rel}")
        priority = get_priority(rel)

        lang_urls = {"en": DOMAIN + en_url}
        if file_exists_in_lang(rel, "fr"):
            lang_urls["fr"] = DOMAIN + fr_url
        if file_exists_in_lang(rel, "es"):
            lang_urls["es"] = DOMAIN + es_url

        results.append((DOMAIN + en_url, now, priority, lang_urls))

    priority_order = {
        PRIORITY_HOME: 0, PRIORITY_SERVICE: 1, PRIORITY_LOCATION: 2,
        PRIORITY_BLOG_INDEX: 3, PRIORITY_BLOG_POST: 4, PRIORITY_OTHER: 5,
    }
    results.sort(key=lambda p: (priority_order.get(p[2], 99), p[0]))
    return results


def generate_sitemap(pages: list[tuple[str, str, str, dict[str, str]]]) -> str:
    """Generate sitemap XML with hreflang alternates for EN/FR/ES."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
    )

    for en_loc, lastmod, priority, lang_urls in pages:
        for lang, loc in lang_urls.items():
            lines.append("  <url>")
            lines.append(f"    <loc>{loc}</loc>")
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
            lines.append(f"    <changefreq>{CHANGE_FREQ_DEFAULT}</changefreq>")
            lines.append(f"    <priority>{priority}</priority>")

            for alt_lang, alt_loc in lang_urls.items():
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="{alt_lang}" href="{alt_loc}"/>'
                )
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en_loc}"/>'
            )
            lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines)


def main():
    pages = collect_all_pages()
    xml = generate_sitemap(pages)
    out = os.path.join(PROJECT_ROOT, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)

    counts = {"en": 0, "fr": 0, "es": 0}
    for _, _, _, lang_urls in pages:
        for lang in lang_urls:
            counts[lang] += 1
    total = sum(counts.values())
    print(f"Generated sitemap.xml with {total} URLs (EN:{counts['en']} FR:{counts['fr']} ES:{counts['es']})")


if __name__ == "__main__":
    main()
