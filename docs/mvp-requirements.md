# Brentwood Organizers — MVP Requirements

> Extracted from existing live site on June 29, 2026
> Source: `brentwood/` in marketing_agency workspace

## 1. Business Overview

### Company
- **Name:** Brentwood Organizers
- **Tagline:** White-glove home organization for Miami's most discerning homes
- **Industry:** Professional home organization and lifestyle management
- **Positioning:** Premium/luxury service provider for high-net-worth individuals in South Florida
- **Contact:** +1 (424) 394-0619, rhode@brentwoodorganizers.com
- **Social:** Instagram (@brentwoodorganizers)

### Target Audience
- **Primary:** High-net-worth individuals moving into luxury homes and high-rises in Miami
- **Secondary:** Seniors requiring compassionate downsizing and estate transition support
- **Tertiary:** Homeowners seeking whole-home organization (closets, pantries, kitchens, offices)

### Service Areas
- **Primary:** Miami, Coral Gables, Brickell, Miami Beach, Coconut Grove, Miami Springs
- **Extended:** Bal Harbour, Boca Raton, Fort Lauderdale, Pembroke Pines, West Palm Beach

### Business Goals
- Generate qualified consultation requests through the website
- Establish brand authority in luxury home organization
- Rank for local SEO keywords across South Florida service areas
- Showcase expertise through content marketing (blog)
- Build trust through client testimonials and reviews

## 2. Functional Requirements

### 2.1 Site Map
```
brentwoodorganizers.com/
├── Home (index.html)
├── Services (services.html)
│   ├── Luxury Move-In (luxury-move-in.html)
│   ├── Home Organization (home-organization.html)
│   └── Estate Transitions (estate-transitions.html)
├── Locations (locations.html)
│   ├── Bal Harbour (bal-harbour.html)
│   ├── Boca Raton (boca-raton.html)
│   ├── Brickell (brickell.html)
│   ├── Coral Gables (coral-gables.html)
│   ├── Fort Lauderdale (fort-lauderdale.html)
│   ├── Miami Springs (miami-springs.html)
│   ├── Pembroke Pines (pembroke-pines.html)
│   └── West Palm Beach (west-palm-beach.html)
├── Reviews (reviews.html)
├── FAQs (faqs/index.html)
├── Blog (blogs.html)
│   └── [18+ individual blog posts]
├── Consultation (consultation.html)
├── 404 Error Page (404.html)
└── Translations
    ├── Spanish (es/)
    ├── French (fr/)
    └── Portuguese (pt/)
```

### 2.2 Pages

| Page | Purpose | Key Sections |
|------|---------|-------------|
| Home | Brand introduction and service overview | Hero banner, value proposition, service highlights, CTAs |
| Services | Complete service catalog | Service cards with descriptions and CTAs |
| Luxury Move-In | Dedicated move-in service page | Hero, process description, benefits, consultation CTA |
| Home Organization | Dedicated organization service page | Hero, space types (closets, pantries, etc.), benefits, CTA |
| Estate Transitions | Dedicated estate/downsizing service page | Hero, compassionate approach, process, CTA |
| Locations | Overview of all service areas | Geographic coverage, service area list |
| Location Pages (×8) | Local SEO landing pages | Location-specific hero, services offered, local context, CTA |
| Reviews | Social proof and testimonials | Client review cards, ratings, trust signals |
| FAQs | Address common questions and objections | Accordion-style Q&A, consultation CTA |
| Blog Index | Content marketing hub | Article cards with titles, dates, excerpts |
| Blog Posts (×18) | SEO content and thought leadership | Article content, related posts, schema markup |
| Consultation | Lead capture form | Contact form with service selection, submission handling |
| 404 | Error handling | Branded error page with navigation back to site |

