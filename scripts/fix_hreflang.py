#!/usr/bin/env python3
"""
Phase 1: Fix hreflang tags, language switcher, and footer across all brentwood HTML files.

This script:
1. Adds complete hreflang tags (en, es, fr, pt, x-default) to all pages
2. Adds PT to the language switcher in the nav
3. Adds language links to the footer
4. Standardizes hreflang URLs (uses brentwoodorganizers.com consistently)
"""

import os
import re
import sys
from pathlib import Path

BRENTWOOD_ROOT = Path(__file__).parent.parent  # scripts/ → brentwood/


def get_page_name(filepath):
    """Extract the page name from a file path.
    
    Examples:
        index.html → index.html
        es/services.html → services.html
        blog/top-home-organizers-in-miami/index.html → blog/top-home-organizers-in-miami/index.html
        es/blog/top-home-organizers-in-miami/index.html → blog/top-home-organizers-in-miami/index.html
    """
    rel = os.path.relpath(filepath, BRENTWOOD_ROOT)
    parts = rel.split(os.sep)
    
    # If starts with a language folder, strip it
    if parts[0] in ('es', 'fr', 'pt'):
        parts = parts[1:]
    
    return os.path.join(*parts) if parts else 'index.html'


def get_language_of_file(filepath):
    """Determine the language of a file based on its path."""
    rel = os.path.relpath(filepath, BRENTWOOD_ROOT)
    parts = rel.split(os.sep)
    
    if parts[0] == 'es':
        return 'es'
    elif parts[0] == 'fr':
        return 'fr'
    elif parts[0] == 'pt':
        return 'pt'
    else:
        return 'en'


def generate_hreflang_block(page_name, base_domain='https://brentwoodorganizers.com'):
    """Generate the complete hreflang block for a page."""
    # For the base URL, use the page name directly
    en_url = f"{base_domain}/{page_name}" if page_name != 'index.html' else f"{base_domain}/index.html"
    es_url = f"{base_domain}/es/{page_name}" if page_name != 'index.html' else f"{base_domain}/es/index.html"
    fr_url = f"{base_domain}/fr/{page_name}" if page_name != 'index.html' else f"{base_domain}/fr/index.html"
    pt_url = f"{base_domain}/pt/{page_name}" if page_name != 'index.html' else f"{base_domain}/pt/index.html"
    
    return f'''    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="es" href="{es_url}">
    <link rel="alternate" hreflang="fr" href="{fr_url}">
    <link rel="alternate" hreflang="pt" href="{pt_url}">
    <link rel="alternate" hreflang="x-default" href="{en_url}">'''


def generate_lang_switcher(lang, is_root=False):
    """Generate the language switcher nav item for a given language.
    
    Shows all 4 languages, with the current one bolded (no link).
    """
    languages = {
        'en': {'label': 'EN', 'path': '' if is_root else '../'},
        'es': {'label': 'ES', 'path': 'es/' if is_root else '../es/'},
        'fr': {'label': 'FR', 'path': 'fr/' if is_root else '../fr/'},
        'pt': {'label': 'PT', 'path': 'pt/' if is_root else '../pt/'},
    }
    
    parts = []
    for code, info in languages.items():
        if code == lang:
            parts.append(f"<strong>{info['label']}</strong>")
        else:
            parts.append(f'<a href="{info["path"]}">{info["label"]}</a>')
    
    return ' <span class="lang-sep">|</span> '.join(parts)


def find_hreflang_block(html):
    """Find the existing hreflang block in the HTML."""
    # Match a block of hreflang link tags
    pattern = r'(?:\s*<link\s+rel="alternate"\s+hreflang="[^"]*"[^>]*>)+'
    match = re.search(pattern, html)
    return match


def find_lang_switcher(html):
    """Find the existing language switcher in the HTML."""
    pattern = r'<li\s+class="lang-switch">[\s\S]*?</li>'
    match = re.search(pattern, html)
    return match


def find_footer(html):
    """Find the footer section."""
    pattern = r'<!-- Footer -->\s*<footer>.*?</footer>'
    match = re.search(pattern, html, re.DOTALL)
    return match


def update_file(filepath, dry_run=False):
    """Update a single HTML file with correct hreflang, switcher, and footer."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    page_name = get_page_name(filepath)
    lang = get_language_of_file(filepath)
    is_root = (lang == 'en')
    
    # 1. Update hreflang block
    hreflang_match = find_hreflang_block(html)
    if hreflang_match:
        new_hreflang = generate_hreflang_block(page_name)
        html = html[:hreflang_match.start()] + new_hreflang + html[hreflang_match.end():]
    else:
        # No hreflang found — inject after <meta charset> or at start of <head>
        # Find a good insertion point
        insert_after = re.search(r'<meta[^>]*name="description"[^>]*>', html)
        if insert_after:
            new_hreflang = '\n' + generate_hreflang_block(page_name)
            html = html[:insert_after.end()] + new_hreflang + html[insert_after.end():]
        else:
            print(f"  ⚠️  Could not find insertion point for hreflang in {filepath}")
            return False
    
    # 2. Update language switcher
    switcher_match = find_lang_switcher(html)
    if switcher_match:
        new_switcher = f'<li class="lang-switch">{generate_lang_switcher(lang, is_root)}</li>'
        html = html[:switcher_match.start()] + new_switcher + html[switcher_match.end():]
    else:
        print(f"  ⚠️  No language switcher found in {filepath}")
    
    # 3. Update footer — add language links
    # Find the footer-links ul and add language links
    footer_links_pattern = r'(<ul\s+class="footer-links">.*?</ul>)'
    footer_match = re.search(footer_links_pattern, html, re.DOTALL)
    if footer_match:
        old_footer_links = footer_match.group(1)
        # Add language links at the end of the footer links
        new_footer_links = old_footer_links.replace(
            '</ul>',
            '<li class="lang-switch"><a href="fr/">FR</a> <span class="lang-sep">|</span> <a href="es/">ES</a> <span class="lang-sep">|</span> <a href="pt/">PT</a></li>\n        </ul>'
            if is_root else
            '<li class="lang-switch"><a href="../fr/">FR</a> <span class="lang-sep">|</span> <a href="../es/">ES</a> <span class="lang-sep">|</span> <a href="../pt/">PT</a></li>\n        </ul>'
        )
        html = html[:footer_match.start()] + new_footer_links + html[footer_match.end():]
    
    # Write the file
    if html != original:
        if dry_run:
            print(f"  ✏️  Would update: {filepath}")
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✅ Updated: {filepath}")
        return True
    else:
        print(f"  ⏭️  No changes: {filepath}")
        return False


def main():
    dry_run = '--dry-run' in sys.argv
    
    # Find all HTML files
    html_files = sorted(BRENTWOOD_ROOT.glob('**/*.html'))
    
    # Filter out google verification file
    html_files = [f for f in html_files if 'google' not in f.name.lower()]
    
    print(f"Found {len(html_files)} HTML files to process")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()
    
    updated = 0
    skipped = 0
    
    for filepath in html_files:
        rel = os.path.relpath(filepath, BRENTWOOD_ROOT)
        try:
            if update_file(filepath, dry_run):
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ❌ Error processing {rel}: {e}")
            skipped += 1
    
    print()
    print(f"Done: {updated} updated, {skipped} skipped/unchanged")


if __name__ == '__main__':
    main()
