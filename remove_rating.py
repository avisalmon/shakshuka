"""Remove star rating section from all recipe pages."""
import os, re, glob

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
fixed_count = 0

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove the star-rating HTML block
    content = re.sub(
        r'\s*<div class="star-rating"[^>]*>.*?</div>\s*</div>',
        '',
        content,
        flags=re.DOTALL,
        count=1
    )
    
    # Remove the inline star rating JS block
    content = re.sub(
        r'  // Star rating - self-contained init\n.*?(?=\n  // Favorite buttons)',
        '',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {os.path.basename(html_file)}')

print(f'\nDone - removed rating from {fixed_count} files')
