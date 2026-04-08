# Shakshuka Recipe Site — שקשוקה

## Summary
Build a stunning, mouth-watering static recipe website about Shakshuka (שקשוקה), hosted on GitHub Pages. The site is based on comprehensive deep research (see `research/deep-research-report.md`) covering 22+ Israeli recipes, historical origins, technique analysis, and expert tips. The site must be fully responsive (desktop + mobile), visually tempting, and feel like a premium food magazine.

## Source Material
- `research/deep-research-report.md` — Deep research report containing 22 recipes, historical context, technique breakdowns, ingredient analysis, and expert tips. This is the AUTHORITATIVE source for all content. Do NOT invent recipes — extract them from this file.

## Tech Stack
- **Pure HTML / CSS / JavaScript** — no frameworks, no build tools, no npm
- **GitHub Pages** compatible — `index.html` at repo root
- Fully static — no server, no database
- **localStorage** for user features (comments, modifications, favorites)

## Site Structure

### Pages
1. **Landing page** (`index.html`) — Hero image/video, tagline in Hebrew + English, category cards (Classic Red, Green, Cheese, Meat, Fusion), search bar, "most popular" highlights
2. **Recipe pages** (`recipes/<slug>.html`) — One page per recipe from the research. Each recipe page includes:
   - Recipe title (Hebrew + English)
   - Hero photo (fetched from source site or high-quality stock — see Images section)
   - Source attribution with clickable link to original recipe
   - Chef/author name and credit
   - Difficulty, prep time, cook time, servings
   - Ingredient list (with checkboxes for shopping list)
   - Step-by-step instructions with technique tips from the research
   - "Pro Tips" callout boxes extracted from the research's expert analysis
   - User notes section (localStorage — user can add personal modifications)
   - Star rating (localStorage — personal rating)
   - "I Made This" photo upload placeholder (localStorage base64, small images only)
   - Related recipes sidebar
3. **History & Culture** (`history.html`) — The origins section from the research: North African roots, migration to Israel, name etymology, the "national dish" debate
4. **Techniques** (`techniques.html`) — Key techniques from the research: spice blooming, sauce reduction, egg control (lid vs no lid), tomato quality, make-ahead tips
5. **The Great Debates** (`debates.html`) — Fun interactive page about Israeli Shakshuka controversies: onion or no onion? cheese? lid? Fresh vs canned tomatoes? With poll-style localStorage voting
6. **Favorites** (`favorites.html`) — User's saved favorite recipes (localStorage)
7. **About** (`about.html`) — Credits, source links, Avi Salmon credit

### Navigation
- Sticky top nav with logo, search, category dropdown, favorites count badge
- Mobile: hamburger menu with smooth slide-in
- Breadcrumbs on recipe pages
- Footer with all recipe links organized by category

## Recipes to Include (from research)

Extract ALL 22 recipes from the research report. Organize by category:

### Classic Red (שקשוקה קלאסית אדומה)
1. Classic Shakshuka — Orly Peli-Bronstein & Shay Lee Lipa
2. Eyal Shani's Minimalist Shakshuka
3. Rafi Cohen's Chef Shakshuka
4. "The Best Recipe" (no-onion, baking soda trick)
5. Quick Canned Shakshuka — Rotem Liberzon
6. Bino Gabso's "Dr. Shakshuka" Classic
7. Racheli Krut's "Most Delicious Shakshuka"
8. Sarit Atar's Home-style Shakshuka
9. Kids-Friendly Shakshuka — Anat Label
10. Shakshuka with Potatoes — Ron Yochananov

### Green (שקשוקה ירוקה)
11. Spinach & Feta Shakshuka — Shir Halpern
12. Spinach-Mushroom with Mozzarella & White Wine

### With Cheese (שקשוקה עם גבינות)
13. Bulgarian Cheese Shakshuka — HaShef HaLavan
14. Cheese Shakshuka — Mutti
15. Community/Museum Recipe — Simcha Yosef (ANU/FOODISH)

### With Meat (שקשוקה עם בשר)
16. Shakshuka with Merguez — Rafi Cohen

### Fusion & Modern (פיוז'ן)
17. Thai Green Shakshuka-Curry
18. Italian Shakshuka — Eitan Acqua
19. Single-Pan Shakshuka — Moshik Roth
20. Eggplant & Vegan Cheese Shakshuka — Christoph Steiner
21. Eggplant Shakshuka — Leiza Panels
22. Yolk-Only Shakshuka — Hila Alpert
23. Jerusalem "Scrambled" Shakshuka — Edi Mizrachi (MasterChef)

### Synthesis Recipe
24. Optimal Red Shakshuka — synthesized from the research's cross-recipe analysis

## Images Strategy
For each recipe, try to fetch a representative image:
1. **First choice**: Fetch the source recipe URL and look for an og:image or main recipe image. Download it to `images/recipes/` and use locally.
2. **Second choice**: Use a high-quality placeholder from Unsplash/Pexels (shakshuka, eggs in tomato sauce, etc.) with proper attribution.
3. **Fallback**: Generate a beautiful CSS gradient placeholder with the recipe name in Hebrew calligraphy.
4. Hero/landing images: Find 3-5 stunning shakshuka photos for the landing page carousel.

Use `fetch_webpage` to find images from original source URLs in the research.

