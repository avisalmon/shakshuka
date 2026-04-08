#!/usr/bin/env python3
"""Generate individual HTML recipe pages from data/recipes.json."""
import json
import os
import html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPES_JSON = os.path.join(SCRIPT_DIR, 'data', 'recipes.json')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'recipes')

CAT_COLORS = {
    'classic-red': ('#C0392B', '#E74C3C', '#96281B'),
    'green':       ('#27AE60', '#2ECC71', '#1E8449'),
    'cheese':      ('#D4A017', '#F1C40F', '#8B6914'),
    'meat':        ('#8B4513', '#A0522D', '#6B3410'),
    'fusion':      ('#8E44AD', '#9B59B6', '#6C3483'),
}

DIFF_MAP = {
    'easy':   ('Easy',   '🟢'),
    'medium': ('Medium', '🟡'),
    'hard':   ('Hard',   '🔴'),
}


def e(text):
    """HTML-escape a string."""
    return html.escape(str(text)) if text else ''


def nav_html():
    return '''<nav class="navbar">
  <div class="nav-container">
    <a href="../index.html" class="nav-logo"><span>🍳</span> Shakshuka</a>
    <div class="nav-links">
      <a href="../index.html" class="nav-link">Home</a>
      <a href="../index.html#recipes" class="nav-link">Recipes</a>
      <a href="../history.html" class="nav-link">History</a>
      <a href="../techniques.html" class="nav-link">Techniques</a>
      <a href="../debates.html" class="nav-link">Debates</a>
    </div>
    <div class="nav-actions">
      <div class="search-container" style="max-width:200px;">
        <span class="search-icon">🔍</span>
        <input type="text" class="search-input" placeholder="Search recipes..." aria-label="Search recipes">
        <div class="search-results"></div>
      </div>
      <a href="../favorites.html" class="nav-favorites" aria-label="Favorites">❤️ <span class="favorites-badge" style="display:none">0</span></a>
      <button class="theme-toggle" aria-label="Toggle theme">🌙</button>
      <button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>
<div class="mobile-overlay"></div>
<div class="mobile-nav">
  <a href="../index.html" class="mobile-nav-link">🏠 Home</a>
  <a href="../index.html#recipes" class="mobile-nav-link">🍳 All Recipes</a>
  <a href="../history.html" class="mobile-nav-link">📜 History</a>
  <a href="../techniques.html" class="mobile-nav-link">👨‍🍳 Techniques</a>
  <a href="../debates.html" class="mobile-nav-link">⚔ Debates</a>
  <a href="../favorites.html" class="mobile-nav-link">❤️ Favorites</a>
  <a href="../about.html" class="mobile-nav-link">ℹ️ About</a>
</div>'''


def footer_html():
    return '''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>🍳 Shakshuka</h4>
        <p>Celebrating Israel's beloved egg dish.</p>
      </div>
      <div>
        <h4>Categories</h4>
        <ul>
          <li><a href="../index.html#classic-red">Classic Red</a></li>
          <li><a href="../index.html#green">Green</a></li>
          <li><a href="../index.html#cheese">With Cheese</a></li>
          <li><a href="../index.html#meat">With Meat</a></li>
          <li><a href="../index.html#fusion">Fusion</a></li>
        </ul>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="../history.html">History</a></li>
          <li><a href="../techniques.html">Techniques</a></li>
          <li><a href="../debates.html">Debates</a></li>
          <li><a href="../favorites.html">Favorites</a></li>
        </ul>
      </div>
      <div>
        <h4>About</h4>
        <p>24 shakshuka recipes from Israel's finest.</p>
        <a href="../about.html">Learn more</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2025 Shakshuka &mdash; Made with ❤️ and 🍳</p>
    </div>
  </div>
</footer>'''


def build_hero(r, colors):
    c1, c2, c3 = colors
    img = r.get('image', '')
    cat_en = e(r.get('categoryEn', r['category']))
    title_en = e(r.get('titleEn', r.get('titleHe', '')))
    title_he = e(r.get('titleHe', ''))
    author_en = e(r.get('authorEn', r.get('author', '')))

    if img:
        bg = f'background-image:url(\'../{img}\');background-size:cover;background-position:center;'
    else:
        bg = f'background:linear-gradient(135deg, {c1}, {c2}, {c3});'

    return f'''<section class="recipe-hero" style="{bg}">
  <div class="hero-overlay" style="background:linear-gradient(135deg, {c1}cc, {c2}99);">
    <div class="hero-content">
      <span class="recipe-tag" style="background:{c2};color:#fff;font-size:0.9rem;padding:6px 16px;border-radius:20px;display:inline-block;margin-bottom:12px;">{cat_en}</span>
      <h1>{title_en}</h1>
      <p class="hero-hebrew" dir="rtl">{title_he}</p>
      <p style="opacity:0.9;margin-top:8px;">by {author_en}</p>
    </div>
  </div>
</section>'''


