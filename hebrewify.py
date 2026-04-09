"""
Transform the entire Shakshuka site to full Hebrew:
1. All UI text in Hebrew (nav, buttons, headings, labels, placeholders)
2. Recipe cards show Hebrew titles as primary
3. Category cards show Hebrew names
4. No em dashes anywhere
5. Category card clicks filter the recipe grid
6. All content pages: Hebrew
"""
import os
import re
import json

# ── Load recipe data ──
with open('data/recipes.json', 'r', encoding='utf-8') as f:
    recipes = json.load(f)

recipe_map = {r['slug']: r for r in recipes}

# ── Category mappings ──
cat_he = {
    'classic-red': 'קלאסית אדומה',
    'green': 'ירוקה',
    'cheese': 'עם גבינות',
    'meat': 'עם בשר',
    'fusion': "פיוז'ן ומודרני",
}

cat_count_he = {
    'classic-red': '11 מתכונים',
    'green': '2 מתכונים',
    'cheese': '3 מתכונים',
    'meat': 'מתכון אחד',
    'fusion': '7 מתכונים',
}

difficulty_he = {
    'Easy': 'קל',
    'Medium': 'בינוני',
    'Hard': 'מאתגר',
}

def remove_em_dashes(text):
    """Remove em dashes and en dashes, replace with ' - ' or just remove."""
    text = text.replace(' — ', ' - ')
    text = text.replace('— ', '- ')
    text = text.replace(' —', ' -')
    text = text.replace('—', ' - ')
    text = text.replace('&mdash;', ' - ')
    # en dash
    text = text.replace(' – ', ' - ')
    text = text.replace('–', ' - ')
    text = text.replace('&ndash;', ' - ')
    return text

# ════════════════════════════════════════════
# 1. FIX INDEX.HTML
# ════════════════════════════════════════════
print("=== Fixing index.html ===")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# lang
html = html.replace('<html lang="en">', '<html lang="he" dir="rtl">')

# title & meta
html = html.replace('<title>Shakshuka שקשוקה — The Definitive Recipe Collection</title>',
                     '<title>שקשוקה - אוסף המתכונים המושלם</title>')
html = re.sub(r'<meta name="description" content="[^"]*">', 
              '<meta name="description" content="אוסף של 24 מתכוני שקשוקה מהשפים והבשלנים הטובים בישראל. קלאסית אדומה, ירוקה, עם גבינות, עם בשר ופיוז\'ן.">', html)
html = re.sub(r'<meta property="og:title" content="[^"]*">',
              '<meta property="og:title" content="שקשוקה - אוסף המתכונים המושלם">', html)
html = re.sub(r'<meta property="og:description" content="[^"]*">',
              '<meta property="og:description" content="24 מתכוני שקשוקה מהשפים הטובים בישראל.">', html)

# Nav links
html = html.replace('>Home</a>', '>בית</a>')
html = html.replace('>Recipes</a>', '>מתכונים</a>')
html = html.replace('>All Recipes</a>', '>כל המתכונים</a>')
html = html.replace('>History</a>', '>היסטוריה</a>')
html = html.replace('>Techniques</a>', '>טכניקות</a>')
html = html.replace('>Debates</a>', '>ויכוחים</a>')
html = html.replace('>Favorites</a>', '>מועדפים</a>')
html = html.replace('>About</a>', '>אודות</a>')

# Mobile nav
html = html.replace('🏠 Home', '🏠 בית')
html = html.replace('📖 All Recipes', '📖 כל המתכונים')
html = html.replace('🍳 All Recipes', '🍳 כל המתכונים')
html = html.replace('📜 History', '📜 היסטוריה')
html = html.replace('👨\u200d🍳 Techniques', '👨\u200d🍳 טכניקות')
html = html.replace('⚡ Debates', '⚡ ויכוחים')
html = html.replace('❤️ Favorites', '❤️ מועדפים')
html = html.replace('ℹ️ About', 'ℹ️ אודות')

