"""Add print button to recipe meta bar in all recipe pages."""
import os, re, glob

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
fixed_count = 0

PRINT_BUTTON = '''  <div class="meta-item">
    <button class="meta-print-btn" onclick="window.print()" aria-label="הדפסת מתכון" title="הדפסה">🖨️</button>
  </div>'''

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Insert print button right before the favorite button meta-item (last item in meta bar)
    content = content.replace(
        '  <div class="meta-item">\n    <button class="meta-fav-btn"',
        PRINT_BUTTON + '\n  <div class="meta-item">\n    <button class="meta-fav-btn"'
    )
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1

print(f'Done - added print button to {fixed_count} files')