### 2.3 Features
- **Responsive Navigation:** Fixed/sticky nav with dropdown menus, mobile hamburger menu
- **Hero Sections:** Full-viewport hero banners with background images and overlay cards
- **Service Cards:** Reusable component for displaying services with descriptions and links
- **CTA Buttons:** Primary (dark), secondary (outline), and gold accent button variants
- **Lead Capture Form:** Consultation request form with service type selection
- **Blog System:** Static blog with individual article pages and index listing
- **Multilingual Navigation:** hreflang tags and translated page versions
- **Social Proof:** Reviews page with client testimonials
- **FAQ Accordion:** Expandable Q&A sections with FAQPage schema

### 2.4 Forms & Lead Capture
- **Consultation Form:** Primary lead capture mechanism
  - Fields: Name, email, phone, service type, message
  - Purpose: Schedule initial consultation with potential clients
  - Destination: Email notification to business owner

### 2.5 Multilingual Support
- **Languages:** English (primary), Spanish, French, Portuguese
- **Scope:** Full page translation for all core pages (home, services, locations, consultation, reviews, FAQs)
- **Implementation:** Duplicate HTML files in language subdirectories (`es/`, `fr/`, `pt/`)
- **hreflang:** Proper hreflang tags on all pages pointing to language variants

## 3. Content Requirements

### Tone & Voice
- **Tone:** Sophisticated, warm, professional, and approachable
- **Voice:** Luxury service provider that is accessible and personal
- **Style:** Clean, minimal copy with emphasis on quality and discretion
- **Keywords:** "white-glove," "luxury," "discerning," "compassionate," "expert"

### Content Inventory
- **Core Pages:** 15+ unique HTML pages
- **Blog Posts:** 18 articles covering organizing tips, senior downsizing, Miami relocation
- **Location Pages:** 8 geo-targeted landing pages
- **Reviews:** Client testimonials displayed on dedicated page
- **FAQs:** Common questions about services, pricing, and process

### Visual Assets
- **Hero Images:** Professional photography of organized spaces (bedrooms, closets, living rooms)
- **Social Preview:** 1200×630 OG image for social sharing
- **Favicons:** Multiple sizes (16×16, 32×32, ICO, apple-touch-icon)
- **Web Manifest:** PWA-compatible site.webmanifest
- **Icons:** SVG icons for social media links (Instagram)

## 4. Technical Requirements

### Stack
- **Hosting:** GitHub Pages (static hosting)
- **Framework:** Pure static HTML5 (no framework)
- **CSS:** Inline `<style>` tags with CSS custom properties (no preprocessor)
- **JavaScript:** Minimal vanilla JS for mobile menu toggle and interactions
- **Fonts:** Google Fonts (Cormorant Garamond + Inter)

### Infrastructure
- **DNS:** Custom domain (brentwoodorganizers.com) with CNAME record
- **CDN:** GitHub Pages global CDN
- **Asset Hosting:** Static files served from GitHub Pages root
- **Error Monitoring:** Sentry (JavaScript error tracking)

### Performance
- **Font Loading:** Preconnect to Google Fonts, rel=preload for critical resources
- **Image Optimization:** External images from Unsplash (optimized URLs with w/q/fit parameters)
- **CSS Strategy:** Inline critical CSS per page (no external stylesheet blocking)
- **Responsive Images:** Background images with center/cover sizing

### Observability
- **Sentry:** JavaScript error tracking and performance monitoring
- **Microsoft Clarity:** Session replay, heatmaps, and user behavior analytics (tag: `x6msvbg50y`)
- **Google Search Console:** Indexing and search performance monitoring
- **[needs clarification]:** Google Analytics or other traffic analytics integration

## 5. SEO Requirements

### Strategy
- **Primary Approach:** Local SEO with geo-targeted landing pages
- **Secondary Approach:** Content marketing through blog articles
- **Tertiary Approach:** Technical SEO excellence (schema, hreflang, sitemaps)

### Technical SEO
- **Meta Tags:** Unique title and description per page
- **Open Graph:** Complete OG tags (type, site_name, locale, title, description, URL, image)
- **Twitter Cards:** Summary large image cards with alt text
- **Canonical URLs:** Self-referencing canonical tags on all pages
- **hreflang:** Complete hreflang implementation (en, es, fr, pt, x-default)
- **Structured Data:** Schema.org markup (LocalBusiness, FAQPage, Article, BreadcrumbList)
- **Sitemap:** Comprehensive sitemap.xml with hreflang alternates
- **robots.txt:** Permissive crawl directives with sitemap reference