def build_breadcrumbs(r):
    title_en = e(r.get('titleEn', r.get('titleHe', '')))
    return f'''<nav class="breadcrumbs" aria-label="Breadcrumb">
  <a href="../index.html">Home</a> &rsaquo;
  <a href="../index.html#recipes">Recipes</a> &rsaquo;
  <span class="breadcrumb-current">{title_en}</span>
</nav>'''


def build_meta_bar(r):
    prep = r.get('prepTime', 0)
    cook = r.get('cookTime', 0)
    total = prep + cook
    servings = e(r.get('servings', ''))
    diff_key = r.get('difficulty', 'easy')
    diff_label, diff_emoji = DIFF_MAP.get(diff_key, ('Easy', '🟢'))
    slug = r.get('slug', '')

    return f'''<div class="recipe-meta-bar">
  <div class="meta-item"><span class="meta-icon">⏱️</span><span class="meta-label">Prep</span><span class="meta-value">{prep} min</span></div>
  <div class="meta-item"><span class="meta-icon">🔥</span><span class="meta-label">Cook</span><span class="meta-value">{cook} min</span></div>
  <div class="meta-item"><span class="meta-icon">⏰</span><span class="meta-label">Total</span><span class="meta-value">{total} min</span></div>
  <div class="meta-item"><span class="meta-icon">🍽️</span><span class="meta-label">Servings</span><span class="meta-value">{servings}</span></div>
  <div class="meta-item"><span class="meta-icon">{diff_emoji}</span><span class="meta-label">Difficulty</span><span class="meta-value">{diff_label}</span></div>
  <div class="meta-item">
    <button class="meta-fav-btn" data-recipe="{e(slug)}" aria-label="Add to favorites">🤍</button>
  </div>
</div>'''


def build_source(r):
    url = r.get('sourceUrl', '')
    if not url:
        return ''
    return f'''<div class="source-attribution">
  <p>📖 Source: <a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(url)}</a></p>
</div>'''


def build_description(r):
    desc = r.get('descriptionEn') or r.get('description', '')
    if not desc:
        return ''
    return f'<div class="recipe-description"><p>{e(desc)}</p></div>'


def build_tags(r):
    tags = r.get('tags', [])
    if not tags:
        return ''
    items = ''.join(f'<span class="recipe-tag">{e(t)}</span>' for t in tags)
    return f'<div class="recipe-tags">{items}</div>'


def build_ingredients(r):
    ingredients = r.get('ingredients', [])
    rows = []
    for i, ing in enumerate(ingredients):
        amt = e(ing.get('amount', ''))
        unit = e(ing.get('unit', ''))
        item_en = e(ing.get('itemEn', ing.get('item', '')))
        item_he = e(ing.get('item', ''))
        display = f'{amt} {unit} {item_en}'.strip()
        rows.append(
            f'<li class="ingredient-item">'
            f'<label><input type="checkbox" class="ingredient-checkbox" '
            f'data-ingredient="{item_en}" data-amount="{amt}" data-unit="{unit}"> '
            f'<span class="ingredient-text">{display}</span>'
            f'<span class="ingredient-hebrew" dir="rtl" style="display:block;font-size:0.85em;opacity:0.7;">{item_he}</span>'
            f'</label></li>'
        )
    items = '\n'.join(rows)
    return f'''<div class="ingredients-section">
  <div class="ingredients-header">
    <h3>🧾 Ingredients</h3>
    <button class="btn btn-sm btn-outline" id="add-shopping-list">🛒 Add to Shopping List</button>
  </div>
  <ul class="ingredients-list">
{items}
  </ul>
</div>'''


def build_steps(r):
    steps = r.get('steps', [])
    rows = []
    for i, step in enumerate(steps, 1):
        text_en = e(step.get('textEn', ''))
        text_he = e(step.get('text', ''))
        he_block = ''
        if text_he:
            he_block = f'<p class="step-hebrew" dir="rtl" style="font-size:0.9em;opacity:0.75;margin-top:4px;">{text_he}</p>'
        rows.append(
            f'<li class="step-item">'
            f'<span class="step-number">{i}</span>'
            f'<div class="step-content"><p>{text_en}</p>{he_block}</div>'
            f'</li>'
        )
    items = '\n'.join(rows)
    return f'''<div class="steps-section">
  <h3>👨‍🍳 Steps</h3>
  <ol class="steps-list">
{items}
  </ol>
</div>'''


