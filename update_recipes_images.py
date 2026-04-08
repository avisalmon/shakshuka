import json

with open("data/recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

count = 0
for recipe in recipes:
    recipe["image"] = f"images/recipes/{recipe['slug']}.jpg"
    recipe["sourceUrl"] = recipe.get("sourceUrl", "")
    count += 1

with open("data/recipes.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=2)

print(f"Updated {count} recipes with image paths.")
for r in recipes:
    print(f"  {r['slug']} -> {r['image']}")
