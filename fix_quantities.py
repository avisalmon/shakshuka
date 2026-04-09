"""Add visible quantities to ingredient text in all recipe pages."""
import os, re, glob

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
fixed_count = 0

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern: match ingredient lines and inject amount+unit into visible text
    # Before: data-amount="8-10" data-unit="שיניים"> <span class="ingredient-text" dir="rtl">שום פרוס דק</span>
    # After:  data-amount="8-10" data-unit="שיניים"> <span class="ingredient-text" dir="rtl">8-10 שיניים שום פרוס דק</span>
    
    def fix_ingredient(m):
        amount = m.group(1)
        unit = m.group(2)
        # Unescape HTML entities for display
        unit_display = unit.replace('&quot;', '"').replace('&amp;', '&')
        item_text = m.group(3)
        
        # Build quantity prefix
        if amount and unit_display:
            prefix = f'{amount} {unit_display} '
        elif amount:
            prefix = f'{amount} '
        else:
            prefix = ''
        
        # Return with quantity prepended to visible text
        return f'data-amount="{amount}" data-unit="{unit}"> <span class="ingredient-text" dir="rtl">{prefix}{item_text}</span>'
    
    content = re.sub(
        r'data-amount="([^"]*)" data-unit="([^"]*)"> <span class="ingredient-text" dir="rtl">([^<]+)</span>',
        fix_ingredient,
        content
    )
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {os.path.basename(html_file)}')

print(f'\nDone - fixed {fixed_count} files')
