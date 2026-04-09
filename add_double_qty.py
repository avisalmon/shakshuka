"""Add 'double quantities' toggle button to all recipe pages.
Pre-calculates x2 amounts and adjusted cook times, stores both in inline JS.
No localStorage - purely real-time toggle."""
import os, re, glob, json, math

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
data_file = os.path.join(os.path.dirname(__file__), 'data', 'recipes.json')

with open(data_file, 'r', encoding='utf-8') as f:
    recipes = json.load(f)

recipe_map = {r['slug']: r for r in recipes}


def double_amount(amount_str):
    """Double an amount string like '1', '1/2', '8-10', '1/4', '2-3'."""
    if not amount_str or not amount_str.strip():
        return ''
    s = amount_str.strip()
    # Range like "8-10"
    if '-' in s and '/' not in s:
        parts = s.split('-')
        try:
            return f'{int(float(parts[0])*2)}-{int(float(parts[1])*2)}'
        except:
            return s
    # Fraction like "1/2" or "1/4"
    if '/' in s:
        try:
            parts = s.split('/')
            num = int(parts[0]) * 2
            denom = int(parts[1])
            # Simplify
            from math import gcd
            g = gcd(num, denom)
            num, denom = num // g, denom // g
            if denom == 1:
                return str(num)
            return f'{num}/{denom}'
        except:
            return s
    # Plain number
    try:
        val = float(s)
        doubled = val * 2
        if doubled == int(doubled):
            return str(int(doubled))
        return str(doubled)
    except:
        return s


def adjust_cook_time(cook_min):
    """Adjust cook time for double quantity: ~30% more, rounded to 5."""
    adjusted = cook_min * 1.3
    return int(5 * round(adjusted / 5))


fixed_count = 0

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    slug = os.path.basename(html_file).replace('.html', '')
    recipe = recipe_map.get(slug)
    if not recipe:
        continue

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Skip if already has the button
    if 'double-qty-btn' in content:
        continue

    # Pre-calculate doubled ingredient texts
    # Build arrays of [original_text, doubled_text] for each ingredient
    x1_texts = []
    x2_texts = []
    for ing in recipe['ingredients']:
        amount = ing.get('amount', '')
        unit = ing.get('unit', '')
        item = ing.get('item', '')
        # x1 text (same as currently rendered)
        if amount and unit:
            x1 = f'{amount} {unit} {item}'
        elif amount:
            x1 = f'{amount} {item}'
        else:
            x1 = item
        # x2 text
        d_amount = double_amount(amount)
        if d_amount and unit:
            x2 = f'{d_amount} {unit} {item}'
        elif d_amount:
            x2 = f'{d_amount} {item}'
        else:
            x2 = item
        x1_texts.append(x1)
        x2_texts.append(x2)

    # Calculate times
    prep = recipe.get('prepTime', 0)
    cook = recipe.get('cookTime', 0)
    servings = recipe.get('servings', '')

    prep_x2 = prep  # prep time stays same
    cook_x2 = adjust_cook_time(cook)
    total_x1 = prep + cook
    total_x2 = prep_x2 + cook_x2

    # Double servings
    try:
        if '-' in str(servings):
            parts = servings.split('-')
            servings_x2 = f'{int(parts[0])*2}-{int(parts[1])*2}'
        else:
            servings_x2 = str(int(servings) * 2)
    except:
        servings_x2 = servings

    # Escape for JS string literals
    def js_escape(s):
        return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')

    x1_js = '[' + ','.join(f"'{js_escape(t)}'" for t in x1_texts) + ']'
    x2_js = '[' + ','.join(f"'{js_escape(t)}'" for t in x2_texts) + ']'

    # 1. Add button after shopping list button
    button_html = '    <button class="btn btn-sm btn-outline" id="double-qty-btn" style="margin-right:8px;">×2 הכפלת כמויות</button>'
    content = content.replace(
        '<button class="btn btn-sm btn-outline" id="add-shopping-list">🛒 הוסף לרשימת קניות</button>',
        '<button class="btn btn-sm btn-outline" id="add-shopping-list">🛒 הוסף לרשימת קניות</button>\n' + button_html
    )

    # 2. Add inline JS before closing </script>
    double_js = f"""
  // Double quantities toggle
  var _dblState = false;
  var _x1 = {x1_js};
  var _x2 = {x2_js};
  var _times_x1 = {{prep: '{prep} דק׳', cook: '{cook} דק׳', total: '{total_x1} דק׳', servings: '{servings}'}};
  var _times_x2 = {{prep: '{prep_x2} דק׳', cook: '{cook_x2} דק׳', total: '{total_x2} דק׳', servings: '{servings_x2}'}};
  var dblBtn = document.getElementById('double-qty-btn');
  if (dblBtn) {{
    dblBtn.addEventListener('click', function() {{
      _dblState = !_dblState;
      var texts = _dblState ? _x2 : _x1;
      var times = _dblState ? _times_x2 : _times_x1;
      dblBtn.textContent = _dblState ? '×1 כמות רגילה' : '×2 הכפלת כמויות';
      dblBtn.style.background = _dblState ? 'var(--accent, #e74c3c)' : '';
      dblBtn.style.color = _dblState ? '#fff' : '';
      // Update ingredients
      var items = document.querySelectorAll('.ingredient-text');
      items.forEach(function(el, idx) {{
        if (idx < texts.length) el.textContent = texts[idx];
      }});
      // Update meta values
      var metaValues = document.querySelectorAll('.meta-value');
      metaValues.forEach(function(mv) {{
        var label = mv.previousElementSibling;
        if (!label) return;
        var lt = label.textContent;
        if (lt.indexOf('הכנה') >= 0) mv.textContent = times.prep;
        else if (lt.indexOf('בישול') >= 0) mv.textContent = times.cook;
        else if (lt.indexOf('סה') >= 0) mv.textContent = times.total;
        else if (lt.indexOf('מנות') >= 0) mv.textContent = times.servings;
      }});
    }});
  }}"""

    # Insert before the closing });  of the DOMContentLoaded
    content = content.replace(
        '\n});\n</script>',
        double_js + '\n});\n</script>'
    )

    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Added: {slug}')

print(f'\nDone - added double button to {fixed_count} files')