def build_pro_tips(r):
    tips_en = r.get('proTipsEn', [])
    tips_he = r.get('proTips', [])
    tips = tips_en or tips_he
    if not tips:
        return ''
    items = ''.join(f'<li>{e(t)}</li>' for t in tips)
    return f'''<div class="pro-tips">
  <h3>💡 Pro Tips</h3>
  <ul>{items}</ul>
</div>'''


def build_rating(r):
    slug = e(r.get('slug', ''))
    return f'''<div class="star-rating" data-recipe="{slug}">
  <h3>⭐ Rate This Recipe</h3>
  <div class="stars">
    <span class="star" data-value="1">☆</span>
    <span class="star" data-value="2">☆</span>
    <span class="star" data-value="3">☆</span>
    <span class="star" data-value="4">☆</span>
    <span class="star" data-value="5">☆</span>
  </div>
</div>'''


def build_notes(r):
    slug = e(r.get('slug', ''))
    return f'''<div class="user-notes" data-recipe="{slug}">
  <h3>📝 My Notes</h3>
  <textarea class="user-notes-input" placeholder="Write your notes about this recipe..." rows="4"></textarea>
  <button class="btn btn-sm" id="save-notes">Save Notes</button>
  <span class="saved-message" style="display:none;color:#27ae60;margin-left:8px;">✓ Saved!</span>
</div>'''


def build_related(r, all_recipes):
    cat = r['category']
    rid = r['id']
    same_cat = [x for x in all_recipes if x['category'] == cat and x['id'] != rid]
    others = [x for x in all_recipes if x['category'] != cat and x['id'] != rid]
    pool = (same_cat + others)[:4]
    if not pool:
        return ''
    cards = []
    for rel in pool:
        slug = e(rel.get('slug', ''))
        title_en = e(rel.get('titleEn', rel.get('titleHe', '')))
        title_he = e(rel.get('titleHe', ''))
        cat_en = e(rel.get('categoryEn', rel['category']))
        diff_key = rel.get('difficulty', 'easy')
        _, diff_emoji = DIFF_MAP.get(diff_key, ('Easy', '🟢'))
        total = rel.get('prepTime', 0) + rel.get('cookTime', 0)
        img = rel.get('image', '')
        colors = CAT_COLORS.get(rel['category'], ('#888', '#aaa', '#666'))

        if img:
            img_html = f'<div class="card-image"><img src="../{img}" alt="{title_en}" loading="lazy"></div>'
        else:
            img_html = (
                f'<div class="card-image-placeholder" style="background:linear-gradient(135deg,{colors[0]},{colors[1]});">'
                f'<span class="placeholder-text">🍳</span></div>'
            )

        cards.append(f'''<a href="{slug}.html" class="recipe-card related-card" data-recipe="{slug}" style="text-decoration:none;color:inherit;">
  {img_html}
  <div class="card-body">
    <h4 class="card-title">{title_en}</h4>
    <p class="card-title-he" dir="rtl">{title_he}</p>
    <div class="card-meta">
      <span>{diff_emoji} {cat_en}</span>
      <span>⏱️ {total} min</span>
    </div>
  </div>
  <button class="card-favorite-btn" data-recipe="{slug}" aria-label="Favorite">🤍</button>
</a>''')

    grid = '\n'.join(cards)
    return f'''<section class="related-section">
  <div class="container">
    <h3>🍳 You Might Also Like</h3>
    <div class="related-grid">{grid}</div>
  </div>
</section>'''


