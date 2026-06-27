# Brentwood Organizers — SEO Performance Fixes

**Priority**: High | **Source**: SEOptimer audit + GSC comparison (Jun 27, 2026)

## Context
- Mobile PageSpeed: 60/100, LCP: 12.9s (target: <2.5s)
- Desktop PageSpeed: 83/100
- Total page size: ~2.9MB (images: 2.48MB)
- All images are uncompressed JPEGs in `brentwood/` root

## Action Items

### 1. Convert images to WebP + add fetchpriority (LCP fix) — **HIGH**
- `Living Room.jpeg` (1.1MB) → hero image, LCP element — add `fetchpriority="high"`
- `Bedroom.jpeg` (670K), `Closet 2.jpg` (860K), `Closet 3.jpeg` (719K), `Glasses.jpeg` (524K), `Linen Closet.jpeg` (205K), `Office.jpeg` (126K), `closet-2-flipped.jpg` (860K), `fort-lauderdale-office.jpg` (193K)
- Below-fold images get `loading="lazy"`
- Expected: page size 2.9MB → ~1MB, LCP 12.9s → ~3s

### 2. Fix redirect chain — **MEDIUM**
- SEOptimer flags "avoid multiple page redirects" (0.63s savings on mobile)
- Likely HTTP → HTTPS + www redirect cascade — check CNAME/GitHub Pages settings

### 3. Keyword optimization in headings — **MEDIUM**
- "home organization" missing from H2 tags (SEOptimer medium priority)
- "Brentwood" missing from meta description and headings
- Add "home organization" to a service section H2

### 4. Trim meta description — **LOW**
- Current: 183 chars (truncated in SERPs)
- Target: ~155 chars
- Suggested: "White-glove home organization for Miami's most discerning homes. Expert move-in, downsizing & relocation services in Coral Gables, Brickell & Miami Beach."

### 5. Obfuscate plain text email — **LOW**
- Plain text email found on page (spam risk)
- Replace with contact form link or JavaScript obfuscation

## Files
- Homepage: `brentwood/index.html`
- Images: `brentwood/*.jpeg`, `brentwood/*.jpg`
- Audit PDF: `scripts/seo/reports/SEOptimer_Audit_brentwood_20260627.pdf`
- Audit review: `scripts/seo/reports/SEOptimer_Review_brentwood_20260627.md`
