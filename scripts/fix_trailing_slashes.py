#!/usr/bin/env python3
"""
Fix trailing slash inconsistency between canonical and hreflang tags.

Problem:
- Canonical URLs use trailing slashes: /blog/post-name/
- Hreflang URLs don't: /blog/post-name
- This causes Google to treat them as separate pages

Fix:
- Add trailing slashes to all hreflang URLs that point to directory-based paths
- Keep .html files without trailing slashes (they're actual files, not directories)
"""

import os
import re
from pathlib import Path

BRENTWOOD_DIR = Path(__file__).parent.parent


def needs_trailing_slash(url: str) -> bool:
    """Check if a URL should have a trailing slash (directory-based paths)."""
    # Remove domain
    path = re.sub(r'^https?://(?:www\.)?brentwoodorganizers.com', '', url)
    # Directory-based paths (blog posts, faqs directory) need trailing slash
    # Match both /blog and /blog/post-name patterns
    if re.match(r'^/(blog|faqs)(/|$)', path):
        return True
    if re.match(r'^/(es|fr|pt)/(blog|faqs)(/|$)', path):
        return True
    return False


def fix_hreflang_tag(tag: str) -> str:
    """Add trailing slash to hreflang URLs that need it."""
    match = re.match(r'(<link[^>]*href=")([^"]+)(")', tag)
    if not match:
        return tag
    url = match.group(2)
    if needs_trailing_slash(url) and not url.endswith('/'):
        return match.group(1) + url + '/' + match.group(3)
    return tag


def process_file(filepath: Path) -> bool:
    """Process a single HTML file. Returns True if changes were made."""
    content = filepath.read_text()
    original = content

    # Find all hreflang tags and fix them
    hreflang_tags = re.findall(r'<link[^>]*hreflang[^>]*>', content)
    for tag in hreflang_tags:
        fixed = fix_hreflang_tag(tag)
        if fixed != tag:
            content = content.replace(tag, fixed)

    if content != original:
        filepath.write_text(content)
        return True
    return False


def main():
    fixed_count = 0

    # Process all HTML files in brentwood/
    for html_file in BRENTWOOD_DIR.rglob('*.html'):
        if process_file(html_file):
            fixed_count += 1
            print(f"  Fixed: {html_file.relative_to(BRENTWOOD_DIR)}")

    print(f"\nDone. Fixed {fixed_count} file(s).")


if __name__ == '__main__':
    main()
