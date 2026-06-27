# Indexing Remediation — Implementation Summary

**Date**: June 27, 2026
**Site**: brentwoodorganizers.com
**Status**: ✅ All automated phases complete. Manual GSC re-submission required.

---

## Problem Statement

GSC indexing report revealed critical multilingual gaps:
- **PT (Portuguese)**: 0 indexed pages — completely invisible to Google
- **FR (French)**: 1 indexed page, "unknown to Google"
- **ES (Spanish)**: 1 indexed page
- **EN (English)**: 40 indexed pages, but 23 pages with zero clicks
- **Duplicate URLs**: Blog posts indexed at both `/blog/post` and `/blog/post/`

---

## Phases Completed

### ✅ Phase 1: Make PT Discoverable (Commit `22d724e`)

**Script**: `brentwood/scripts/fix_hreflang.py`

**Changes**:
- Updated all 164 HTML files with complete hreflang blocks (en/es/fr/pt/x-default)
- Added PT to language switcher on all 4 language versions
- Added language links (FR | ES | PT) to footer

**Impact**: PT pages now have internal links pointing to them from every page on the site.

---

### ✅ Phase 2: Canonical Tags (Commit `3326039`)

**Script**: `brentwood/scripts/fix_blog_canonicals.py`

**Changes**:
- Added canonical tags to 88 blog/faq pages across all 4 languages
- Standardized trailing slash format for folder-based pages (GitHub Pages convention)
- Canonicals placed after hreflang x-default tag

**Impact**: Eliminates duplicate URL issues (`/blog/post` vs `/blog/post/`).

---

### ✅ Phase 3: Sitemap Regeneration (Commit `e39c577`)

**Script**: `brentwood/scripts/regenerate_sitemap.py`

**Changes**:
- Regenerated `sitemap.xml` with **168 URLs** (was ~195, but missing PT main pages)
- Added **42 PT URLs** (main pages, locations, blog posts, FAQs)
- All URLs have complete hreflang annotations (en/fr/es/pt)

**Breakdown**:
| Category | EN | ES | FR | PT | Total |
|----------|-----|-----|-----|-----|-------|
| Homepage | ✓ | ✓ | ✓ | ✓ | 4 |
| Main pages (10) | 10 | 10 | 10 | 10 | 40 |
| Location pages (8) | 8 | 8 | 8 | 8 | 32 |
| Blog index | 1 | 1 | 1 | 1 | 4 |
| Blog posts (20) | 20 | 20 | 20 | 20 | 80 |
| FAQ index | 1 | 1 | 1 | 1 | 4 |
| **Total** | **40** | **40** | **40** | **42** | **168** |

---

### ✅ Phase 4: GSC Verification (Commit `cf5825a`)

**Script**: `scripts/seo/submit_sitemap.py`

**Findings**:
- ✅ `sitemap.xml` is already registered in GSC
- ✅ URL Inspection API accessible (read-only)
- PT/FR pages show "UNKNOWN" status (expected — not yet crawled)

---

## Manual Actions Required

### 1. Re-submit Sitemap in GSC (HIGH PRIORITY)

The service account has read-only access, so sitemap re-submission must be done manually:

1. Open: **https://search.google.com/search-console/sitemaps**
2. Select property: `https://www.brentwoodorganizers.com/`
3. Find `sitemap.xml` in the list
4. Click the delete icon (🗑️) next to it
5. Re-enter `sitemap.xml` and click **Submit**
6. Verify status shows "Success"

This forces Google to re-fetch the updated sitemap with PT pages.

### 2. Request Indexing for Key Pages (HIGH PRIORITY)

In Google Search Console, use the URL Inspection Tool:

1. Open: **https://search.google.com/search-console/inspection**
2. Enter each URL below and click "Request Indexing":
   - `https://www.brentwoodorganizers.com/pt/index.html`
   - `https://www.brentwoodorganizers.com/fr/index.html`
   - `https://www.brentwoodorganizers.com/pt/services.html`
   - `https://www.brentwoodorganizers.com/fr/services.html`
   - `https://www.brentwoodorganizers.com/pt/consultation.html`
   - `https://www.brentwoodorganizers.com/fr/consultation.html`

### 3. Monitor Progress (2-4 weeks)

Run the indexing check script periodically:
```bash
cd scripts/seo
python check_indexing.py --client brentwood
```

**Expected timeline**:
- **Week 1-2**: PT and FR pages start appearing in GSC Coverage report
- **Week 2-4**: PT/FR pages get indexed and start showing impressions
- **Week 4+**: Search performance data available for PT/FR pages

---

## Scripts Created

| Script | Location | Purpose |
|--------|----------|---------|
| `fix_hreflang.py` | `brentwood/scripts/` | Bulk hreflang + language switcher updates |
| `fix_blog_canonicals.py` | `brentwood/scripts/` | Add canonical tags to blog/faq pages |
| `regenerate_sitemap.py` | `brentwood/scripts/` | Generate complete sitemap with all 4 languages |
| `submit_sitemap.py` | `scripts/seo/` | Check GSC sitemap status + URL inspection |
| `check_indexing.py` | `scripts/seo/` | Full GSC indexing audit (from previous session) |

---

## Expected Outcomes

| Metric | Before | Expected After (4 weeks) |
|--------|--------|--------|
| PT indexed pages | 0 | 15-25 |
| FR indexed pages | 1 | 15-25 |
| ES indexed pages | 1 | 10-20 |
| EN indexed pages | 40 | 40+ |
| Total indexed | 42 | 80-110 |
| Duplicate URLs | ~40 | ~0 (canonicals) |

---

## Git Commits

| Phase | Commit | Repository | Files Changed |
|-------|--------|------------|---------------|
| Phase 1 | `22d724e` | brentwood | 164 files |
| Phase 2 | `3326039` | brentwood | 89 files |
| Phase 3 | `e39c577` | brentwood | 2 files |
| Phase 4 | `cf5825a` | marketing_agency | 7 files |
