"""Inline recipes.json data into index.html to avoid fetch() failure on file:// protocol."""
import json

with open('data/recipes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_fetch = """      let allRecipes = [];

      try {
        const res = await fetch('data/recipes.json');
        allRecipes = await res.json();
      } catch (e) {
        grid.innerHTML = '<p style="text-align:center;color:#999;">\u05dc\u05d0 \u05e0\u05d9\u05ea\u05df \u05dc\u05d8\u05e2\u05d5\u05df \u05d0\u05ea \u05d4\u05de\u05ea\u05db\u05d5\u05e0\u05d9\u05dd.</p>';
        return;
      }"""

new_inline = '      const allRecipes = ' + json_str + ';'

if old_fetch in html:
    html = html.replace(old_fetch, new_inline)
    html = html.replace("document.addEventListener('DOMContentLoaded', async function () {",
                         "document.addEventListener('DOMContentLoaded', function () {")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Done - inlined {len(data)} recipes into index.html')
else:
    print('ERROR: Could not find fetch block to replace')
    # Try to find what's actually there
    import re
    m = re.search(r'let allRecipes.*?catch.*?\}', html, re.DOTALL)
    if m:
        print(f'Found similar block at pos {m.start()}: {repr(m.group()[:100])}')
