"""Inject source attribution links into all recipe HTML files."""
import json, os, re

with open('data/recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

url_map = {r['slug']: r.get('sourceUrl', '') for r in recipes}
author_map = {r['slug']: r.get('author', '') for r in recipes}

recipes_dir = 'recipes'
updated = 0
skipped = 0

for fname in os.listdir(recipes_dir):
    if not fname.endswith('.html'):
        continue
    slug = fname.replace('.html', '')
    url = url_map.get(slug, '')
    author = author_map.get(slug, '')
    
    fpath = os.path.join(recipes_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Skip if already has source attribution
    if 'source-attribution' in html:
        print(f"  SKIP {slug} (already has attribution)")
        skipped += 1
        continue
    
    if not url:
        print(f"  SKIP {slug} (no source URL)")
        skipped += 1
        continue
    
    # Build the attribution HTML
    attribution = f'''
    <div class="source-attribution" style="margin:16px 0;padding:12px 20px;background:var(--bg-card, #fff);border-left:4px solid var(--accent, #C0392B);border-radius:8px;font-size:0.95rem;">
      <span style="opacity:0.7;">📖 מקור המתכון:</span>
      <a href="{url}" target="_blank" rel="noopener noreferrer" style="color:var(--accent, #C0392B);text-decoration:none;font-weight:600;margin-right:8px;">{author if author else url}</a>
      <span style="opacity:0.5;font-size:0.85em;">↗</span>
    </div>
'''
    
    # Insert after the recipe-description div
    # Look for the recipe-tags div and insert before it
    marker = '<div class="recipe-tags">'
    if marker in html:
        html = html.replace(marker, attribution + '    ' + marker, 1)
    else:
        # Fallback: insert after recipe-description
        marker2 = '</div>\n\n    <div class="recipe-content-grid">'
        if marker2 in html:
            html = html.replace(marker2, '</div>\n' + attribution + '\n    <div class="recipe-content-grid">', 1)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  OK   {slug}")
    updated += 1

print(f"\nDone: {updated} updated, {skipped} skipped")
