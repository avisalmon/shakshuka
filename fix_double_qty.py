"""Fix double-qty: use data attributes on meta-value spans instead of DOM traversal."""
import os, re, glob, json

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
data_file = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

with open(data_file, 'r', encoding='utf-8') as f:
    recipes = json.load(f)

recipe_map = {r['slug']: r for r in recipes}
fixed_count = 0

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    slug = os.path.basename(html_file).replace('.html', '')
    recipe = recipe_map.get(slug)
    if not recipe:
        continue

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Add data-field attributes to meta-value spans
    content = re.sub(
        r'(<span class="meta-label">הכנה</span><span class="meta-value">)',
        r'<span class="meta-label">הכנה</span><span class="meta-value" data-field="prep">',
        content
    )
    content = re.sub(
        r'(<span class="meta-label">בישול</span><span class="meta-value">)',
        r'<span class="meta-label">בישול</span><span class="meta-value" data-field="cook">',
        content
    )
    content = re.sub(
        r'(<span class="meta-label">סה"כ</span><span class="meta-value">)',
        r'<span class="meta-label">סה"כ</span><span class="meta-value" data-field="total">',
        content
    )
    content = re.sub(
        r'(<span class="meta-label">מנות</span><span class="meta-value">)',
        r'<span class="meta-label">מנות</span><span class="meta-value" data-field="servings">',
        content
    )

    # 2. Replace the DOM traversal JS with simple data-field selectors
    old_js = """      // Update meta values
      var metaValues = document.querySelectorAll('.meta-value');
      metaValues.forEach(function(mv) {
        var label = mv.previousElementSibling;
        if (!label) return;
        var lt = label.textContent;
        if (lt.indexOf('הכנה') >= 0) mv.textContent = times.prep;
        else if (lt.indexOf('בישול') >= 0) mv.textContent = times.cook;
        else if (lt.indexOf('סה') >= 0) mv.textContent = times.total;
        else if (lt.indexOf('מנות') >= 0) mv.textContent = times.servings;
      });"""

    new_js = """      // Update meta values
      var f;
      f = document.querySelector('.meta-value[data-field="prep"]');
      if (f) f.textContent = times.prep;
      f = document.querySelector('.meta-value[data-field="cook"]');
      if (f) f.textContent = times.cook;
      f = document.querySelector('.meta-value[data-field="total"]');
      if (f) f.textContent = times.total;
      f = document.querySelector('.meta-value[data-field="servings"]');
      if (f) f.textContent = times.servings;"""

    content = content.replace(old_js, new_js)

    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {slug}')

print(f'\nDone - fixed {fixed_count} files')
