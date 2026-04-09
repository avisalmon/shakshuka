"""Fix remaining English text in recipe HTML pages."""
import os, re, glob, json

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
data_file = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

# Load recipe data for Hebrew author names
with open(data_file, 'r', encoding='utf-8') as f:
    recipes = json.load(f)

# Build slug -> Hebrew author map
author_map = {}
for r in recipes:
    author_map[r['slug']] = r['author']

fixed_count = 0

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    slug = os.path.basename(html_file).replace('.html', '')
    
    # 1. Fix "min" -> "דק'" in meta-value spans
    content = re.sub(
        r'(<span class="meta-value">)(\d+)\s*min(</span>)',
        r'\g<1>\2 דק׳\3',
        content
    )
    
    # 2. Fix "by AuthorName" -> "מאת HebrewName" in hero section
    he_author = author_map.get(slug, '')
    if he_author:
        content = re.sub(
            r'>by\s+[^<]+</p>',
            f'>מאת {he_author}</p>',
            content
        )
    
    # 3. Fix English alt text in related recipe cards
    for r in recipes:
        # Replace English alt text with Hebrew title
        content = content.replace(
            f'alt="{r["titleEn"]}"',
            f'alt="{r["titleHe"]}"'
        )
        # Also handle HTML-escaped variants
        en_escaped = r['titleEn'].replace("'", "&#x27;").replace("&", "&amp;")
        he_title = r['titleHe']
        content = content.replace(
            f'alt="{en_escaped}"',
            f'alt="{he_title}"'
        )
    
    # 4. Fix any remaining English card titles in related cards
    for r in recipes:
        content = content.replace(
            f'<h3>{r["titleEn"]}</h3>',
            f'<h3>{r["titleHe"]}</h3>'
        )
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {os.path.basename(html_file)}')

print(f'\nDone — fixed {fixed_count} files')