# Search placeholders
html = html.replace('placeholder="Search recipes..."', 'placeholder="חיפוש מתכונים..."')
html = html.replace('placeholder="Search 24 recipes by name, ingredient, or style..."', 'placeholder="חיפוש ב-24 מתכונים לפי שם, מרכיב או סגנון..."')
html = html.replace('aria-label="Search recipes"', 'aria-label="חיפוש מתכונים"')
html = html.replace('aria-label="Favorites"', 'aria-label="מועדפים"')
html = html.replace('aria-label="Toggle theme"', 'aria-label="החלפת ערכת נושא"')
html = html.replace('aria-label="Toggle menu"', 'aria-label="תפריט"')

# Hero section
html = html.replace('<h1>Shakshuka</h1>', '<h1>שקשוקה</h1>')
html = re.sub(r'<p class="hero-subtitle">.*?</p>', 
              '<p class="hero-subtitle">המדריך המושלם למנת הביצים האהובה של ישראל - 24 מתכונים מהשפים והבשלנים הטובים ביותר</p>', html)

# Categories section
html = html.replace('<h2 class="text-center">Explore by Category</h2>', 
                     '<h2 class="text-center">גלו לפי קטגוריה</h2>')

# Category cards - fix hrefs to trigger JS filter instead of broken anchors
html = html.replace('<a href="#classic-red" class="category-card" data-category="classic-red">',
                     '<a href="#recipes" class="category-card" data-category="classic-red" onclick="filterByCategory(\'classic-red\')">')
html = html.replace('<a href="#green" class="category-card" data-category="green">',
                     '<a href="#recipes" class="category-card" data-category="green" onclick="filterByCategory(\'green\')">')
html = html.replace('<a href="#cheese" class="category-card" data-category="cheese">',
                     '<a href="#recipes" class="category-card" data-category="cheese" onclick="filterByCategory(\'cheese\')">')
html = html.replace('<a href="#meat" class="category-card" data-category="meat">',
                     '<a href="#recipes" class="category-card" data-category="meat" onclick="filterByCategory(\'meat\')">')
html = html.replace('<a href="#fusion" class="category-card" data-category="fusion">',
                     '<a href="#recipes" class="category-card" data-category="fusion" onclick="filterByCategory(\'fusion\')">')

# Category card text to Hebrew
html = html.replace('<h3>Classic Red</h3>', '<h3>קלאסית אדומה</h3>')
html = html.replace('<h3>Green</h3>', '<h3>ירוקה</h3>')
html = html.replace('<h3>With Cheese</h3>', '<h3>עם גבינות</h3>')
html = html.replace('<h3>With Meat</h3>', '<h3>עם בשר</h3>')
html = html.replace('<h3>Fusion &amp; Modern</h3>', "<h3>פיוז'ן ומודרני</h3>")
# Remove duplicate Hebrew spans under category cards since h3 is now Hebrew
html = re.sub(r'<span class="category-hebrew">קלאסית אדומה</span>\s*', '', html)
html = re.sub(r'<span class="category-hebrew">ירוקה</span>\s*', '', html)
html = re.sub(r'<span class="category-hebrew">עם גבינות</span>\s*', '', html)
html = re.sub(r'<span class="category-hebrew">עם בשר</span>\s*', '', html)
html = re.sub(r"<span class=\"category-hebrew\">פיוז'ן</span>\s*", '', html)

# Category card counts to Hebrew
html = html.replace('>11 recipes</span>', '>11 מתכונים</span>')
html = html.replace('>2 recipes</span>', '>2 מתכונים</span>')
html = html.replace('>3 recipes</span>', '>3 מתכונים</span>')
html = html.replace('>1 recipe</span>', '>מתכון אחד</span>')
html = html.replace('>7 recipes</span>', '>7 מתכונים</span>')

# Featured section
html = html.replace('<h2 class="text-center">⭐ Featured: The Synthesized Ultimate Shakshuka</h2>',
                     '<h2 class="text-center">⭐ מתכון מומלץ: השקשוקה האולטימטיבית</h2>')
