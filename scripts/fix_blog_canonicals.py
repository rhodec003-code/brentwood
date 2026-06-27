#!/usr/bin/env python3
"""
Phase 2: Add canonical tags to blog posts that are missing them.

Blog posts are folder/index.html on GitHub Pages, so canonical URLs should
use trailing slashes (e.g., /blog/post-name/).
"""

import os
import re
from pathlib import Path

BRENTWOOD_ROOT = Path(__file__).parent.parent


def add_canonical_to_file(filepath, dry_run=False):
    """Add a canonical tag to a blog post if it doesn't have one."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Skip if already has canonical
    if '<link rel="canonical"' in html:
        return False
    
    # Determine the canonical URL
    rel = os.path.relpath(filepath, BRENTWOOD_ROOT)
    parts = rel.split(os.sep)
    
    # Determine language prefix
    lang_prefix = ''
    if parts[0] in ('es', 'fr', 'pt'):
        lang_prefix = parts[0] + '/'
        parts = parts[1:]
    
    # Reconstruct the path
    page_path = '/'.join(parts)
    
    # For index.html files, use trailing slash
    if page_path.endswith('/index.html'):
        page_path = page_path.replace('/index.html', '/')
    elif page_path == 'index.html':
        page_path = '/'
    
    # Build canonical URL
    canonical = f"https://www.brentwoodorganizers.com/{lang_prefix}{page_path}"
    
    # Insert canonical after the hreflang block (after x-default line)
    insert_after = re.search(r'<link\s+rel="alternate"\s+hreflang="x-default"[^>]*>', html)
    if insert_after:
        new_canonical = f'\n<link rel="canonical" href="{canonical}">'
        html = html[:insert_after.end()] + new_canonical + html[insert_after.end():]
    else:
        # Fallback: insert after </title>
        insert_after = re.search(r'</title>', html)
        if insert_after:
            new_canonical = f'\n<link rel="canonical" href="{canonical}">'
            html = html[:insert_after.end()] + new_canonical + html[insert_after.end():]
        else:
            print(f"  ⚠️  Could not find insertion point in {rel}")
            return False
    
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    
    return True


def main():
    dry_run = '--dry-run' in __import__('sys').argv
    
    # Find all blog index.html files (across all languages)
    blog_files = []
    for lang in ['', 'es/', 'fr/', 'pt/']:
        blog_dir = BRENTWOOD_ROOT / lang / 'blog'
        if blog_dir.exists():
            # Blog index
            blog_files.append(blog_dir / 'index.html')
            # Blog posts
            for post_dir in blog_dir.iterdir():
                if post_dir.is_dir():
                    post_index = post_dir / 'index.html'
                    if post_index.exists():
                        blog_files.append(post_index)
    
    # Also check faqs/index.html
    for lang in ['', 'es/', 'fr/', 'pt/']:
        faqs_file = BRENTWOOD_ROOT / lang / 'faqs' / 'index.html'
        if faqs_file.exists():
            blog_files.append(faqs_file)
    
    print(f"Found {len(blog_files)} blog/faq files to process")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(blog_files):
        rel = os.path.relpath(filepath, BRENTWOOD_ROOT)
        try:
            if add_canonical_to_file(filepath, dry_run):
                if dry_run:
                    print(f"  ✏️  Would add canonical: {rel}")
                else:
                    print(f"  ✅ Added canonical: {rel}")
                updated += 1
            else:
                print(f"  ⏭️  Already has canonical or no change: {rel}")
                skipped += 1
        except Exception as e:
            print(f"  ❌ Error processing {rel}: {e}")
            skipped += 1
    
    print()
    print(f"Done: {updated} updated, {skipped} skipped/unchanged")


if __name__ == '__main__':
    main()
