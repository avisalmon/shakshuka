"""Update all recipe HTMLs with per-stage cooking times and accurate double-qty data.
Reads stage_times.json for per-step durations.
For each recipe:
  1. Adds time badge to each step in the steps list
  2. Updates meta-bar prep/cook/total from JSON
  3. Updates double-qty JS with accurate _times_x1/_times_x2 from JSON
  4. Adds step-time toggle in double-qty click handler
"""
import os, re, json
from html import escape as html_escape

BASE = os.path.dirname(os.path.abspath(__file__))
recipes_dir = os.path.join(BASE, 'recipes')
stage_file = os.path.join(BASE, 'data', 'stage_times.json')
data_file = os.path.join(BASE, 'data', 'recipes.json')

with open(stage_file, 'r', encoding='utf-8') as f:
    stage_data = json.load(f)

with open(data_file, 'r', encoding='utf-8') as f:
    recipes_json = json.load(f)

recipe_map = {r['slug']: r for r in recipes_json}

def fmt_time(mins):
    if mins == 0:
        return ''
    if mins < 1:
        return f'{int(mins*60)} שנ׳'
    if mins == int(mins):
        return f'{int(mins)} דק׳'
    return f'{mins} דק׳'

updated = 0
skipped = []

for fn in sorted(os.listdir(recipes_dir)):
    if not fn.endswith('.html'):
        continue
    slug = fn.replace('.html', '')

    if slug not in stage_data:
        skipped.append(slug)
        continue

    sd = stage_data[slug]
    stages = sd['stages']

    fpath = os.path.join(recipes_dir, fn)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # ── 0. Clean up any previously injected step-time badges and step-time JS ──
    content = re.sub(r'<span class="step-time"[^>]*>⏱[^<]*</span>', '', content)
    # Remove previously injected step-time forEach block
    content = re.sub(
        r'\n\s*// Update step time badges\n\s*document\.querySelectorAll\(\'\.step-time\'\)\.forEach\(function\(st\) \{\n\s*var t = _dblState \? st\.dataset\.timeX2 : st\.dataset\.timeX1;\n\s*if \(t\) st\.textContent = .*?;\n\s*\}\);',
        '',
        content
    )

    # ── 1. Add time badges to steps ──
    # Find all step-items and add time badge after step-number
    step_items = list(re.finditer(
        r'<li class="step-item"><span class="step-number">(\d+)</span><div class="step-content">',
        content
    ))

    if len(step_items) != len(stages):
        print(f'WARNING {fn}: {len(step_items)} steps in HTML but {len(stages)} stages in JSON — skipping step badges')
    else:
        # Process in reverse order to preserve positions
        for i in range(len(step_items) - 1, -1, -1):
            m = step_items[i]
            step_num = int(m.group(1))
            stage = stages[i]
            t = stage['time_min']
            t_x2 = stage['time_x2']
            stage_name = stage['name']

            # Build time badge HTML
            if t > 0:
                time_str = fmt_time(t)
                time_x2_str = fmt_time(t_x2)
                badge = f'<span class="step-time" data-time-x1="{time_str}" data-time-x2="{time_x2_str}" title="{html_escape(stage_name, quote=True)}">⏱ {time_str}</span>'
            else:
                badge = ''

            # Insert badge after </span> of step-number, before <div class="step-content">
            insert_pos = m.start() + len(f'<li class="step-item"><span class="step-number">{step_num}</span>')
            if badge:
                content = content[:insert_pos] + badge + content[insert_pos:]

    # ── 2. Update meta-bar times ──
    total_cook = sd['total_cook']
    prep = sd['prep']
    total = prep + total_cook

    total_cook_x2 = sd['total_cook_x2']
    prep_x2 = sd['prep_x2']
    total_x2 = prep_x2 + total_cook_x2

    # Update the HTML meta-value spans
    content = re.sub(
        r'data-field="prep">.*?</span>',
        f'data-field="prep">{prep} דק׳</span>',
        content
    )
    content = re.sub(
        r'data-field="cook">.*?</span>',
        f'data-field="cook">{total_cook} דק׳</span>',
        content
    )
    content = re.sub(
        r'data-field="total">.*?</span>',
        f'data-field="total">{total} דק׳</span>',
        content
    )

    # ── 3. Update _times_x1 and _times_x2 in inline JS ──
    recipe = recipe_map.get(slug, {})
    servings = recipe.get('servings', '')
    try:
        if '-' in str(servings):
            parts = servings.split('-')
            servings_x2 = f'{int(parts[0])*2}-{int(parts[1])*2}'
        else:
            servings_x2 = str(int(servings) * 2)
    except:
        servings_x2 = servings

    new_x1 = f"var _times_x1 = {{prep: '{prep} דק׳', cook: '{total_cook} דק׳', total: '{total} דק׳', servings: '{servings}'}};"
    new_x2 = f"var _times_x2 = {{prep: '{prep_x2} דק׳', cook: '{total_cook_x2} דק׳', total: '{total_x2} דק׳', servings: '{servings_x2}'}};"

    content = re.sub(r"var _times_x1 = \{.*?\};", new_x1, content)
    content = re.sub(r"var _times_x2 = \{.*?\};", new_x2, content)

    # ── 4. Add step-time toggle to double-qty click handler ──
    # Add code to update step-time badges when toggling
    step_time_update = """
      // Update step time badges
      document.querySelectorAll('.step-time').forEach(function(st) {
        var t = _dblState ? st.dataset.timeX2 : st.dataset.timeX1;
        if (t) st.textContent = '\\u23F1 ' + t;
      });"""

    # Check if already has step-time update code
    if 'step-time' not in content.split('dblBtn.addEventListener')[1] if 'dblBtn.addEventListener' in content else True:
        # Insert after the meta-values update block
        content = content.replace(
            "if (f) f.textContent = times.servings;\n    });",
            "if (f) f.textContent = times.servings;" + step_time_update + "\n    });"
        )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated {fn}: prep={prep} cook={total_cook} total={total} | x2: prep={prep_x2} cook={total_cook_x2} total={total_x2} | {len(stages)} stages')
        updated += 1

if skipped:
    print(f'\nSkipped (no stage data): {skipped}')
print(f'\nTotal updated: {updated}')
