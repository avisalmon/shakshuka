# Knowledge Base

## Pre-Run Audit Findings
- ALL 24 existing recipes are AI-generated fabrications — NOT from real sources
- Only 2 source URLs confirmed accessible: mutti.co.il/recipe/shakshuka/ and saritatar.net/post/shakshuka
- Dead sources: hashulchan (404), mako (403), ynet (redirect), walla (redirect), chef-lavan (CAPTCHA)
- All 24 images are generic Unsplash stock photos — unrelated to shakshuka
- Site infrastructure (CSS, JS, pages, responsive, dark mode, print) is complete and working
- This run focuses ONLY on recipe data integrity — research, validate, rebuild with verified content

## Iteration 1 — Source Discovery Results

### Verified Accessible Sources (10 recipes with full data)

| # | Slug | Title (He) | Title (En) | Author | Source URL | Category | Status |
|---|------|-----------|-----------|--------|-----------|----------|--------|
| 1 | mutti-shakshuka | שקשוקה של Mutti | Mutti's Shakshuka | Mutti Israel | https://mutti.co.il/recipe/shakshuka/ | cheese | ✅ |
| 2 | sarit-atar-shakshuka | שקשוקה שכולם אוהבים | Sarit Atar's Home-Style Shakshuka | שרית עטר | https://saritatar.net/post/shakshuka | classic-red | ✅ |
| 3 | 10dakot-shakshuka | מתכון לשקשוקה טעימה | 10 Dakot Classic Shakshuka | אפרת סיאצ'י | https://www.10dakot.co.il/recipe/מתכון-לשקשוקה/ | classic-red | ✅ |
| 4 | 10dakot-kids-shakshuka | שקשוקה לילדים | Kids' Shakshuka | אפרת סיאצ'י | https://www.10dakot.co.il/recipe/שקשוקה-לילדים/ | classic-red | ✅ |
| 5 | bishulim-shakshuka | שקשוקה מקושקשת | Bishulim Scrambled Shakshuka | נטלי שמעוני | https://www.bishulim.co.il/מתכון/שקשוקה | classic-red | ✅ |
| 6 | downshiftology-shakshuka | שקשוקה מסורתית | Downshiftology Traditional Shakshuka | Lisa Bryan | https://downshiftology.com/recipes/shakshuka/ | classic-red | ✅ |
| 7 | love-and-lemons-shakshuka | שקשוקה מיטבית | Love and Lemons Best Shakshuka | Jeanine Donofrio | https://www.loveandlemons.com/shakshuka-recipe/ | classic-red | ✅ |
| 8 | mediterranean-dish-shakshuka | שקשוקה ים-תיכונית | Mediterranean Dish Shakshuka | Suzy Karadsheh | https://www.themediterraneandish.com/shakshuka/ | classic-red | ✅ |
| 9 | tori-avey-shakshuka | שקשוקה של טורי אייבי | Tori Avey's Shakshuka | Tori Avey | https://toriavey.com/shakshuka/ | classic-red | ✅ |
| 10 | recipetineats-shakshuka | שקשוקה ביצים ברוטב עגבניות | RecipeTin Eats Shakshuka | Nagi Maehashi | https://www.recipetineats.com/shakshuka/ | classic-red | ✅ |

### Dead/Blocked Sources (DO NOT RETRY)
- hashulchan.co.il — ALL URLs return 404
- mako.co.il — Returns 403 (Akamai bot-block)
- food.walla.co.il — Redirects to ad tracker
- ynet.co.il/food — Redirects to ad tracker
- chef-lavan.co.il — Imperva CAPTCHA blocks
- foodish.anumuseum.org.il — Returns 403
- seriouseats.com/shakshuka-recipe — Returns 404
- bonappetit.com/recipe/shakshuka — Content extraction failed
- foodnetwork.com — Content extraction failed
- minimalistbaker.com — Content extraction blocked
- natashaskitchen.com — Returns 404
- osem.co.il — Redirects to corporate page, no recipes
- tnuva.co.il — Content extraction failed
- foody.co.il — Content extraction failed

### Recipe Data Extracted (Summary per Source)

**1. Mutti (mutti.co.il):** Servings: 4-5 | Time: 20 min | Ingredients: 2T oil, 1 onion, 2 garlic, 1 red pepper, ½ hot pepper, cherry tomatoes, 1 can Polpa, 1T paste, ⅓ cup water, 4-5 eggs; Seasoning mix, feta/mozzarella garnish

**2. Sarit Atar:** Servings: ~4 | Ingredients: 1 onion, 5T oil, 6 tomatoes, 1 pepper, 4 garlic, 1T paprika, 1t salt, 2T paste, ½ cup water, 6 eggs, parsley

**3. 10 Dakot Classic:** Servings: 2-3 | Ingredients: 1 onion, 4 tomatoes, ½ bell pepper, 3-4 garlic, 1T paste, 4 eggs; paprika, salt, pepper