html = html.replace('<h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">The Optimal Red Shakshuka</h3>',
                     '<h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">השקשוקה האדומה המושלמת</h3>')
html = re.sub(r'<p style="color: var\(--text-secondary, #666\); margin-bottom: 1rem;">A data-driven synthesis.*?</p>',
              '<p style="color: var(--text-secondary, #666); margin-bottom: 1rem;">סינתזה מבוססת נתונים של 22 מתכונים מובילים - כל יחס מרכיבים, טכניקה ותזמון ממוטבים לשקשוקה האולטימטיבית. זה לא מתכון של שף אחד, זה הקונצנזוס של הטובים ביותר.</p>', html)
html = html.replace('>View Recipe →</a>', '>לצפייה במתכון ←</a>')

# All Recipes section
html = html.replace('<h2 class="text-center">All 24 Recipes</h2>',
                     '<h2 class="text-center">כל 24 המתכונים</h2>')

# Filter buttons
html = html.replace('>All</button>', '>הכל</button>')
html = html.replace('>Classic Red</button>', '>קלאסית אדומה</button>')
html = html.replace('>Green</button>', '>ירוקה</button>')
html = html.replace('>Cheese</button>', '>עם גבינות</button>')
html = html.replace('>Meat</button>', '>עם בשר</button>')
html = html.replace('>Fusion</button>', ">פיוז'ן</button>")

# Could not load message
html = html.replace("Could not load recipes.", "לא ניתן לטעון את המתכונים.")

# Footer
html = html.replace('<h4>🍳 Shakshuka</h4>', '<h4>🍳 שקשוקה</h4>')
html = html.replace("<p>Celebrating Israel's beloved egg dish — from the classic red to bold fusions. Recipes, history, techniques, and spirited debates.</p>",
                     '<p>חוגגים את מנת הביצים האהובה של ישראל. מתכונים, היסטוריה, טכניקות וויכוחים סוערים.</p>')
html = html.replace('<h4>Categories</h4>', '<h4>קטגוריות</h4>')
html = html.replace('<li><a href="#classic-red">Classic Red</a></li>', '<li><a href="#classic-red">קלאסית אדומה</a></li>')
html = html.replace('<li><a href="#green">Green</a></li>', '<li><a href="#green">ירוקה</a></li>')
html = html.replace('<li><a href="#cheese">With Cheese</a></li>', '<li><a href="#cheese">עם גבינות</a></li>')
html = html.replace('<li><a href="#meat">With Meat</a></li>', '<li><a href="#meat">עם בשר</a></li>')
html = html.replace('<li><a href="#fusion">Fusion &amp; Modern</a></li>', "<li><a href=\"#fusion\">פיוז'ן ומודרני</a></li>")
html = html.replace('<h4>Explore</h4>', '<h4>גלו</h4>')
html = html.replace('>History &amp; Origins</a>', '>היסטוריה ומקורות</a>')
html = html.replace('>Techniques</a>', '>טכניקות</a>')
html = html.replace('>Great Debates</a>', '>ויכוחים גדולים</a>')
html = html.replace('>My Favorites</a>', '>המועדפים שלי</a>')
html = html.replace('<h4>About This Project</h4>', '<h4>על הפרויקט</h4>')
html = html.replace('<p>A passion project documenting 24 shakshuka recipes from Israel\'s finest chefs and home cooks, built with research and love.</p>',
                     '<p>פרויקט אהבה המתעד 24 מתכוני שקשוקה מהשפים והבשלנים הטובים בישראל, בנוי ממחקר ואהבה.</p>')
html = html.replace('>Learn More →</a>', '>קראו עוד ←</a>')
html = html.replace('<p>&copy; 2026 Shakshuka שקשוקה — Made with 🍅 and ❤️</p>',
                     '<p>&copy; 2026 שקשוקה - נבנה עם 🍅 ו-❤️</p>')

