#!/usr/bin/env python3
"""
Phase 3: Regenerate sitemap.xml with PT main pages included.

The current sitemap has EN/FR/ES for main pages and EN/FR/ES/PT for blog posts.
This script adds PT main pages with proper hreflang annotations.
"""

import os
import re
from pathlib import Path
from datetime import datetime

BRENTWOOD_ROOT = Path(__file__).parent.parent

# Main pages that exist in all 4 languages
MAIN_PAGES = [
    ('index.html', 1.0),
    ('blogs.html', 0.9),
    ('services.html', 0.9),
    ('consultation.html', 0.9),
    ('locations.html', 0.9),
    ('reviews.html', 0.9),
    ('faqs.html', 0.8),
    ('estate-transitions.html', 0.8),
    ('home-organization.html', 0.8),
    ('luxury-move-in.html', 0.8),
]

# Location pages
LOCATION_PAGES = [
    ('bal-harbour.html', 0.7),
    ('boca-raton.html', 0.7),
    ('brickell.html', 0.7),
    ('coral-gables.html', 0.7),
    ('fort-lauderdale.html', 0.7),
    ('miami-springs.html', 0.7),
    ('pembroke-pines.html', 0.7),
    ('west-palm-beach.html', 0.7),
]

LANGUAGES = ['en', 'fr', 'es', 'pt']
LANG_PREFIXES = {'en': '', 'fr': 'fr', 'es': 'es', 'pt': 'pt'}


def get_blog_posts():
    """Get all blog post slugs from the English blog directory."""
    blog_dir = BRENTWOOD_ROOT / 'blog'
    posts = []
    for item in sorted(blog_dir.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            posts.append(item.name)
    return posts


def generate_sitemap():
    """Generate a complete sitemap.xml with all 4 languages."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    
    base = 'https://brentwoodorganizers.com'
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Helper: generate hreflang links for a page
    def hreflang_links(page_path, is_homepage=False):
        """Generate hreflang xhtml:link entries for a page."""
        links = []
        for lang in LANGUAGES:
            prefix = LANG_PREFIXES[lang]
            if is_homepage:
                if lang == 'en':
                    url = f"{base}/index.html"
                else:
                    url = f"{base}/{prefix}"
            elif prefix:
                url = f"{base}/{prefix}/{page_path}"
            else:
                url = f"{base}/{page_path}"
            links.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{url}"/>')
        # x-default points to English
        if is_homepage:
            links.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{base}/index.html"/>')
        else:
            links.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{base}/{page_path}"/>')
        return links
    
    # Helper: add a URL entry
    def add_url(loc, priority, is_homepage=False, page_path=None):
        links = []
        if page_path:
            links = hreflang_links(page_path, is_homepage)
        
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        lines.append(f'    <changefreq>monthly</changefreq>')
        lines.append(f'    <priority>{priority:.1f}</priority>')
        for link in links:
            lines.append(link)
        lines.append('  </url>')
    
    # === HOMEPAGE (4 languages) ===
    add_url(f"{base}/index.html", 1.0, is_homepage=True, page_path='index.html')
    add_url(f"{base}/fr", 1.0, is_homepage=True, page_path='index.html')
    add_url(f"{base}/es", 1.0, is_homepage=True, page_path='index.html')
    add_url(f"{base}/pt", 1.0, is_homepage=True, page_path='index.html')
    
    # === MAIN PAGES (4 languages each) ===
    for page, priority in MAIN_PAGES:
        for lang in LANGUAGES:
            prefix = LANG_PREFIXES[lang]
            if prefix:
                loc = f"{base}/{prefix}/{page}"
            else:
                loc = f"{base}/{page}"
            add_url(loc, priority, page_path=page)
    
    # === LOCATION PAGES (4 languages each) ===
    for page, priority in LOCATION_PAGES:
        for lang in LANGUAGES:
            prefix = LANG_PREFIXES[lang]
            if prefix:
                loc = f"{base}/{prefix}/{page}"
            else:
                loc = f"{base}/{page}"
            add_url(loc, priority, page_path=page)
    
    # === BLOG INDEX (4 languages) ===
    for lang in LANGUAGES:
        prefix = LANG_PREFIXES[lang]
        if prefix:
            loc = f"{base}/{prefix}/blog"
        else:
            loc = f"{base}/blog"
        add_url(loc, 0.8, page_path='blog/index.html')
    
    # === BLOG POSTS (4 languages each) ===
    blog_posts = get_blog_posts()
    for post_slug in blog_posts:
        for lang in LANGUAGES:
            prefix = LANG_PREFIXES[lang]
            if prefix:
                loc = f"{base}/{prefix}/blog/{post_slug}"
            else:
                loc = f"{base}/blog/{post_slug}"
            add_url(loc, 0.6, page_path=f'blog/{post_slug}/index.html')
    
    # === FAQ PAGES (4 languages) ===
    for lang in LANGUAGES:
        prefix = LANG_PREFIXES[lang]
        if prefix:
            loc = f"{base}/{prefix}/faqs"
        else:
            loc = f"{base}/faqs"
        add_url(loc, 0.7, page_path='faqs/index.html')
    
    lines.append('</urlset>')
    return '\n'.join(lines)


def main():
    sitemap_content = generate_sitemap()
    
    # Count URLs
    url_count = sitemap_content.count('<loc>')
    print(f"Generated sitemap with {url_count} URLs")
    
    # Write
    sitemap_path = BRENTWOOD_ROOT / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"Written to: {sitemap_path}")
    
    # Verify XML is well-formed
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = root.findall('.//sitemap:url', ns)
        # Also count without namespace
        all_urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        print(f"XML validation: ✅ ({len(all_urls)} URLs parsed)")
    except Exception as e:
        print(f"XML validation: ❌ {e}")


if __name__ == '__main__':
    main()
