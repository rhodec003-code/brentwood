#!/usr/bin/env python3
"""Add self-referencing canonical tags to all HTML pages."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://www.brentwoodorganizers.com"

def get_canonical_url(filepath: Path):
    """Get the canonical URL for a given file path."""
    rel = filepath.relative_to(ROOT)
    parts = list(rel.parts)

    # Remove index.html from path segments
    if parts[-1] == "index.html":
        parts = parts[:-1]

    if not parts:
        return DOMAIN

    path = "/".join(parts)
    if rel.name == "index.html" or path.endswith("/"):
        return f"{DOMAIN}/{path}/"
    return f"{DOMAIN}/{path}"

def add_canonical(html: str, canonical_url: str):
    """Add canonical link tag after the last hreflang tag or after <head>."""
    canonical_tag = f'    <link rel="canonical" href="{canonical_url}">'

    # Insert after the last hreflang tag
    hreflang_matches = list(re.finditer(r'<link[^>]*hreflang[^>]*>', html))
    if hreflang_matches:
        insert_pos = hreflang_matches[-1].end()
        return html[:insert_pos] + f'\n{canonical_tag}' + html[insert_pos:]
    else:
        # Insert right after <head>
        return html.replace('<head>', '<head>\n' + canonical_tag, 1)

def process_file(filepath: Path):
    """Process a single HTML file."""
    html = filepath.read_text(encoding="utf-8")

    # Skip if already has canonical
    if 'rel="canonical"' in html:
        print(f"  SKIP: {filepath.relative_to(ROOT)}")
        return

    canonical_url = get_canonical_url(filepath)
    new_html = add_canonical(html, canonical_url)
    filepath.write_text(new_html, encoding="utf-8")
    print(f"  OK: {filepath.relative_to(ROOT)} -> {canonical_url}")

def main():
    # English pages only
    html_files = list(ROOT.glob("*.html"))
    html_files.extend(ROOT.glob("blog/*/index.html"))
    html_files.append(ROOT / "blog" / "index.html")
    html_files.extend(ROOT.glob("faqs/*.html"))

    print(f"Processing {len(html_files)} files...")
    for f in sorted(html_files):
        process_file(f)
    print("Done.")

if __name__ == "__main__":
    main()
