"""Fix star rating init and remaining English h1 in recipe pages."""
import os, re, glob, json

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
data_file = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

with open(data_file, 'r', encoding='utf-8') as f:
    recipes = json.load(f)

# Build slug -> Hebrew title map
title_map = {}
for r in recipes:
    title_map[r['slug']] = r['titleHe']

fixed_count = 0

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    slug = os.path.basename(html_file).replace('.html', '')
    
    # 1. Fix inline star rating: remove the broken initStarRating() call
    # Replace the whole rating block in the inline script to just be a comment
    content = re.sub(
        r'// Star rating\s*\n\s*if \(typeof initStarRating === \'function\'\) \{\s*\n\s*initStarRating\(\);\s*\n\s*\} else \{[^}]*\{[^}]*\{[^}]*\}[^}]*\}[^}]*\}[^}]*\}[^}]*\}',
        '// Star rating handled by app.js initRecipePage()',
        content,
        flags=re.DOTALL
    )
    
    # 2. Fix English h1 titles
    he_title = title_map.get(slug, '')
    if he_title:
        # Replace English h1 in hero section
        content = re.sub(
            r'(<h1[^>]*>)[^<]+(</h1>)',
            lambda m: f'{m.group(1)}{he_title}{m.group(2)}',
            content,
            count=1  # Only first h1
        )
    
    # 3. Fix English title in RecentlyViewed.add call
    if he_title:
        content = re.sub(
            r"RecentlyViewed\.add\(\{[^}]*\}\)",
            f"RecentlyViewed.add('{slug}')",
            content
        )
    
    # 4. Fix nav logo "Shakshuka" -> "שקשוקה"
    content = content.replace(
        '<a href="../index.html" class="nav-logo"><span>🍳</span> Shakshuka</a>',
        '<a href="../index.html" class="nav-logo"><span>🍳</span> שקשוקה</a>'
    )
    
    # 5. Fix footer English text
    content = content.replace(
        "<p>Celebrating Israel's beloved egg dish.</p>",
        '<p>אתר השקשוקה של אבי סלמון</p>'
    )
    content = content.replace('>Green<', '>ירוקה<')
    content = content.replace('>Cheese<', '>עם גבינות<')
    content = content.replace('>Meat<', '>עם בשר<')
    content = content.replace('>Fusion<', '>פיוז׳ן<')
    content = content.replace('<h4>About</h4>', '<h4>אודות</h4>')
    content = content.replace(
        "<p>24 shakshuka recipes from Israel's finest.</p>",
        '<p>24 מתכוני שקשוקה מהטובים בישראל</p>'
    )
    content = content.replace('>Learn more<', '>עוד<')
    content = content.replace(
        '&copy; 2025 Shakshuka  -  Made with',
        '&copy; 2025 שקשוקה &ndash; נבנה עם'
    )
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {os.path.basename(html_file)}')

print(f'\nDone - fixed {fixed_count} files')
