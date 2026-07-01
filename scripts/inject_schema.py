#!/usr/bin/env python3
"""Inject JSON-LD schema into all HTML pages."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://www.brentwoodorganizers.com"

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": f"{DOMAIN}#localbusiness",
    "name": "Brentwood Organizers",
    "description": "White-glove home organization for Miami's most discerning homes. Expert move-in organizing, downsizing, and relocation services.",
    "telephone": "+14243940619",
    "email": "rhode@brentwoodorganizers.com",
    "url": DOMAIN,
    "image": f"{DOMAIN}/Office.jpeg",
    "priceRange": "$$$",
    "areaServed": [
        {"@type": "City", "name": "Miami"},
        {"@type": "City", "name": "Coral Gables"},
        {"@type": "City", "name": "Brickell"},
        {"@type": "City", "name": "Miami Beach"},
        {"@type": "City", "name": "Coconut Grove"},
        {"@type": "City", "name": "Boca Raton"},
        {"@type": "City", "name": "West Palm Beach"},
        {"@type": "City", "name": "Fort Lauderdale"},
        {"@type": "City", "name": "Pembroke Pines"},
        {"@type": "City", "name": "Bal Harbour"},
        {"@type": "City", "name": "Miami Springs"},
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Home Organization Services",
        "itemListElement": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Move-In Organization",
                    "description": "White-glove move-in setup and unpacking for luxury homes."
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Home Organization",
                    "description": "Beautiful systems for closets, pantries, and everyday spaces."
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Estate Transitions",
                    "description": "Compassionate downsizing and estate transition support."
                }
            }
        ]
    },
    "knowsAbout": [
        "Home Organization",
        "Move-In Services",
        "Senior Downsizing",
        "Closet Organization",
        "Pantry Organization",
        "Estate Transitions",
        "Professional Organizing"
    ]
}


def get_breadcrumb(path: Path, title: str):
    """Build BreadcrumbList schema from file path."""
    parts = []
    rel = path.relative_to(ROOT)
    segments = []
    for seg in rel.parts[:-1]:
        if seg == "blog" or seg == "faqs":
            segments.append(seg)

    items = []
    if not segments and path.parent == ROOT:
        # Root-level page
        slug = path.stem
        label = slug.replace("-", " ").title()
        if slug == "index":
            label = "Home"
        elif slug == "services":
            label = "Services"
        elif slug == "locations":
            label = "Locations"
        elif slug == "consultation":
            label = "Consultation"
        elif slug == "reviews":
            label = "Reviews"
        elif slug == "faqs":
            label = "FAQ"
        elif slug == "blogs":
            label = "Blog"
        items = [{"@type": "ListItem", "position": 1, "name": label, "item": f"{DOMAIN}/{slug}.html"}]
    elif "blog" in segments:
        items = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{DOMAIN}/blog/"},
        ]
        post_slug = rel.parts[-2] if len(rel.parts) > 2 else ""
        if post_slug:
            lang = ""
            if rel.parts[0] in ("fr", "es", "pt"):
                lang = f"/{rel.parts[0]}"
            items.append({
                "@type": "ListItem",
                "position": 3,
                "name": title,
                "item": f"{DOMAIN}{lang}/blog/{post_slug}"
            })
        else:
            items.append({
                "@type": "ListItem",
                "position": 3,
                "name": "Blog",
                "item": f"{DOMAIN}/blog/"
            })
    elif "faqs" in segments:
        items = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {"@type": "ListItem", "position": 2, "name": "FAQ", "item": f"{DOMAIN}/faqs"},
        ]

    if not items:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN}]

    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def get_article_schema(title: str, description: str, url: str):
    """Build Article schema for blog posts."""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": url,
        "author": {
            "@type": "Organization",
            "name": "Brentwood Organizers",
            "url": DOMAIN
        },
        "publisher": {
            "@type": "Organization",
            "name": "Brentwood Organizers",
            "url": DOMAIN,
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/favicon.ico"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        }
    }


def get_service_schema(title: str, description: str, page_path: str):
    """Build Service schema for service pages."""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": title,
        "description": description,
        "provider": {
            "@type": "LocalBusiness",
            "name": "Brentwood Organizers",
            "url": DOMAIN
        },
        "serviceType": "Home Organization",
        "areaServed": {
            "@type": "City",
            "name": "Miami"
        },
        "url": f"{DOMAIN}/{page_path}"
    }


def get_faq_schema(html_content: str):
    """Extract FAQ items from HTML details/summary or .faq-question/.faq-answer elements."""
    questions = []

    # Try details/summary first
    details = re.findall(r'<details[^>]*>(.*?)</details>', html_content, re.DOTALL)
    for d in details:
        q_match = re.search(r'<summary[^>]*>(.*?)</summary>', d, re.DOTALL)
        if not q_match:
            continue
        question = re.sub(r'<[^>]+>', '', q_match.group(1)).strip()
        answer_html = re.sub(r'<summary[^>]*>.*?</summary>', '', d, flags=re.DOTALL)
        answer = re.sub(r'<[^>]+>', '', answer_html).strip()
        if question and answer:
            questions.append({
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {
                    "@type": "AcceptedAnswer",
                    "text": answer
                }
            })

    # Fall back to .faq-question / .faq-answer pattern (button-based)
    if not questions:
        faq_items = re.findall(r'<button\s+class="faq-question"[^>]*>(.*?)</button>\s*<div\s+class="faq-answer"[^>]*>(.*?)</div>', html_content, re.DOTALL)
        for q_html, a_html in faq_items:
            question = re.sub(r'<[^>]+>', '', q_html).strip()
            answer = re.sub(r'<[^>]+>', '', a_html).strip()
            if question and answer:
                questions.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "AcceptedAnswer",
                        "text": answer
                    }
                })

    if not questions:
        return None

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": questions
    }


def extract_meta(html: str, tag: str):
    """Extract meta tag content."""
    match = re.search(rf'<{tag}\s+content="([^"]*)"', html)
    return match.group(1) if match else ""


def extract_title(html: str):
    """Extract page title."""
    match = re.search(r'<title>(.*?)</title>', html)
    return match.group(1) if match else ""


def inject_schema(html: str, schemas: list):
    """Inject JSON-LD scripts before </head>."""
    scripts = ""
    for schema in schemas:
        scripts += f'\n    <script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n    </script>'

    return html.replace("</head>", scripts + "\n</head>")


def process_file(filepath: Path):
    """Process a single HTML file and inject appropriate schema."""
    html = filepath.read_text(encoding="utf-8")

    # Skip if already has JSON-LD
    if 'application/ld+json' in html:
        print(f"  SKIP (already has schema): {filepath.relative_to(ROOT)}")
        return

    title = extract_title(html)
    description = extract_meta(html, "meta")
    schemas = []

    # LocalBusiness on every page
    schemas.append(LOCAL_BUSINESS)

    # BreadcrumbList
    schemas.append(get_breadcrumb(filepath, title))

    # Determine page type
    rel = filepath.relative_to(ROOT)
    parts = rel.parts

    # Blog posts
    if "blog" in parts and filepath.name == "index.html" and len(parts) > 2:
        lang = ""
        if parts[0] in ("fr", "es", "pt"):
            lang = f"/{parts[0]}"
        post_slug = parts[-2]
        url = f"{DOMAIN}{lang}/blog/{post_slug}"
        schemas.append(get_article_schema(title, description, url))

    # FAQ page
    elif "faqs" in parts and filepath.name == "index.html":
        faq = get_faq_schema(html)
        if faq:
            schemas.append(faq)

    # Service pages
    elif filepath.parent == ROOT and filepath.name in (
        "luxury-move-in.html", "home-organization.html", "estate-transitions.html"
    ):
        schemas.append(get_service_schema(title, description, str(filepath)))

    if schemas:
        new_html = inject_schema(html, schemas)
        filepath.write_text(new_html, encoding="utf-8")
        print(f"  OK: {filepath.relative_to(ROOT)}")


def main():
    # All English pages
    html_files = list(ROOT.glob("*.html"))
    # Blog posts + blog index
    html_files.extend(ROOT.glob("blog/*/index.html"))
    html_files.append(ROOT / "blog" / "index.html")
    # FAQ
    html_files.extend(ROOT.glob("faqs/*.html"))

    print(f"Processing {len(html_files)} files...")
    for f in sorted(html_files):
        process_file(f)
    print("Done.")


if __name__ == "__main__":
    main()
