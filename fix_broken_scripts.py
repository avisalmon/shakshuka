"""Fix broken inline scripts in recipe pages - remove garbled star rating code."""
import os, re, glob

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
fixed_count = 0

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix the broken remnant: "// Star rating handled by app.js initRecipePage());\n    }\n  }"
    # and any variants with extra closing braces/whitespace
    # Replace the whole garbled block with just the comment
    content = re.sub(
        r'// Star rating handled by app\.js[^/\n]*initRecipePage\(\)\);\s*\}\s*\}',
        '// Star rating handled by app.js initRecipePage()',
        content
    )
    
    # Also catch simpler variants
    content = re.sub(
        r'// Star rating handled by app\.js\s+initRecipePage\(\)\);\s*\}\s*\}',
        '// Star rating handled by app.js initRecipePage()',
        content
    )
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {os.path.basename(html_file)}')

print(f'\nDone - fixed {fixed_count} files')