**4. 10 Dakot Kids:** Servings: 2-3 | Ingredients: ½ onion grated, 1 garlic, 1 tomato grated, 1T paste, 2-3 eggs; sugar, salt, paprika

**5. Bishulim:** Servings: 2 | Ingredients: 2 garlic, 3 tomatoes grated, 2 eggs, paprika, salt, pepper (scrambled style)

**6. Downshiftology:** Servings: 6 | Ingredients: 2T oil, 1 onion, 1 bell pepper, 4 garlic, paprika, cumin, chili powder, 28oz canned tomatoes, 6 eggs

**7. Love and Lemons:** Servings: 4 | Ingredients: 2T oil, 1 onion, 1 bell pepper, 3 garlic, cumin, paprika, cayenne, 28oz fire-roasted crushed tomatoes, 6 eggs

**8. Mediterranean Dish:** Servings: 6 | Ingredients: 3T oil, 1 onion, 2 green peppers, 2 garlic, coriander, paprika, cumin, 6 fresh tomatoes, ½ cup tomato sauce, 6 eggs, parsley, mint

**9. Tori Avey:** Servings: 6 | Ingredients: 1T oil, ½ onion, 1 garlic, 1 bell pepper, 4 cups tomatoes, 2T paste, spices, 6 eggs

**10. RecipeTin Eats:** Servings: 2-3 | Ingredients: 2T oil, 1 onion, 1 garlic, 1 bell pepper, 1 tomato, 400g can, 1T paste, ½ cup broth, spices, 4 eggs

### Category Distribution
- Classic Red: 9 recipes (#2-10)
- Cheese: 1 recipe (#1 Mutti)
- Green/Meat/Fusion: 0 found accessible

## Self-Observation — Iteration 1
- Tool rounds used: ~12 (read files + 10+ fetch calls + 1 subagent)
- Efficient use of parallel fetches saved rounds
- Subagent for batch URL testing was very efficient
- Dead sources identified quickly and not retried
- 10 verified recipes exceeds minimum target of 8
- Gap: Most recipes are "classic red" — no green/meat/fusion accessible

## Iteration 3 — Build Recipe Pages + Site Integration

### Completed Tasks
1. **Created `scripts/build_recipe_pages.py`** — Generates recipe HTML pages from `data/recipes.json`
   - Full template with nav, hero, breadcrumbs, meta bar, ingredients, steps, pro tips, notes, shopping list, double qty toggle, related recipes, footer
   - Automatic deletion of orphaned recipe pages
   
2. **Generated 10 verified recipe HTML pages**:
   - mutti-shakshuka.html, sarit-atar-shakshuka.html, 10dakot-shakshuka.html, 10dakot-kids-shakshuka.html, bishulim-shakshuka.html, downshiftology-shakshuka.html, love-and-lemons-shakshuka.html, mediterranean-dish-shakshuka.html, tori-avey-shakshuka.html, recipetineats-shakshuka.html

3. **Deleted 24 old fabricated recipe pages** — All unverified pages removed

4. **Cleaned up images** — Only 10 verified images remain (downloaded from real sources)

5. **Created `scripts/update_index.py`** — Updates index.html with verified recipe data
   
6. **Updated `index.html`**:
   - Meta descriptions updated: "10 מתכונים מאומתים ממקורות אמיתיים"
   - Hero text: "10 מתכונים מאומתים ממקורות אמיתיים"
   - Category cards: classic-red=9, cheese=1 (מתכון אחד), green/meat/fusion= "בקרוב"
   - Featured recipe: Sarit Atar's shakshuka (replacing deleted "optimal red synthesis")
   - Inlined recipe data array: replaced 24 fabricated entries with 10 verified
   - Footer text updated

7. **Verified integrity**:
   - No stale references to deleted recipe slugs in any HTML file
   - All 10 recipe pages have correct source URLs, ingredient counts, step counts
   - All 10 images are valid JPEG files (sizes: 9KB to 2.6MB)
   - Validation script: 10/10 PASS, 0 FAIL

8. **Created reports**:
   - `state/validation_report.txt` — Full validation details per recipe
   - `state/review_table.md` — Source vs extracted comparison table
   - `scripts/gen_reports.py` — Report generation script

### Site Status After Iteration 3
- **Recipe Pages**: 10 verified (was: 24 fabricated)
- **Images**: 10 from real sources (was: 24 Unsplash stock photos)
- **Index.html**: Updated with correct data
- **All features working**: Nav, search, favorites, shopping list, dark mode, print, double qty

## Self-Observation — Iteration 3
- Tool rounds used: ~15 (read state, write script, run build, update index, verify, reports)
- Efficient: Created scripts that handle both generation and cleanup in one pass
- Build_recipe_pages.py auto-deletes orphans — no manual cleanup needed
- Update_index.py handles all count/text/data replacement in one Python pass
- PowerShell here-string (@'...'@) was reliable for writing Python scripts with embedded f-strings
- Validation script from Iteration 2 confirmed all 10 recipes pass
- No surprises — clean execution