### Content SEO
- **Blog Topics:** Home organization tips, senior downsizing, Miami relocation, minimalism benefits
- **Keyword Targets:** "home organizer Miami," "luxury move-in," "senior downsizing Miami," "closet organization"
- **Content Frequency:** [needs clarification] — 18 posts exist, publication cadence unknown

### Local SEO
- **Location Pages:** 8 dedicated geo-targeted pages with unique content
- **Schema Markup:** LocalBusiness schema with service area
- **Google Business:** [needs clarification] — Google Business Profile integration status

## 6. Design Requirements

### Design System
- **Colors:**
  - Cream: `#faf8f4` (background)
  - Warm White: `#f5f2ed` (sections)
  - Sand: `#e8e0d4` (borders)
  - Stone: `#c9bfb0` (subtle borders)
  - Charcoal: `#2a2520` (text, buttons)
  - Warm Gray: `#6b6259` (secondary text)
  - Light Gray: `#9c9289` (muted text)
  - Gold: `#b8965a` (accent, CTAs)
  - Gold Light: `#d4ad73` (hover states)

- **Typography:**
  - Headings: Cormorant Garamond (300-600 weight, serif)
  - Body: Inter (300-600 weight, sans-serif)
  - Section Labels: 0.68rem, uppercase, 0.2em letter-spacing
  - Section Titles: clamp(2.2rem, 4vw, 4rem), 300 weight
  - Body Text: 0.92-0.98rem, 1.7-1.85 line height
  - Navigation: 0.74-0.75rem, uppercase, 0.12em letter-spacing

- **Components:**
  - Navigation bar (fixed/sticky, with dropdown)
  - Hero sections (full-viewport with overlay card)
  - Service cards (bordered, with title/description/link)
  - CTA buttons (primary, secondary, gold variants)
  - Section layouts (label + title + intro pattern)
  - Footer (dark background, logo + links + social)
  - Mobile menu (hamburger toggle, full-width dropdown)

### Responsive Behavior
- **Breakpoints:**
  - Desktop: >1024px (full navigation, multi-column layouts)
  - Tablet: ≤1024px (hamburger menu, adjusted spacing)
  - Mobile: ≤900px (single column, reduced padding)
- **Mobile Navigation:** Hamburger menu with animated toggle (X icon when open)
- **Grid Layouts:** CSS Grid for service cards and location layouts
- **Fluid Typography:** clamp() for section titles

## 7. MVP Scope

### In Scope (Phase 1)
- [ ] Static HTML website with core pages (home, services, consultation, reviews, FAQs)
- [ ] 3 dedicated service pages (move-in, home organization, estate transitions)
- [ ] 8 location-specific landing pages for local SEO
- [ ] Consultation request form (lead capture)
- [ ] Complete multilingual support (EN/ES/FR/PT)
- [ ] Blog system with 18 existing articles
- [ ] Full SEO implementation (meta tags, schema, hreflang, sitemap)
- [ ] Responsive design with mobile-first approach
- [ ] Luxury design system (color palette, typography, components)
- [ ] Error monitoring (Sentry)
- [ ] GitHub Pages hosting with custom domain

### Out of Scope (Future Phases)
- [ ] Dynamic content management system (CMS)
- [ ] Client portal or booking system
- [ ] Email marketing integration
- [ ] Advanced analytics dashboard
- [ ] Video content integration
- [ ] Before/after photo gallery
- [ ] Online payment or quoting system
- [ ] Chatbot or live chat

## 8. Success Metrics
- **Lead Generation:** Number of consultation form submissions per month
- **Search Visibility:** Organic traffic growth from target keywords
- **Local Rankings:** Position for "home organizer [location]" queries
- **Engagement:** Time on site, pages per session, blog read-through rates
- **Conversion:** Consultation request rate (form submissions / visitors)
- **Indexing Health:** All pages indexed in Google Search Console without errors
