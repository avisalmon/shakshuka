#!/usr/bin/env python3
"""Update index.html with verified recipe data from recipes.json."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES_JSON = os.path.join(ROOT, "data", "recipes.json")
INDEX_HTML = os.path.join(ROOT, "index.html")

def main():
    with open(RECIPES_JSON, "r", encoding="utf-8") as f:
        recipes = json.load(f)
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    n = len(recipes)
    print(f"Loaded {n} recipes")

    # Count categories
    cats = {}
    for r in recipes:
        c = r.get("category", "classic-red")
        cats[c] = cats.get(c, 0) + 1
    print(f"Categories: {cats}")

    # 1. Fix meta description
    html = html.replace("24 מתכוני שקשוקה מהשפים והבשלנים הטובים בישראל. קלאסית אדומה, ירוקה, עם גבינות, עם בשר ופיוז'ן.",
                         f"{n} מתכוני שקשוקה מאומתים ממקורות אמיתיים. קלאסית אדומה ועם גבינות.")
    html = html.replace("24 מתכוני שקשוקה מהשפים הטובים בישראל.",
                         f"{n} מתכוני שקשוקה מאומתים ממקורות אמיתיים.")

    # 2. Fix hero text
    html = html.replace("24 מתכונים מהשפים והבשלנים הטובים ביותר",
                         f"{n} מתכונים מאומתים ממקורות אמיתיים")
    html = html.replace("חיפוש ב-24 מתכונים", f"חיפוש ב-{n} מתכונים")

    # 3. Fix category cards
    # Classic red image
    first_classic = next((r for r in recipes if r["category"]=="classic-red"), recipes[0])
    html = html.replace("images/recipes/classic-shakshuka-orly-shaylee.jpg", first_classic["image"])
    classic_count = cats.get("classic-red", 0)
    html = html.replace('<span class="category-card-count">11 מתכונים</span>',
                         f'<span class="category-card-count">{classic_count} מתכונים</span>')

    # Green - 0 recipes now
    green_count = cats.get("green", 0)
    html = html.replace("images/recipes/spinach-feta-shir-halpern.jpg", first_classic["image"])
    html = html.replace('<span class="category-card-count">2 מתכונים</span>',
                         f'<span class="category-card-count">{green_count} מתכונים</span>' if green_count else
                         '<span class="category-card-count">בקרוב</span>')

    # Cheese
    cheese_recipe = next((r for r in recipes if r["category"]=="cheese"), None)
    cheese_count = cats.get("cheese", 0)
    if cheese_recipe:
        html = html.replace("images/recipes/bulgarian-cheese-hashef-halavan.jpg", cheese_recipe["image"])
    html = html.replace('<span class="category-card-count">3 מתכונים</span>',
                         f'<span class="category-card-count">{"מתכון אחד" if cheese_count==1 else f"{cheese_count} מתכונים"}</span>')

    # Meat - 0 now
    meat_count = cats.get("meat", 0)
    html = html.replace("images/recipes/merguez-shakshuka-rafi-cohen.jpg", first_classic["image"])
    old_meat = '<span class="category-card-count">מתכון אחד</span>'
    html = html.replace(old_meat,
                         f'<span class="category-card-count">{"מתכון אחד" if meat_count==1 else ("בקרוב" if meat_count==0 else f"{meat_count} מתכונים")}</span>', 1)

    # Fusion - 0 now
    fusion_count = cats.get("fusion", 0)
    html = html.replace("images/recipes/thai-green-shakshuka-curry.jpg", first_classic["image"])
    html = html.replace('<span class="category-card-count">7 מתכונים</span>',
                         f'<span class="category-card-count">{"בקרוב" if fusion_count==0 else f"{fusion_count} מתכונים"}</span>')

    # 4. Replace featured recipe section
    featured_start = html.find('<!-- ======== 4. FEATURED RECIPE ========')
    featured_end = html.find('<!-- ======== 5. ALL RECIPES ========')
    if featured_start >= 0 and featured_end >= 0:
        featured_recipe = first_classic
        new_featured = f'''<!-- ======== 4. FEATURED RECIPE ======== -->
  <section class="section" id="featured">
    <div class="container">
      <h2 class="text-center">\u2b50 \u05de\u05ea\u05db\u05d5\u05df \u05de\u05d5\u05de\u05dc\u05e5</h2>
      <div style="background: var(--card-bg, #fff); border-radius: 1rem; box-shadow: 0 4px 24px rgba(0,0,0,0.08); padding: 2.5rem; max-width: 900px; margin: 2rem auto;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center;">
          <div>
            <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{featured_recipe["titleHe"]}</h3>
            <p style="color: var(--text-secondary, #666); margin-bottom: 1rem;">{featured_recipe.get("description","")}</p>
            <a href="recipes/{featured_recipe["slug"]}.html" style="display: inline-block; padding: 0.75rem 1.5rem; background: var(--accent, #e63946); color: #fff; border-radius: 0.5rem; text-decoration: none; font-weight: 600;">\u05dc\u05e6\u05e4\u05d9\u05d9\u05d4 \u05d1\u05de\u05ea\u05db\u05d5\u05df \u2190</a>
          </div>
          <div style="border-radius: 0.75rem; overflow: hidden; min-height: 200px;">
            <img src="{featured_recipe["image"]}" alt="{featured_recipe["titleHe"]}" style="width:100%;height:200px;object-fit:cover;border-radius:0.75rem;">
          </div>
        </div>
      </div>
    </div>
  </section>

  '''
        html = html[:featured_start] + new_featured + html[featured_end:]

    # 5. Update "ALL RECIPES" heading
    html = html.replace("כל 24 המתכונים", f"כל {n} המתכונים")

    # 6. Replace the inlined recipe data array
    # Find the pattern: const allRecipes = [...];
    data_start = html.find("const allRecipes = [")
    if data_start >= 0:
        # Find the end of the array (the matching ];)
        bracket_count = 0
        i = html.index("[", data_start)
        for j in range(i, len(html)):
            if html[j] == "[": bracket_count += 1
            elif html[j] == "]": bracket_count -= 1
            if bracket_count == 0:
                data_end = j + 1
                break

        # Build compact recipe data for index cards
        card_data = []
        for r in recipes:
            cd = {
                "id": r["id"],
                "slug": r["slug"],
                "titleHe": r["titleHe"],
                "titleEn": r["titleEn"],
                "author": r["author"],
                "category": r["category"],
                "categoryHe": r.get("categoryHe", ""),
                "difficulty": r.get("difficulty", "קל"),
                "prepTime": parse_min(r.get("prepTime", "0")),
                "cookTime": parse_min(r.get("cookTime", "0")),
                "servings": r.get("servings", ""),
                "description": r.get("description", ""),
                "sourceUrl": r.get("sourceUrl", ""),
                "image": r.get("image", ""),
                "tags": r.get("tags", []),
                "ingredients": [{"item": ing["item"], "amount": ing.get("amount",""), "unit": ing.get("unit","")} for ing in r.get("ingredients", [])],
            }
            card_data.append(cd)

        new_data = json.dumps(card_data, ensure_ascii=False, separators=(",", ":"))
        html = html[:data_start] + f"const allRecipes = {new_data}" + html[data_end:]

    # 7. Fix footer text
    html = html.replace("24 מתכוני שקשוקה מהשפים והבשלנים הטובים בישראל, בנוי ממחקר ואהבה.",
                         f"{n} מתכוני שקשוקה מאומתים ממקורות אמיתיים.")
    html = html.replace("פרויקט אהבה המתעד 24 מתכוני שקשוקה",
                         f"פרויקט אהבה המתעד {n} מתכוני שקשוקה")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Updated index.html with {n} verified recipes")
    print(f"Category counts: classic-red={cats.get('classic-red',0)}, cheese={cats.get('cheese',0)}")

def parse_min(s):
    m = re.search(r'(\d+)', str(s))
    return int(m.group(1)) if m else 0

if __name__ == "__main__":
    main()