def build_inline_script(r):
    slug = r.get('slug', '')
    recipe_id = r.get('id', 0)
    title_en = r.get('titleEn', r.get('titleHe', ''))
    # Escape for JS string
    safe_title = title_en.replace('\\', '\\\\').replace("'", "\\'")
    safe_slug = slug.replace('\\', '\\\\').replace("'", "\\'")

    return '''<script>
document.addEventListener('DOMContentLoaded', function() {{
  // Recently viewed
  if (typeof RecentlyViewed !== 'undefined' && RecentlyViewed.add) {{
    RecentlyViewed.add({{ slug: '{slug}', title: '{title}', id: {rid} }});
  }}

  // Star rating
  if (typeof initStarRating === 'function') {{
    initStarRating();
  }} else {{
    var ratingDiv = document.querySelector('.star-rating');
    if (ratingDiv) {{
      var stars = ratingDiv.querySelectorAll('.star');
      var key = 'rating_' + ratingDiv.dataset.recipe;
      var saved = localStorage.getItem(key);
      if (saved) {{
        stars.forEach(function(s) {{
          s.textContent = parseInt(s.dataset.value) <= parseInt(saved) ? '★' : '☆';
        }});
      }}
      stars.forEach(function(star) {{
        star.style.cursor = 'pointer';
        star.style.fontSize = '1.8rem';
        star.addEventListener('click', function() {{
          var val = this.dataset.value;
          localStorage.setItem(key, val);
          stars.forEach(function(s) {{
            s.textContent = parseInt(s.dataset.value) <= parseInt(val) ? '★' : '☆';
          }});
        }});
      }});
    }}
  }}

  // Favorite buttons
  if (typeof initFavoriteButtons === 'function') {{
    initFavoriteButtons();
  }}
  if (typeof Favorites !== 'undefined' && Favorites.updateBadge) {{
    Favorites.updateBadge();
  }}

  // Notes
  var notesArea = document.querySelector('.user-notes-input');
  var saveBtn = document.getElementById('save-notes');
  var savedMsg = document.querySelector('.saved-message');
  if (notesArea && saveBtn) {{
    var noteKey = 'notes_{slug}';
    var existingNote = localStorage.getItem(noteKey);
    if (existingNote) notesArea.value = existingNote;
    saveBtn.addEventListener('click', function() {{
      localStorage.setItem(noteKey, notesArea.value);
      if (savedMsg) {{
        savedMsg.style.display = 'inline';
        setTimeout(function() {{ savedMsg.style.display = 'none'; }}, 2000);
      }}
    }});
  }}

  // Shopping list
  var addAllBtn = document.getElementById('add-shopping-list');
  if (addAllBtn) {{
    addAllBtn.addEventListener('click', function() {{
      var items = [];
      document.querySelectorAll('.ingredient-checkbox').forEach(function(cb) {{
        items.push({{
          ingredient: cb.dataset.ingredient,
          amount: cb.dataset.amount,
          unit: cb.dataset.unit,
          recipe: '{slug}'
        }});
      }});
      if (typeof ShoppingList !== 'undefined' && ShoppingList.addAll) {{
        ShoppingList.addAll(items);
      }} else {{
        var existing = JSON.parse(localStorage.getItem('shoppingList') || '[]');
        items.forEach(function(item) {{ existing.push(item); }});
        localStorage.setItem('shoppingList', JSON.stringify(existing));
      }}
      addAllBtn.textContent = '✓ Added!';
      setTimeout(function() {{ addAllBtn.textContent = '🛒 Add to Shopping List'; }}, 2000);
    }});
  }}

  // Individual checkbox -> shopping list
  document.querySelectorAll('.ingredient-checkbox').forEach(function(cb) {{
    cb.addEventListener('change', function() {{
      if (this.checked) {{
        var item = {{
          ingredient: this.dataset.ingredient,
          amount: this.dataset.amount,
          unit: this.dataset.unit,
          recipe: '{slug}'
        }};
        if (typeof ShoppingList !== 'undefined' && ShoppingList.add) {{
          ShoppingList.add(item);
        }} else {{
          var existing = JSON.parse(localStorage.getItem('shoppingList') || '[]');
          existing.push(item);
          localStorage.setItem('shoppingList', JSON.stringify(existing));
        }}
      }}
    }});
  }});
}});
</script>'''.format(slug=safe_slug, title=safe_title, rid=recipe_id)


def generate_page(r, all_recipes):
    slug = r.get('slug', f"recipe-{r['id']}")
    title_en = e(r.get('titleEn', r.get('titleHe', '')))
    cat = r.get('category', 'classic-red')
    colors = CAT_COLORS.get(cat, ('#888', '#aaa', '#666'))

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_en} | Shakshuka Recipes</title>
  <link rel="stylesheet" href="../css/style.css">
  <script src="../js/app.js" defer></script>
</head>
<body>

{nav_html()}

{build_hero(r, colors)}

<main class="recipe-detail">
  <div class="container">

    {build_breadcrumbs(r)}

    {build_meta_bar(r)}

    {build_source(r)}

    {build_description(r)}

    {build_tags(r)}

    <div class="recipe-content-grid">
      {build_ingredients(r)}
      {build_steps(r)}
    </div>

    {build_pro_tips(r)}

    {build_rating(r)}

    {build_notes(r)}

  </div>
</main>

{build_related(r, all_recipes)}

{footer_html()}

{build_inline_script(r)}

</body>
</html>'''
    return slug, page


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(RECIPES_JSON, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    generated = []
    for r in recipes:
        slug, html_content = generate_page(r, recipes)
        out_path = os.path.join(OUTPUT_DIR, f'{slug}.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        generated.append(f'{slug}.html')
        print(f'  ✓ {slug}.html')

    print(f'\nGenerated {len(generated)} recipe pages in {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
