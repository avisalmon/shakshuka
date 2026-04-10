# Shakshuka Recipe Site — Rebuild with Verified Recipes Only

## Summary
Rebuild the shakshuka recipe site using ONLY real, verified recipes from accessible Israeli food sources. Every recipe must be validated against its actual source page — correct ingredients, exact quantities, real steps, real images. Delete all fabricated/unverifiable recipes. The site infrastructure (CSS, JS, HTML template, responsive layout, localStorage features) already exists and works — this rebuild focuses exclusively on recipe DATA INTEGRITY.

## Problem Statement — Why This Rewrite Is Needed
An audit of the existing 24 recipes revealed that **ALL recipe content is AI-generated fabrication**:
- Recipes attributed to real chefs/bloggers contain wrong ingredients, wrong quantities, and invented techniques
- Example: "Sarit Atar" recipe has 3 garlic cloves (real: 4), 4 eggs (real: 6), 1 tbsp paste (real: 2 tbsp), missing parsley & water
- Example: "Mutti" recipe is missing onion and peppers entirely, invents "caraway" and "spice paste technique" not in original
- 14 of 24 source URLs return 403/404 (dead pages, bot-blocked sites, ad redirects)
- 7 hashulchan.co.il URLs return 404 (pages don't exist)
- 4 mako.co.il URLs are generic category pages, not specific recipes
- All 24 images are generic Unsplash stock food photos unrelated to shakshuka
- The "Optimal Red Synthesis" recipe has no source at all (purely invented)

**The research report** (`research/deep-research-report.md`) is a useful INDEX of 22 recipe names, chef attributions, and cooking style descriptions — but it contains NO actual recipe data (no ingredient lists, no quantities, no step-by-step instructions). It is a GUIDE for discovering real sources, NOT a source of recipe content.

## Existing Site Infrastructure (PRESERVE — DO NOT REBUILD)
The following files are already working and should NOT be modified unless a recipe count change requires it:
- `css/style.css` — Full responsive CSS with dark mode, RTL, print layout
- `js/app.js` — Search, favorites, shopping list, localStorage features
- `index.html` — Landing page with category cards, search, hero
- `history.html`, `techniques.html`, `debates.html`, `favorites.html`, `about.html` — Content pages
- HTML recipe template pattern in `recipes/*.html` — Use as template for new pages
- Navigation, footer, breadcrumbs — All working

**What MUST be rebuilt:**
- `data/recipes.json` — Replace ALL entries with verified recipe data
- `recipes/*.html` — Regenerate from verified JSON data
- `images/recipes/*` — Replace with real images from sources
- `download_images.py` — Rewrite to download real images
- `index.html` recipe card section — Update to match new recipe count/slugs

## Tech Stack
- **Pure HTML / CSS / JavaScript** — no frameworks, no build tools, no npm
- **Python 3.11** (`.\env\Scripts\activate`) for build/validation scripts
- **GitHub Pages** compatible — `index.html` at repo root
- **localStorage** for user features (already implemented)

## Recipe Research & Validation Protocol

### Step 1: Source Discovery
For each of the 22 recipes named in the research report, find the ACTUAL source URL.
Use `fetch_webpage` with search queries like: `"שקשוקה" site:saritatar.net` or `"שקשוקה של אייל שני"`.

**Known accessible sources (verified working):**
- `https://mutti.co.il/recipe/shakshuka/` — Mutti cheese shakshuka (ACCESSIBLE)
- `https://saritatar.net/post/shakshuka` — Sarit Atar home-style (ACCESSIBLE)

**Known DEAD/BLOCKED sources (do NOT waste time retrying):**
- `hashulchan.co.il` — ALL URLs return 404
- `mako.co.il` — Returns 403 (bot-blocked with Akamai)
- `food.walla.co.il` — Redirects to ad tracker
- `ynet.co.il/food` — Redirects to ad tracker
- `chef-lavan.co.il` — Imperva CAPTCHA blocks access
- `foodish.anumuseum.org.il` — Returns 403

**Sites to try for additional real recipes:**
- `saritatar.net` — Israeli food blog (ACCESSIBLE)
- `mutti.co.il` — Mutti Israel recipes (ACCESSIBLE)
- `foody.co.il` — Large Israeli recipe site
- `10dakot.co.il` — Quick recipes (try for shakshuka)
- `sheilta.co.il` — Israeli cooking community
- `seriouseats.com` — English reference for technique validation
- Google search: `שקשוקה מתכון site:<domain>` for each chef name

### Step 2: Recipe Extraction (for each accessible source)
For each URL that returns an ACTUAL recipe page:
1. Fetch the page with `fetch_webpage`
2. Extract the COMPLETE recipe: all ingredients with EXACT quantities, all steps in order
3. Extract the recipe image URL (og:image or main recipe photo)
4. Record the chef/author name as shown on the page
5. Record the exact page title
6. Download the recipe image to `images/recipes/<slug>.jpg`

### Step 3: Data Validation
For each extracted recipe, verify:
- [ ] Source URL is accessible and returns a real recipe page (not 404, 403, or redirect)
- [ ] Recipe title matches the source page title
- [ ] ALL ingredients from source are present (no missing, no invented)
- [ ] ALL quantities match the source exactly (not approximated)
- [ ] ALL steps match the source (not reworded or invented)
- [ ] Image is downloaded from the source (not a stock photo)
- [ ] Author/chef name matches the source

### Step 4: Delete or Keep Decision
- **KEEP**: Recipe passes ALL validation checks above
- **DELETE**: Recipe fails ANY check (broken URL, can't access, data doesn't match)
- **MINIMUM TARGET: 8 verified recipes.** If fewer than 8 survive from the research report sources, Step 5 MUST find more until we reach at least 8. If after exhaustive searching the total is still below 8, log a prominent WARNING in knowledge.md — but do NOT fabricate recipes to fill the gap.

### Step 5: Search for Additional Real Recipes
If fewer than 12 recipes survive validation, search for more real shakshuka recipes.
Each new recipe must go through the SAME validation protocol (Steps 2-4).
Focus on variety: try to cover classic red, green, cheese, meat categories.

**Expanded discovery list — try ALL of these:**
- `foody.co.il` — Large Israeli recipe aggregator
- `10dakot.co.il` — Quick recipes
- `sheilta.co.il` — Israeli cooking community
- `osem.co.il` — Osem brand recipes (search for שקשוקה)
- `strauss-group.com` or `strauss.co.il` — Strauss brand recipes
- `tnuva.co.il` — Tnuva dairy recipes (שקשוקה with cheese)
- `al-hashulchan.co.il` — Food magazine (different from hashulchan.co.il)
- `seriouseats.com/shakshuka` — English reference
- `bonappetit.com` — Check for shakshuka
- `ottolenghi.co.uk` — Ottolenghi's shakshuka if available
- `foodnetwork.com` — Check for shakshuka
- Google search: `שקשוקה מתכון` and try the top 10 results that aren't in the dead list
- Google search: `shakshuka recipe` for international high-quality sources
- Look for recipes from: prominent Israeli chefs, popular food blogs, brand sites

## Recipe Data Model
Each verified recipe in `data/recipes.json` must have:
```json
{
  "id": 1,
  "slug": "sarit-atar-shakshuka",
  "titleHe": "שקשוקה ביתית של שרית עטר",
  "titleEn": "Sarit Atar's Home-Style Shakshuka",
  "author": "שרית עטר",
  "sourceUrl": "https://saritatar.net/post/shakshuka",
  "sourceVerified": true,
  "image": "images/recipes/sarit-atar-shakshuka.jpg",
  "imageSource": "saritatar.net",
  "category": "classic-red",
  "difficulty": "קל",
  "prepTime": "10 דקות",
  "cookTime": "20 דקות",
  "servings": 4,
  "ingredients": [
    {"item": "שמן זית", "amount": "3", "unit": "כפות"},
    {"item": "בצל", "amount": "1", "unit": "גדול"}
  ],
  "steps": [
    "חממו שמן זית במחבת רחבה על אש בינונית",
    "הוסיפו את הבצל הקצוץ וטגנו 5 דקות עד שמזהיב"
  ],
  "proTips": ["טיפ מקצועי מהמקור אם קיים"],
  "tags": ["קלאסית", "אדומה", "ביתית"]
}
```

**CRITICAL**: The `ingredients` and `steps` arrays must **faithfully represent** the data from the actual source page — same items, same quantities, same order. Translate to Hebrew if the source is in English. Always credit the source with `sourceUrl` and `author`. Do NOT invent ingredients, change quantities, or add steps that don't exist in the original.

## Images Strategy
1. **ONLY source**: Download the actual recipe image from the source page
2. **Method**: Find `og:image` meta tag or the main recipe photo `<img>` in the article
3. **Download**: Use Python `requests` to download to `images/recipes/<slug>.jpg`
4. **NO stock photos**: Do NOT use Unsplash, Pexels, or any generic images
5. **Fallback**: If source has no image, generate a CSS placeholder with recipe name — do NOT substitute a stock photo
6. **Hero images**: For the landing page, reuse one of the verified recipe images

## Build Scripts

### `scripts/validate_recipes.py`
Create this script to independently validate ALL recipes in `data/recipes.json`.
This is the GUARD against LLM drift — it re-fetches the source and compares:
- Fetch `sourceUrl` and verify it returns HTTP 200 (not redirect, 403, 404)
- Re-parse the source page to extract ingredient names and step count
- **DIFF CHECK**: Compare the number of ingredients in our JSON vs the source page. Flag if counts differ.
- **DIFF CHECK**: Compare the number of steps in our JSON vs the source page. Flag if counts differ.
- **INGREDIENT NAMES CHECK**: For each ingredient name in the source, check it appears (or a close Hebrew equivalent) in our JSON. Flag missing ingredients.
- Verify image file exists at the `image` path and is >10KB (not a broken download)
- Print a detailed PASS/FAIL report per recipe with specific mismatches listed
- At the end, print a SUMMARY: X passed, Y failed, Z warnings
- Exit with non-zero code if any recipe fails
- **Write the full report to `state/validation_report.txt`** so Avi can review it

### `scripts/build_recipe_pages.py`
Create this script to generate `recipes/<slug>.html` from `data/recipes.json`:
- Read the existing recipe HTML template pattern from a working recipe page
- For each recipe in JSON, generate the HTML page
- Ensure RTL, Hebrew, and all interactive features work

### `scripts/download_images.py` (rewrite existing)
Rewrite to download images from verified source URLs (not Unsplash IDs).

### `scripts/update_index.py`
Update `index.html` recipe cards to match the new verified recipe list.

## Site Design (PRESERVE EXISTING)
The visual design is already done and working:
- **Color palette**: Warm Mediterranean tones (tomato red, egg yolk, olive green, warm cream, cast iron dark)
- **Typography**: Rubik (Hebrew), clean sans-serif body
- **RTL**: Full Hebrew RTL support with `dir="rtl"`
- **Responsive**: Mobile 320px through desktop 1440px
- **Dark mode**: CSS `prefers-color-scheme` with toggle
- **Features**: Search, favorites, shopping list, print, double-qty — all working in `js/app.js`

Only modify design files if recipe count change requires index.html card updates.

## Iteration Plan

### Iteration 1 — Research & Source Discovery
- Read `state/knowledge.md` and `state/plan.md`
- Read the research report `research/deep-research-report.md` for the 22 recipe names and attributions
- For each recipe, search for the REAL source URL using `fetch_webpage`
- Test each URL: accessible (200) vs dead (404/403/redirect)
- ALSO search the expanded discovery list for additional shakshuka recipes beyond the 22
- Record ALL findings in `state/knowledge.md`: URL, status, accessible yes/no
- Build a triage list: which recipes can be verified, which are dead, which are new finds
- Count accessible recipes. If below 8, flag a WARNING in knowledge.md.
- Update dashboard

### Iteration 2 — Recipe Extraction + Validation + Gap Filling
- For each ACCESSIBLE source URL from Iteration 1:
  - Fetch the page and extract the COMPLETE recipe (ingredients, quantities, steps)
  - Download the recipe image from the source
  - Build the recipe JSON entry
- If fewer than 12 recipes extracted, search for MORE from the expanded discovery list
- Write ALL verified recipes to `data/recipes.json` (REPLACE the entire file)
- Create `scripts/validate_recipes.py` (see Build Scripts section)
- Run validation script — fix any failures
- Delete `images/recipes/*` old stock photos, replace with downloaded real images
- Record validation results in `state/knowledge.md`
- **HUMAN REVIEW CHECKPOINT**: Write `state/review_table.md` with a comparison table:
  | Recipe | Source URL | Our Ingredients Count | Source Ingredients Count | Our Steps Count | Source Steps Count | Image? | Status |
  This table lets Avi verify the extraction quality before page generation proceeds.
- Update dashboard

### Iteration 3 — Build Recipe Pages + Site Integration
- Run `scripts/build_recipe_pages.py` to generate `recipes/<slug>.html` for all verified recipes
- Remove old recipe HTML pages that no longer exist in the verified JSON
- Run `scripts/update_index.py` to update `index.html` recipe cards
- Update category counts and any hardcoded recipe references in nav/footer
- Verify all links work: recipe cards → recipe pages → source URLs
- Verify images display correctly on each page
- Update dashboard

### Iteration 4 — End-to-End Verification + Fixes
- Run `scripts/validate_recipes.py` as independent re-check
- Open each recipe page URL and verify:
  - Content renders correctly (Hebrew RTL, ingredients, steps)
  - Source link is clickable and loads the real source
  - Image displays (not broken)
  - Responsive layout works with new recipe count
- Fix any issues found
- Re-run validation script — must be 0 failures
- Update dashboard

### Iteration 5 — Final Review + Summary
- Final run of `scripts/validate_recipes.py` — ALL must PASS
- Write Self-Observation
- Send Summary Email
- Final dashboard update + upload

## Constraints
- **ZERO tolerance for fabricated content** — every ingredient, quantity, and step must faithfully represent the actual source page
- Do NOT use the research report as a source of recipe data — it contains NO quantities or step-by-step instructions
- Do NOT use Unsplash, Pexels, or any stock photo service
- Do NOT invent recipes, pro tips, or cooking techniques
- Do NOT keep broken source URLs — if the source returns 404/403, DELETE that recipe
- **MINIMUM 8 verified recipes** — if below 8 after exhaustive search, log WARNING but do not fabricate
- Integrity over quantity — but a recipe site needs enough content to be useful
- NO external JavaScript frameworks (no React, Vue, jQuery)
- GitHub Pages compatible (static files only)
- Hebrew text must render correctly with proper RTL support
- Python scripts run in `.\env\Scripts\activate` virtual environment
- **Copyright**: Always attribute the original author and source URL. Do not claim recipes as original content.

## Definition of Done
- [ ] At least 8 verified recipes in `data/recipes.json` (all with `sourceVerified: true`)
- [ ] ALL source URLs return 200 when fetched
- [ ] ALL recipe ingredients and steps faithfully represent the actual source page content
- [ ] ALL recipe images are downloaded from actual source pages (no stock photos)
- [ ] `scripts/validate_recipes.py` passes with 0 failures
- [ ] `state/validation_report.txt` exists with full pass/fail details
- [ ] `state/review_table.md` exists with source vs extracted comparison table
- [ ] Recipe HTML pages generated from verified JSON data
- [ ] `index.html` updated with correct recipe cards
- [ ] Old unverified recipe pages and images are deleted
- [ ] Site loads and works from `index.html` with no server
- [ ] Summary email composed via Outlook COM

## State Management
- Read `state/knowledge.md` and `state/plan.md` at the START of each iteration
- Write progress to `state/knowledge.md` at the END of each iteration
- Do NOT repeat work already recorded in knowledge.md

## Self-Observation (every iteration)
At the end of each iteration, read `state/agent_raw.jsonl` and observe:
- How many tool rounds did you use? Were any wasted on repeated searches?
- Did you hit the round cap? What can be done more efficiently?
- Are your prompts and definitions effective or should they be adapted?
Write observations to `state/knowledge.md` under a `## Self-Observation` heading.
Learn from your observations and adapt your approach in subsequent iterations.

## Summary Email (final iteration only)
At the end of the LAST iteration, compose a summary email to avi.salmon@intel.com.
Use Outlook PowerShell COM — NEVER use Graph API:
```powershell
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.Subject = "Shakshuka Recipe Site — AutoAgent Run Summary"
$mail.To = "avi.salmon@intel.com"
$mail.HTMLBody = "<html>...</html>"
$mail.Display()   # NEVER call $mail.Send() — always Display() for review
```
The email must cover:
- What was built (deliverables produced)
- Results (tests passed/failed, synthesis results, etc.)
- Per-iteration progression (what each iteration accomplished)
- Total time, tokens, iterations used
- Recommendations: what to fix or improve for the next AutoAgent run

## Dashboard (every iteration)
Before ending each iteration, create or update `dashboard.html` — a beautiful single-page HTML dashboard summarizing:
1. **Purpose**: What this project is building
2. **Accomplishments so far**: What has been completed
3. **Future plans**: What remains
4. **Workflow visualization**: A visual timeline/flowchart showing per-iteration work and cross-iteration dependencies
   - Use inline SVG or CSS-based diagrams (no external dependencies)
   - Color-code: green=done, blue=in-progress, gray=planned

Style: modern, clean, dark header with project name, card-based layout, responsive.

After creating/updating the dashboard, upload it:
```powershell
$slug = "shakshuka"
$html = Get-Content "dashboard.html" -Raw
$body = @{ slug = $slug; html_content = $html } | ConvertTo-Json -Depth 10
Invoke-RestMethod -Method POST -Uri "http://143.185.126.57:8000/pages" -ContentType "application/json" -Body $body
```
If the upload fails (server unreachable), log a warning but do not fail the iteration.
