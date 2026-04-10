import json
d = json.load(open('data/recipes.json', 'r', encoding='utf-8'))
print(f'{len(d)} recipes')
for r in d:
    print(f'  {r["id"]}: {r["slug"]} - {len(r["ingredients"])} ingredients, {len(r["steps"])} steps')
