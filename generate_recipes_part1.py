#!/usr/bin/env python3
import json, os, html

RECIPES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'recipes.json')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes')

CAT_COLORS = {
    'classic-red': ('#C0392B','#E74C3C','#96281B'),
    'green': ('#27AE60','#2ECC71','#1E8449'),
    'cheese': ('#D4A017','#F1C40F','#8B6914'),
    'meat': ('#8B4513','#A0522D','#6B3410'),
    'fusion': ('#8E44AD','#9B59B6','#6C3483'),
}
DIFF_MAP = {'easy':('Easy','🟢'),'medium':('Medium','🟡'),'hard':('Hard','🔴')}

def e(t):
    return html.escape(str(t)) if t else ''

def nav_html():
    return '<nav class="navbar"><div class="nav-container">\n<a href="../index.html" class="nav-logo"><span>🍳</span> Shakshuka</a>\n<div class="nav-links">\n<a href="../index.html" class="nav-link">Home</a>\n<a href="../index.html#recipes" class="nav-link">Recipes</a>\n<a href="../history.html" class="nav-link">History</a>\n<a href="../techniques.html" class="nav-link">Techniques</a>\n<a href="../debates.html" class="nav-link">Debates</a>\n</div>\n<div class="nav-actions">\n<div class="search-container" style="max-width:200px;">\n<span class="search-icon">🔍</span>\n<input type="text" class="search-input" placeholder="Search recipes..." aria-label="Search recipes">\n<div class="search-results"></div>\n</div>\n<a href="../favorites.html" class="nav-favorites" aria-label="Favorites">❤️ <span class="favorites-badge" style="display:none">0</span></a>\n<button class="theme-toggle" aria-label="Toggle theme">🌙</button>\n<button class="hamburger" aria-label="Toggle menu"><span></span><span></span><span></span></button>\n</div></div></nav>\n<div class="mobile-overlay"></div>\n<div class="mobile-nav">\n<a href="../index.html" class="mobile-nav-link">🏠 Home</a>\n<a href="../index.html#recipes" class="mobile-nav-link">📖 All Recipes</a>\n<a href="../history.html" class="mobile-nav-link">📜 History</a>\n<a href="../techniques.html" class="mobile-nav-link">👨‍🍳 Techniques</a>\n<a href="../debates.html" class="mobile-nav-link">⚡ Debates</a>\n<a href="../favorites.html" class="mobile-nav-link">❤️ Favorites</a>\n<a href="../about.html" class="mobile-nav-link">ℹ️ About</a>\n</div>'

def footer_html():
    return '<footer class="footer"><div class="container"><div class="footer-grid">\n<div><h4>🍳 Shakshuka</h4><p>Celebrating Israel\'s beloved egg dish.</p></div>\n<div><h4>Categories</h4><ul><li><a href="../index.html#classic-red">Classic Red</a></li><li><a href="../index.html#green">Green</a></li><li><a href="../index.html#cheese">With Cheese</a></li><li><a href="../index.html#meat">With Meat</a></li><li><a href="../index.html#fusion">Fusion</a></li></ul></div>\n<div><h4>Explore</h4><ul><li><a href="../history.html">History</a></li><li><a href="../techniques.html">Techniques</a></li><li><a href="../debates.html">Debates</a></li><li><a href="../favorites.html">Favorites</a></li></ul></div>\n<div><h4>About</h4><p>24 shakshuka recipes from Israel\'s finest.</p><a href="../about.html">Learn more</a></div>\n</div><div class="footer-bottom"><p>© 2025 Shakshuka — Made with 🍅 and ❤️</p></div></div></footer>'

