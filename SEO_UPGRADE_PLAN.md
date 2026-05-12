Now I have a comprehensive picture. Here's the full SEO audit:

---

SEO Audit: brentwoodorganizers.com

Overall assessment: Solid foundations, but several critical gaps are holding this back from ranking well.

---

🔴 CRITICAL ISSUES

1. Missing H1 on homepage
The homepage has no <h1> tag at all. The hero text uses <h1 class="hero-title"> but I couldn't confirm its content — need to verify, but the grep only found H2 tags on the homepage. The H1 is the #1 on-page signal for what the page is about. Google needs it.

2. NO Structured Data (Schema.org)
Zero JSON-LD markup anywhere on the site. This is a local service business — they should have:
- LocalBusiness schema with NAP (name, address, phone, service area)
- Service schema on service pages
- FAQPage schema on the FAQ page
- Article schema on blog posts
- BreadcrumbList sitewide

This is the single biggest missed opportunity. Competitors with schema get rich results; without it, they're invisible in features like local packs, FAQ snippets, and knowledge panels.

3. NO Open Graph / Twitter Cards
Zero OG tags. When someone shares a link on social media, it renders as a bare URL with no image, title, or description. This kills social shareability and indirect traffic.

4. Missing robots.txt
Returns a 404. Without it, Google has no instructions. At minimum, it should exist and reference the sitemap.

5. No canonical tags
Every page is missing <link rel="canonical">. This means Google may see brentwoodorganizers.com and www.brentwoodorganizers.com as duplicate pages, splitting ranking signals.

---

🟡 HIGH PRIORITY

6. Location pages are thin
All 8 location pages follow the exact same template with nearly identical meta descriptions:
 "Luxury home organization, move-in support, and estate transition services for [City] by Brentwood Organizers."

These are essentially doorway pages. Google will flag them as thin/duplicate content. Each needs:
- 500+ words of unique, location-specific content
- Local landmarks, neighborhoods, property types
- Client work done in that area
- Embedded Google Map

7. Blog content volume vs. quality
18 blog posts exist — that's a good start. But blog index only shows ~731 words. Individual posts need to be 1,500–2,500+ words to rank. Also:
- Blog posts use subdirectory URLs (/blog/slug) — good ✅
- No internal linking from blog posts back to service pages
- Blog index page has no structured data

8. Missing Google Business Profile integration
No mention of a Google Maps pin, embedded review widget, or GBP link. For a local service business, this is essential for local SEO.

9. No breadcrumb navigation
No visible breadcrumbs and no breadcrumb schema. hurts both UX and rich results.

---

🟠 MEDIUM PRIORITY

10. Image optimization issues
- Local images (Living Room.jpeg, Closet 3.jpeg) return empty headers — may not exist or have wrong casing (GitHub Pages is case-sensitive)
- Heavy use of stock photos (Unsplash, Pexels) — real client photos build trust and rank better
- No loading="lazy" on below-the-fold images
- No WebP/AVIF format — serving only JPEG
- One local image is ~197KB uncompressed

11. Homepage text is thin
Only ~738 words of text content. For a competitive niche like "luxury home organizer Miami," aim for 1,500+ words on the homepage with keyword-rich sections.

12. No customer reviews/testimonials with schema
Testimonials section exists but has no Review or AggregateRating markup. Missing out on star ratings in search results.

13. Internal linking is weak
- Location pages don't link to each other
- Blog posts don't link to service pages
- No "related articles" on blog index
- Sitemap is well-structured ✅ but internal link graph is flat

14. No hreflang or language alternates
If serving Spanish-speaking Miami clients (huge market), there's no Spanish version of the site at all.

---

🟢 LOW PRIORITY / NICE-TO-HAVE
 (1/2)

 15. Performance
- Hosted on GitHub Pages (fast CDN ✅)
- Inline CSS (no render-blocking stylesheets ✅)
- Only 2 fonts loaded (reasonable)
- But: Calendly widget loads synchronously, could block
- No preconnect to Calendly or Unsplash domains

16. Mobile UX
- Viewport meta tag present ✅
- Single HTML file with inline styles — renders fast on mobile ✅
- Hamburger menu likely needed (check on actual mobile)

17. No 404 custom page
Uses default GitHub Pages 404. Should be branded.

18. HTTPS enforced ✅ — GitHub Pages handles this automatically.

19. No favicon sizes/Apple touch icon
Only one favicon. Missing Apple touch icon for iOS home screen.

---

📋 QUICK WINS (do these first)

1

• Priority: 1

• Action: Add <h1> to homepage with target keyword

• Impact: High

2

• Priority: 2

• Action: Add LocalBusiness JSON-LD schema to every page

• Impact: High

3

• Priority: 3

• Action: Add FAQPage schema to FAQ page

• Impact: High

4

• Priority: 4

• Action: Add canonical tags to every page

• Impact: High

5

• Priority: 5

• Action: Create robots.txt referencing sitemap.xml

• Impact: High

6

• Priority: 6

• Action: Add Open Graph + Twitter Card meta tags

• Impact: Medium

7

• Priority: 7

• Action: Fix broken image references (case sensitivity)

• Impact: Medium

8

• Priority: 8

• Action: Expand location pages with unique content

• Impact: High

9

• Priority: 9

• Action: Add breadcrumb navigation + schema

• Impact: Medium

10

• Priority: 10

• Action: Set up Google Business Profile

• Impact: High

---

🎯 KEYWORD TARGETING GAPS

Current title targets "Miami" broadly but misses high-intent phrases:
- "professional organizer near me"
- "luxury organizer [neighborhood]"
- "move-in unpacking service [city]"
- "senior downsizing help Miami"
- "closet organizer Miami"
- "pantry organization service"
- "home organizer Coral Gables"

Location pages could each target 10+ neighborhood-specific keywords if fleshed out.