## Source Links
The research references these sources. Find and link to the original recipe URLs:
- Orly Peli-Bronstein / Shay Lee Lipa recipe site
- Eyal Shani recipe
- Rafi Cohen recipe
- Rotem Liberzon recipe
- Bino Gabso / Dr. Shakshuka
- Shir Halpern recipe
- HaShef HaLavan (Bulgarian shakshuka)
- Christoph Steiner recipe
- Racheli Krut blog
- Sarit Atar blog
- Mutti Israel recipe
- Leiza Panels blog
- Ron Yochananov recipe
- Eitan Acqua recipe
- Moshik Roth recipe
- Hila Alpert recipe
- Anat Label recipe
- Edi Mizrachi / MasterChef recipe
- ANU Museum / FOODISH archive
- Serious Eats (spice technique reference)
- The Kitchen Coach (Hebrew technique reference)

Use `fetch_webpage` to locate the actual URLs for each. If a URL cannot be found, note it prominently in knowledge.md.

## Design Requirements

### Visual Identity
- **Color palette**: Warm Mediterranean — deep tomato red (#C0392B), golden egg yolk (#F39C12), olive green (#27AE60), warm cream (#FFF5E6), cast iron dark (#2C3E50)
- **Typography**: Use Google Fonts — a display font for headings (e.g., Playfair Display or similar elegant serif), clean sans-serif for body (e.g., Inter or Rubik for Hebrew support)
- **Hebrew support**: All recipe titles in Hebrew AND English. History page primarily in Hebrew with English translations. Use `dir="rtl"` where appropriate.
- **Photography-forward**: Large hero images, recipe cards with photo backgrounds, minimal text overlays with good contrast
- **Micro-animations**: Subtle hover effects on recipe cards, smooth scroll, ingredient checkbox animations, rating star fill animation
- **Dark mode**: CSS `prefers-color-scheme` support with manual toggle

### Mobile-First Responsive
- Breakpoints: 320px (phone), 768px (tablet), 1024px (desktop), 1440px (wide)
- Recipe cards: 1 column phone, 2 tablet, 3-4 desktop
- Sticky nav collapses to hamburger on mobile
- Touch-friendly: large tap targets, swipe-friendly carousel
- Images: responsive `srcset` or CSS `object-fit` for different screen sizes

### Interactive Features (all localStorage)
1. **Search**: Client-side full-text search across recipe names, ingredients, categories, and tags. Instant results as you type.
2. **Favorites**: Heart icon on each recipe card and page. Favorites page shows saved recipes.
3. **User Notes**: Per-recipe textarea for personal modifications ("I added za'atar", "used canned tomatoes"). Persisted in localStorage.
4. **Star Rating**: 1-5 star personal rating per recipe.
5. **Shopping List**: Check ingredients on a recipe → accumulate into a shopping list view. Export as text.
6. **The Great Debates Voting**: Fun polls ("Onion or no onion?", "Lid on or off?", "Fresh or canned?", "Cheese: yes or heresy?") with animated bar charts showing YOUR votes (localStorage).
7. **Recently Viewed**: Track last 5 viewed recipes for quick access.
8. **Print-friendly**: CSS print stylesheet for clean recipe printing (no nav, no ads, just recipe).

## Iteration Plan

### Iteration 1 — Foundation
- Create site structure: index.html, template system, CSS framework, nav, footer
- Build recipe data model (JSON file with all 22+ recipes extracted from research)
- Implement 3-4 classic red recipes as proof of concept
- Landing page with hero, category cards, search bar skeleton
- Mobile-responsive layout

### Iteration 2 — All Recipes + Images
- Extract and create ALL remaining recipes from the research
- Fetch source URLs and images for each recipe
- Recipe detail pages with full content
- Source attribution links
- Related recipes logic

### Iteration 3 — Content Pages + Features
- History & Culture page
- Techniques page
- The Great Debates page (with voting)
- localStorage features: favorites, user notes, ratings, recently viewed
- Search implementation

### Iteration 4 — Polish + Advanced Features
- Shopping list feature
- Print stylesheet
- Dark mode
- Micro-animations and transitions
- Performance optimization (lazy loading images)
- Favorites page
- About page with credits

### Iteration 5 — Final Review + Summary
- Cross-browser testing (fix any issues)
- Accessibility check (alt text, ARIA labels, keyboard nav)
- Final content review — verify all 22+ recipes present and accurate
- Verify all source links work
- Self-observation and summary email

## Constraints
- NO external JavaScript frameworks (no React, Vue, jQuery)
- NO build tools (no webpack, vite, npm)
- ALL content extracted from the deep research report — do not invent recipes
- GitHub Pages compatible (static files only, index.html at root)
- Images must be stored locally in `images/` (not hotlinked from other sites)
- Hebrew text must render correctly with proper RTL support
- Must work offline after first load (all assets local except Google Fonts)

## Definition of Done
- [ ] 22+ recipe pages, each with full content from the research
- [ ] Landing page with hero, categories, search, and highlights
- [ ] History, Techniques, Debates, Favorites, About pages complete
- [ ] All localStorage features working (favorites, notes, ratings, search, votes, shopping list)
- [ ] Fully responsive on phone (320px) through desktop (1440px)
- [ ] Source attribution links on every recipe
- [ ] At least 15 recipes have real images (fetched or stock)
- [ ] Dark mode toggle works
- [ ] Print stylesheet produces clean output
- [ ] Site loads and works from `index.html` with no server

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