# Add filterByCategory JS function before the closing script
filter_js = """
    // Category card click handler
    function filterByCategory(cat) {
      const filterBtns = document.querySelectorAll('.filter-btn');
      filterBtns.forEach(b => {
        b.classList.remove('active');
        if (b.dataset.filter === cat) b.classList.add('active');
      });
      renderRecipes(cat);
    }
    // Make it global
    window.filterByCategory = filterByCategory;
"""
# We need to inject this inside the IIFE but make renderRecipes accessible
# Actually let's make renderRecipes global and add the function outside
html = html.replace('      function renderRecipes(filter) {', '      window.renderRecipes = function renderRecipes(filter) {')

# Add filterByCategory function right before </script>
html = html.replace('    })();\n  </script>', filter_js + '    })();\n  </script>')

# Remove em dashes
html = remove_em_dashes(html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("  index.html done")

# ════════════════════════════════════════════
# 2. FIX ALL RECIPE PAGES
# ════════════════════════════════════════════
print("\n=== Fixing recipe pages ===")
recipe_dir = 'recipes'
for fname in sorted(os.listdir(recipe_dir)):
    if not fname.endswith('.html'):
        continue
    slug = fname.replace('.html', '')
    fpath = os.path.join(recipe_dir, fname)
    r = recipe_map.get(slug, {})
    
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # lang
    html = html.replace('<html lang="en">', '<html lang="he" dir="rtl">')
    
    # Page title
    title_en_pattern = re.compile(r'<title>.*?</title>')
    title_he = r.get('titleHe', slug)
    html = title_en_pattern.sub(f'<title>{title_he} | שקשוקה</title>', html)
    
    # Nav links
    html = html.replace('>Home</a>', '>בית</a>')
    html = html.replace('>Recipes</a>', '>מתכונים</a>')
    html = html.replace('>All Recipes</a>', '>כל המתכונים</a>')
    html = html.replace('>History</a>', '>היסטוריה</a>')
    html = html.replace('>Techniques</a>', '>טכניקות</a>')
    html = html.replace('>Debates</a>', '>ויכוחים</a>')
    html = html.replace('>Favorites</a>', '>מועדפים</a>')
    html = html.replace('>About</a>', '>אודות</a>')
    
    # Mobile nav
    html = html.replace('🏠 Home', '🏠 בית')
    html = html.replace('🍳 All Recipes', '🍳 כל המתכונים')
    html = html.replace('📖 All Recipes', '📖 כל המתכונים')
    html = html.replace('📜 History', '📜 היסטוריה')
    html = html.replace('👨\u200d🍳 Techniques', '👨\u200d🍳 טכניקות')
    html = html.replace('⚔ Debates', '⚔ ויכוחים')
    html = html.replace('❤️ Favorites', '❤️ מועדפים')
    html = html.replace('ℹ️ About', 'ℹ️ אודות')
    
    # Search
    html = html.replace('placeholder="Search recipes..."', 'placeholder="חיפוש מתכונים..."')
    html = html.replace('aria-label="Search recipes"', 'aria-label="חיפוש מתכונים"')
    html = html.replace('aria-label="Favorites"', 'aria-label="מועדפים"')
    html = html.replace('aria-label="Toggle theme"', 'aria-label="החלפת ערכת נושא"')
    html = html.replace('aria-label="Toggle menu"', 'aria-label="תפריט"')
    
    # Category tag in hero - translate to Hebrew
    for cat_en, cat_heb in [('Classic Red', 'קלאסית אדומה'), ('Green', 'ירוקה'), 
                             ('With Cheese', 'עם גבינות'), ('With Meat', 'עם בשר'),
                             ('Fusion', "פיוז'ן"), ('Fusion & Modern', "פיוז'ן ומודרני")]:
        html = html.replace(f'border-radius:20px;display:inline-block;margin-bottom:12px;">{cat_en}</span>',
                             f'border-radius:20px;display:inline-block;margin-bottom:12px;">{cat_heb}</span>')
    
    # Hero: make Hebrew title the h1, remove the English h1 and hero-hebrew
    title_he = r.get('titleHe', '')
    title_en = r.get('titleEn', '')
    author = r.get('author', '')
    author_en = r.get('authorEn', '')
    
    if title_en and title_he:
        # Replace English h1 with Hebrew
        html = html.replace(f'<h1>{title_en}</h1>', f'<h1 dir="rtl">{title_he}</h1>')
        # Remove the hero-hebrew line (now redundant)
        html = re.sub(r'\s*<p class="hero-hebrew" dir="rtl">.*?</p>', '', html)
    
    # Author: use Hebrew
    if author_en and author:
        html = html.replace(f'by {author_en}', f'מאת {author}')
        html = html.replace(f'by {author}', f'מאת {author}')
    elif author:
        html = html.replace(f'by {author}', f'מאת {author}')
    
    # Breadcrumbs
    html = html.replace('>Home</a> &rsaquo;', '>בית</a> &rsaquo;')
    if title_en:
        html = html.replace(f'<span class="breadcrumb-current">{title_en}</span>', 
                             f'<span class="breadcrumb-current">{title_he}</span>')
    
    # Meta bar labels
    html = html.replace('<span class="meta-label">Prep</span>', '<span class="meta-label">הכנה</span>')
    html = html.replace('<span class="meta-label">Cook</span>', '<span class="meta-label">בישול</span>')
    html = html.replace('<span class="meta-label">Total</span>', '<span class="meta-label">סה"כ</span>')
    html = html.replace('<span class="meta-label">Servings</span>', '<span class="meta-label">מנות</span>')
    html = html.replace('<span class="meta-label">Difficulty</span>', '<span class="meta-label">רמת קושי</span>')
    html = html.replace('aria-label="Add to favorites"', 'aria-label="הוספה למועדפים"')
    
    # Difficulty values
    html = html.replace('<span class="meta-value">Easy</span>', '<span class="meta-value">קל</span>')
    html = html.replace('<span class="meta-value">Medium</span>', '<span class="meta-value">בינוני</span>')
    html = html.replace('<span class="meta-value">Hard</span>', '<span class="meta-value">מאתגר</span>')
    
    # Section headings
    html = html.replace('<h3>🧾 Ingredients</h3>', '<h3>🧾 מרכיבים</h3>')
    html = html.replace('>🛒 Add to Shopping List</button>', '>🛒 הוסף לרשימת קניות</button>')
    html = html.replace('<h3>👨\u200d🍳 Steps</h3>', '<h3>👨\u200d🍳 הוראות הכנה</h3>')
    html = html.replace('<h3>💡 Pro Tips</h3>', '<h3>💡 טיפים מקצועיים</h3>')
    html = html.replace('<h3>⭐ Rate This Recipe</h3>', '<h3>⭐ דרגו את המתכון</h3>')
    html = html.replace('<h3>📝 My Notes</h3>', '<h3>📝 ההערות שלי</h3>')
    html = html.replace('placeholder="Write your notes about this recipe..."', 'placeholder="כתבו הערות על המתכון הזה..."')
    html = html.replace('>Save Notes</button>', '>שמירה</button>')
    html = html.replace('✓ Saved!', '✓ נשמר!')
    
    # Source attribution
    html = html.replace('📖 מקור המתכון:', '📖 מקור המתכון:')  # already Hebrew, keep
    
    # Related section
    html = html.replace('<h3>🍳 You Might Also Like</h3>', '<h3>🍳 אולי תאהבו גם</h3>')
    
    # Related cards: make Hebrew title primary
    # Pattern: <h4 class="card-title">English</h4>\n    <p class="card-title-he" dir="rtl">Hebrew</p>
    def swap_related_titles(match):
        en_title = match.group(1)
        he_title = match.group(2)
        return f'<h4 class="card-title" dir="rtl">{he_title}</h4>'
    html = re.sub(r'<h4 class="card-title">(.*?)</h4>\s*<p class="card-title-he" dir="rtl">(.*?)</p>', 
                  swap_related_titles, html)
    
    # Related card category labels
    html = html.replace('🟡 Classic Red', '🟡 קלאסית אדומה')
    html = html.replace('🟢 Classic Red', '🟢 קלאסית אדומה')  
    html = html.replace('🟡 Green', '🟡 ירוקה')
    html = html.replace('🟢 Green', '🟢 ירוקה')
    html = html.replace('🟡 Cheese', '🟡 עם גבינות')
    html = html.replace('🟢 Cheese', '🟢 עם גבינות')
    html = html.replace('🟡 Meat', '🟡 עם בשר')
    html = html.replace('🟢 Meat', '🟢 עם בשר')
    html = html.replace('🟡 Fusion', "🟡 פיוז'ן")
    html = html.replace('🟢 Fusion', "🟢 פיוז'ן")
    html = html.replace('🔴 Classic Red', '🔴 קלאסית אדומה')
    html = html.replace('🔵 Cheese', '🔵 עם גבינות')
    
    # Favorite button aria
    html = html.replace('aria-label="Favorite"', 'aria-label="מועדף"')
    
    # Footer content (same as index)
    html = html.replace('<h4>🍳 Shakshuka</h4>', '<h4>🍳 שקשוקה</h4>')
    html = html.replace('<h4>Categories</h4>', '<h4>קטגוריות</h4>')
    html = html.replace('<h4>Explore</h4>', '<h4>גלו</h4>')
    html = html.replace('<h4>About This Project</h4>', '<h4>על הפרויקט</h4>')
    html = html.replace('>Classic Red</a>', '>קלאסית אדומה</a>')
    html = html.replace('>With Cheese</a>', '>עם גבינות</a>')
    html = html.replace('>With Meat</a>', '>עם בשר</a>')
    html = html.replace('>History &amp; Origins</a>', '>היסטוריה ומקורות</a>')
    html = html.replace('>Great Debates</a>', '>ויכוחים גדולים</a>')
    html = html.replace('>My Favorites</a>', '>המועדפים שלי</a>')
    html = html.replace('>Learn More →</a>', '>קראו עוד ←</a>')
    
    # Ingredients: make Hebrew text primary, remove English
    # Current: <span class="ingredient-text">English</span><span class="ingredient-hebrew" ...>Hebrew</span>
    def swap_ingredient(match):
        full = match.group(0)
        he_match = re.search(r'<span class="ingredient-hebrew"[^>]*>(.*?)</span>', full)
        if he_match:
            he_text = he_match.group(1)
            # Remove the English text span, keep Hebrew as primary
            full = re.sub(r'<span class="ingredient-text">.*?</span>', f'<span class="ingredient-text" dir="rtl">{he_text}</span>', full)
            # Remove the separate Hebrew span
            full = re.sub(r'<span class="ingredient-hebrew"[^>]*>.*?</span>', '', full)
        return full
    
    html = re.sub(r'<li class="ingredient-item">.*?</li>', swap_ingredient, html, flags=re.DOTALL)
    
    # Steps: make Hebrew primary, remove English
    # Current: <p>English</p><p class="step-hebrew" ...>Hebrew</p>
    def swap_step(match):
        full = match.group(0)
        he_match = re.search(r'<p class="step-hebrew"[^>]*>(.*?)</p>', full)
        if he_match:
            he_text = he_match.group(1)
            # Replace English paragraph with Hebrew
            full = re.sub(r'<div class="step-content"><p>.*?</p>', f'<div class="step-content"><p dir="rtl">{he_text}</p>', full)
            # Remove the separate Hebrew paragraph
            full = re.sub(r'<p class="step-hebrew"[^>]*>.*?</p>', '', full)
        return full
    
    html = re.sub(r'<li class="step-item">.*?</li>', swap_step, html, flags=re.DOTALL)
    
    # Pro tips: translate if they have Hebrew equivalents in data
    pro_tips_he = r.get('proTips', [])
    if pro_tips_he:
        # Replace the pro tips UL content with Hebrew
        def replace_pro_tips(match):
            items = ''.join(f'<li dir="rtl">{tip}</li>' for tip in pro_tips_he)
            return f'<ul>{items}</ul>'
        html = re.sub(r'<ul><li>.*?</li></ul>', replace_pro_tips, html, count=1, flags=re.DOTALL)
    
    # Min -> דק'
    html = re.sub(r'<span>⏱️\s*(\d+)\s*min</span>', r"<span>⏱️ \1 דק'</span>", html)
    
    # Remove em dashes
    html = remove_em_dashes(html)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  {fname} done")

# ════════════════════════════════════════════
# 3. FIX app.js createRecipeCard to show Hebrew
# ════════════════════════════════════════════
print("\n=== Fixing js/app.js ===")
with open('js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Card: Hebrew title as primary
js = js.replace(
    '<h3 class="card-title">${recipe.titleEn}</h3>',
    '<h3 class="card-title" dir="rtl">${recipe.titleHe}</h3>'
)
js = js.replace(
    '<p class="card-title-he">${recipe.titleHe}</p>',
    ''  # Remove redundant Hebrew subtitle
)
# Card author: Hebrew
js = js.replace(
    '<p class="card-author">${recipe.authorEn || recipe.author}</p>',
    '<p class="card-author" dir="rtl">${recipe.author}</p>'
)
# Card category badge: Hebrew
js = js.replace(
    '<span class="card-category-badge">${recipe.categoryEn}</span>',
    '<span class="card-category-badge">${recipe.categoryHe}</span>'
)
# Card meta: Hebrew time unit
js = js.replace(
    "<span class=\"card-meta-item\">🕐 ${totalTime} min</span>",
    "<span class=\"card-meta-item\">🕐 ${totalTime} דק'</span>"
)
# Difficulty to Hebrew in card
js = js.replace(
    '<span class="card-meta-item">${recipe.difficulty}</span>',
    """<span class="card-meta-item">${{'Easy':'קל','Medium':'בינוני','Hard':'מאתגר'}[recipe.difficulty] || recipe.difficulty}</span>"""
)

# Nav HTML in getNavHTML
js = js.replace("'>Home</a>", "'>בית</a>")
js = js.replace("'>Recipes</a>", "'>מתכונים</a>")
js = js.replace("'>History</a>", "'>היסטוריה</a>")
js = js.replace("'>Techniques</a>", "'>טכניקות</a>")
js = js.replace("'>Debates</a>", "'>ויכוחים</a>")
js = js.replace('placeholder="Search..."', 'placeholder="חיפוש..."')

# Remove em dashes from JS
js = remove_em_dashes(js)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("  app.js done")

# ════════════════════════════════════════════
# 4. FIX CONTENT PAGES (history, techniques, debates, favorites, about)
# ════════════════════════════════════════════
print("\n=== Fixing content pages ===")
content_pages = ['history.html', 'techniques.html', 'debates.html', 'favorites.html', 'about.html']

for page in content_pages:
    if not os.path.exists(page):
        print(f"  SKIP {page} (not found)")
        continue
    with open(page, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # lang
    html = html.replace('<html lang="en">', '<html lang="he" dir="rtl">')
    
    # Nav links (same as recipes)
    html = html.replace('>Home</a>', '>בית</a>')
    html = html.replace('>Recipes</a>', '>מתכונים</a>')
    html = html.replace('>All Recipes</a>', '>כל המתכונים</a>')
    html = html.replace('>History</a>', '>היסטוריה</a>')
    html = html.replace('>Techniques</a>', '>טכניקות</a>')
    html = html.replace('>Debates</a>', '>ויכוחים</a>')
    html = html.replace('>Favorites</a>', '>מועדפים</a>')
    html = html.replace('>About</a>', '>אודות</a>')
    
    # Mobile nav
    html = html.replace('🏠 Home', '🏠 בית')
    html = html.replace('📖 All Recipes', '📖 כל המתכונים')
    html = html.replace('🍳 All Recipes', '🍳 כל המתכונים')
    html = html.replace('📜 History', '📜 היסטוריה')
    html = html.replace('👨\u200d🍳 Techniques', '👨\u200d🍳 טכניקות')
    html = html.replace('⚡ Debates', '⚡ ויכוחים')
    html = html.replace('❤️ Favorites', '❤️ מועדפים')
    html = html.replace('ℹ️ About', 'ℹ️ אודות')
    
    # Search
    html = html.replace('placeholder="Search recipes..."', 'placeholder="חיפוש מתכונים..."')
    html = html.replace('aria-label="Search recipes"', 'aria-label="חיפוש מתכונים"')
    html = html.replace('aria-label="Favorites"', 'aria-label="מועדפים"')
    html = html.replace('aria-label="Toggle theme"', 'aria-label="החלפת ערכת נושא"')
    html = html.replace('aria-label="Toggle menu"', 'aria-label="תפריט"')
    
    # Footer
    html = html.replace('<h4>🍳 Shakshuka</h4>', '<h4>🍳 שקשוקה</h4>')
    html = html.replace('<h4>Categories</h4>', '<h4>קטגוריות</h4>')
    html = html.replace('<h4>Explore</h4>', '<h4>גלו</h4>')
    html = html.replace('<h4>About This Project</h4>', '<h4>על הפרויקט</h4>')
    html = html.replace('>Classic Red</a>', '>קלאסית אדומה</a>')
    html = html.replace('>Green</a>', '>ירוקה</a>')
    html = html.replace('>With Cheese</a>', '>עם גבינות</a>')
    html = html.replace('>With Meat</a>', '>עם בשר</a>')
    html = html.replace('>Fusion &amp; Modern</a>', ">פיוז'ן ומודרני</a>")
    html = html.replace('>History &amp; Origins</a>', '>היסטוריה ומקורות</a>')
    html = html.replace('>Great Debates</a>', '>ויכוחים גדולים</a>')
    html = html.replace('>My Favorites</a>', '>המועדפים שלי</a>')
    html = html.replace('>Learn More →</a>', '>קראו עוד ←</a>')
    
    # Page-specific titles
    if page == 'favorites.html':
        html = html.replace('<title>Favorites', '<title>מועדפים')
        html = html.replace('<title>My Favorites', '<title>המועדפים שלי')
        html = html.replace('>My Favorite Recipes</h', '>המתכונים המועדפים שלי</h')
        html = html.replace('>No favorites yet', '>עדיין אין מועדפים')
        html = html.replace("haven't saved any favorites", 'עדיין לא שמרתם מועדפים')
        html = html.replace('Start exploring recipes', 'התחילו לגלות מתכונים')
        html = html.replace('>Browse Recipes</a>', '>לכל המתכונים</a>')
        html = html.replace('>Browse All Recipes</a>', '>לכל המתכונים</a>')
    
    if page == 'about.html':
        html = html.replace('<title>About', '<title>אודות')
    
    if page == 'history.html':
        html = html.replace('<title>History', '<title>היסטוריה')
    
    if page == 'techniques.html':
        html = html.replace('<title>Techniques', '<title>טכניקות')
    
    if page == 'debates.html':
        html = html.replace('<title>Debates', '<title>ויכוחים')
        html = html.replace('<title>The Great Debates', '<title>הויכוחים הגדולים')
    
    # Remove em dashes
    html = remove_em_dashes(html)
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  {page} done")

# ════════════════════════════════════════════
# 5. Final em-dash sweep across ALL files
# ════════════════════════════════════════════
print("\n=== Final em-dash sweep ===")
all_files = ['index.html', 'js/app.js'] + [f'recipes/{f}' for f in os.listdir('recipes') if f.endswith('.html')] + content_pages
em_dash_count = 0
for fpath in all_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if '—' in content or '–' in content:
        content = remove_em_dashes(content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        em_dash_count += 1
        print(f"  Cleaned dashes in {fpath}")

if em_dash_count == 0:
    print("  No remaining dashes found!")

print("\n✅ All done!")
