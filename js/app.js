/* ============================================
   SHAKSHUKA RECIPE SITE - Core JavaScript
   Pure Vanilla JS, No Frameworks
   ============================================ */

/* 1. Storage Manager
   ============================================ */
const Storage = {
  _prefix: 'shakshuka_',

  get(key, fallback = null) {
    try {
      const raw = localStorage.getItem(this._prefix + key);
      return raw !== null ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  },

  set(key, value) {
    try {
      localStorage.setItem(this._prefix + key, JSON.stringify(value));
    } catch {
      // Storage full or unavailable
    }
  },

  remove(key) {
    try {
      localStorage.removeItem(this._prefix + key);
    } catch {
      // Ignore
    }
  }
};

/* 2. Favorites Module
   ============================================ */
const Favorites = {
  getAll() {
    return Storage.get('favorites', []);
  },

  toggle(slug) {
    const favs = this.getAll();
    const idx = favs.indexOf(slug);
    if (idx === -1) {
      favs.push(slug);
    } else {
      favs.splice(idx, 1);
    }
    Storage.set('favorites', favs);
    this.updateBadge();
    return idx === -1;
  },

  isFavorite(slug) {
    return this.getAll().indexOf(slug) !== -1;
  },

  updateBadge() {
    const count = this.getAll().length;
    document.querySelectorAll('.favorites-badge').forEach(badge => {
      badge.textContent = count;
      badge.style.display = count > 0 ? '' : 'none';
    });
  }
};

/* 3. Ratings Module
   ============================================ */
const Ratings = {
  getAll() {
    return Storage.get('ratings', {});
  },

  get(slug) {
    return this.getAll()[slug] || 0;
  },

  set(slug, stars) {
    const all = this.getAll();
    all[slug] = stars;
    Storage.set('ratings', all);
  }
};

/* 4. Notes Module
   ============================================ */
const Notes = {
  getAll() {
    return Storage.get('notes', {});
  },

  get(slug) {
    return this.getAll()[slug] || '';
  },

  set(slug, text) {
    const all = this.getAll();
    if (text) {
      all[slug] = text;
    } else {
      delete all[slug];
    }
    Storage.set('notes', all);
  }
};

/* 5. RecentlyViewed Module
   ============================================ */
const RecentlyViewed = {
  _max: 5,

  getAll() {
    return Storage.get('recently_viewed', []);
  },

  add(slug) {
    let list = this.getAll().filter(s => s !== slug);
    list.unshift(slug);
    if (list.length > this._max) list = list.slice(0, this._max);
    Storage.set('recently_viewed', list);
  }
};

/* 6. ShoppingList Module
   ============================================ */
const ShoppingList = {
  getAll() {
    return Storage.get('shopping_list', []);
  },

  add(item) {
    const list = this.getAll();
    list.push(item);
    Storage.set('shopping_list', list);
  },

  remove(text) {
    const list = this.getAll().filter(item => item.text !== text);
    Storage.set('shopping_list', list);
  },

  clear() {
    Storage.set('shopping_list', []);
  },

  exportText() {
    return this.getAll()
      .map(item => {
        const parts = [];
        if (item.amount) parts.push(item.amount);
        if (item.unit) parts.push(item.unit);
        parts.push(item.text);
        return '• ' + parts.join(' ');
      })
      .join('\n');
  }
};

/* 7. Votes Module (Debates)
   ============================================ */
const Votes = {
  getAll() {
    return Storage.get('votes', {});
  },

  vote(questionId, option) {
    const all = this.getAll();
    all[questionId] = option;
    Storage.set('votes', all);
  },

  getVote(questionId) {
    return this.getAll()[questionId] || null;
  }
};

/* 8. Theme Module
   ============================================ */
const Theme = {
  init() {
    const saved = Storage.get('theme', null);
    if (saved) {
      document.documentElement.setAttribute('data-theme', saved);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
    this.updateIcon();
  },

  toggle() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    Storage.set('theme', next);
    this.updateIcon();
  },

  updateIcon() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.textContent = isDark ? '☀️' : '🌙';
    });
  }
};

/* 9. Navigation
   ============================================ */
function initNavigation() {
  const hamburger = document.querySelector('.hamburger');
  const mobileNav = document.querySelector('.mobile-nav');
  const overlay = document.querySelector('.mobile-overlay');

  function closeMobileNav() {
    if (hamburger) hamburger.classList.remove('active');
    if (mobileNav) mobileNav.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  function openMobileNav() {
    if (hamburger) hamburger.classList.add('active');
    if (mobileNav) mobileNav.classList.add('open');
    if (overlay) overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  if (hamburger) {
    hamburger.addEventListener('click', () => {
      const isOpen = hamburger.classList.contains('active');
      if (isOpen) {
        closeMobileNav();
      } else {
        openMobileNav();
      }
    });
  }

  if (overlay) {
    overlay.addEventListener('click', closeMobileNav);
  }

  document.querySelectorAll('.theme-toggle').forEach(btn => {
    btn.addEventListener('click', () => Theme.toggle());
  });
}

/* 10. Search
   ============================================ */
let _recipesCache = null;

async function loadRecipes() {
  if (_recipesCache) return _recipesCache;
  // Check if recipe data is available globally (inlined in index.html)
  if (window._allRecipesData) {
    _recipesCache = window._allRecipesData;
    return _recipesCache;
  }
  const isSubpage = window.location.pathname.includes('/recipes/');
  const path = isSubpage ? '../data/recipes.json' : 'data/recipes.json';
  try {
    const res = await fetch(path);
    _recipesCache = await res.json();
    return _recipesCache;
  } catch {
    return [];
  }
}

function initSearch() {
  const searchInput = document.querySelector('.search-input');
  const searchResults = document.querySelector('.search-results');
  if (!searchInput || !searchResults) return;

  let debounceTimer = null;

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      const query = searchInput.value.trim().toLowerCase();
      if (!query) {
        searchResults.innerHTML = '';
        searchResults.classList.remove('active');
        return;
      }

      const recipes = await loadRecipes();
      const isSubpage = window.location.pathname.includes('/recipes/');
      const prefix = isSubpage ? '' : 'recipes/';

      const matches = recipes.filter(r => {
        const searchable = [
          r.titleEn, r.titleHe, r.description, r.descriptionHe,
          r.categoryEn, ...(r.tags || []),
          ...(r.ingredients || []).map(i => (i.itemEn || '') + ' ' + (i.item || ''))
        ].join(' ').toLowerCase();
        return searchable.includes(query);
      }).slice(0, 8);

      if (matches.length === 0) {
        searchResults.innerHTML = '<div class="search-result-item no-results">לא נמצאו מתכונים</div>';
      } else {
        searchResults.innerHTML = matches.map(r =>
          `<a href="${prefix}${r.slug}.html" class="search-result-item">
            <span class="search-result-title">${r.titleHe}</span>
            <span class="search-result-category">${r.categoryHe}</span>
          </a>`
        ).join('');
      }
      searchResults.classList.add('active');
    }, 200);
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-bar') && !e.target.closest('.search-results')) {
      searchResults.innerHTML = '';
      searchResults.classList.remove('active');
    }
  });
}

/* 11. Star Rating
   ============================================ */
function initStarRating(container, recipeSlug) {
  if (!container) return;

  const saved = Ratings.get(recipeSlug);
  container.innerHTML = '';

  for (let i = 1; i <= 5; i++) {
    const star = document.createElement('span');
    star.className = 'star';
    star.textContent = i <= saved ? '★' : '☆';
    star.dataset.value = i;

    star.addEventListener('click', () => {
      Ratings.set(recipeSlug, i);
      updateStars(container, i);
    });

    star.addEventListener('mouseenter', () => {
      updateStars(container, i);
    });

    container.appendChild(star);
  }

  container.addEventListener('mouseleave', () => {
    updateStars(container, Ratings.get(recipeSlug));
  });
}

function updateStars(container, active) {
  container.querySelectorAll('.star').forEach(star => {
    star.textContent = parseInt(star.dataset.value) <= active ? '★' : '☆';
  });
}

/* 12. Favorite Buttons
   ============================================ */
function initFavoriteButtons() {
  const selector = '[data-favorite], .card-favorite-btn[data-recipe], .meta-fav-btn[data-recipe]';
  document.querySelectorAll(selector).forEach(btn => {
    const slug = btn.dataset.favorite || btn.dataset.recipe;
    if (!slug) return;
    btn.textContent = Favorites.isFavorite(slug) ? '❤️' : '🤍';

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const added = Favorites.toggle(slug);
      btn.textContent = added ? '❤️' : '🤍';
    });
  });
}

/* 13. Scroll Animations
   ============================================ */
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

/* 14. Recipe Card Builder
   ============================================ */
function createRecipeCard(recipe) {
  const isFav = Favorites.isFavorite(recipe.slug);
  const totalTime = (recipe.prepTime || 0) + (recipe.cookTime || 0);
  const imageContent = recipe.image
    ? `<img src="${recipe.image}" alt="${recipe.titleHe}" loading="lazy">`
    : `<div class="card-image-placeholder">
        <span class="placeholder-text">${recipe.titleHe}</span>
      </div>`;

  return `<a href="recipes/${recipe.slug}.html" class="recipe-card">
    <div class="card-image">
      ${imageContent}
      <button class="card-favorite-btn" data-favorite="${recipe.slug}">${isFav ? '❤️' : '🤍'}</button>
      <span class="card-category-badge">${recipe.categoryHe}</span>
    </div>
    <div class="card-body">
      <h3 class="card-title" dir="rtl">${recipe.titleHe}</h3>
      
      <p class="card-author" dir="rtl">${recipe.author}</p>
      <div class="card-meta">
        <span class="card-meta-item">🕐 ${totalTime} דק'</span>
        <span class="card-meta-item">🍽️ ${recipe.servings}</span>
        <span class="card-meta-item">${{'Easy':'קל','Medium':'בינוני','Hard':'מאתגר'}[recipe.difficulty] || recipe.difficulty}</span>
      </div>
    </div>
  </a>`;
}

/* 15. Navbar HTML
   ============================================ */
function getNavHTML(isSubpage = false) {
  const p = isSubpage ? '../' : '';
  return `<nav class="navbar">
    <div class="container nav-container">
      <a href="${p}index.html" class="nav-logo">🍳 Shakshuka</a>

      <div class="nav-links">
        <a href="${p}index.html" class="nav-link">Home</a>
        <a href="${p}recipes.html" class="nav-link">Recipes</a>
        <a href="${p}history.html" class="nav-link">History</a>
        <a href="${p}techniques.html" class="nav-link">Techniques</a>
        <a href="${p}debates.html" class="nav-link">Debates</a>
      </div>

      <div class="nav-actions">
        <div class="search-bar">
          <input type="text" class="search-input" placeholder="Search recipes..." aria-label="Search recipes">
          <div class="search-results"></div>
        </div>
        <a href="${p}favorites.html" class="nav-favorites" aria-label="Favorites">
          ❤️ <span class="favorites-badge" style="display:none">0</span>
        </a>
        <button class="theme-toggle" aria-label="Toggle theme">🌙</button>
        <button class="hamburger" aria-label="Toggle menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>

  <div class="mobile-overlay"></div>

  <div class="mobile-nav">
    <a href="${p}index.html" class="mobile-nav-link">Home</a>
    <a href="${p}recipes.html" class="mobile-nav-link">Recipes</a>
    <a href="${p}history.html" class="mobile-nav-link">History</a>
    <a href="${p}techniques.html" class="mobile-nav-link">Techniques</a>
    <a href="${p}debates.html" class="mobile-nav-link">Debates</a>
    <a href="${p}about.html" class="mobile-nav-link">About</a>
  </div>`;
}

/* 16. Footer HTML
   ============================================ */
function getFooterHTML(isSubpage = false) {
  const p = isSubpage ? '../' : '';
  return `<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h4 class="footer-heading">🍳 Shakshuka</h4>
          <p class="footer-about">Celebrating Israel's beloved egg dish - from the classic red to bold fusions. Recipes, history, techniques, and spirited debates.</p>
        </div>
        <div class="footer-col">
          <h4 class="footer-heading">Categories</h4>
          <ul class="footer-links">
            <li><a href="${p}recipes.html?cat=classic-red">Classic Red</a></li>
            <li><a href="${p}recipes.html?cat=green">Green</a></li>
            <li><a href="${p}recipes.html?cat=cheese">Cheese</a></li>
            <li><a href="${p}recipes.html?cat=meat">Meat</a></li>
            <li><a href="${p}recipes.html?cat=fusion">Fusion</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4 class="footer-heading">Explore</h4>
          <ul class="footer-links">
            <li><a href="${p}history.html">History &amp; Origins</a></li>
            <li><a href="${p}techniques.html">Techniques</a></li>
            <li><a href="${p}debates.html">Great Debates</a></li>
            <li><a href="${p}favorites.html">My Favorites</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4 class="footer-heading">Project</h4>
          <ul class="footer-links">
            <li><a href="${p}about.html">About</a></li>
            <li><a href="https://github.com" target="_blank" rel="noopener">GitHub</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; ${new Date().getFullYear()} Shakshuka - Made with 🍅 and ❤️</p>
      </div>
    </div>
  </footer>`;
}

/* 17. Recipe Detail Page Init
   ============================================ */
function initRecipePage() {
  const path = window.location.pathname;
  const slug = path.split('/').pop().replace('.html', '');
  if (!slug) return;

  RecentlyViewed.add(slug);

  // Star rating
  const ratingContainer = document.querySelector('.star-rating[data-recipe]');
  if (ratingContainer) {
    const recipeSlug = ratingContainer.dataset.recipe;
    const starsDiv = ratingContainer.querySelector('.stars');
    const target = starsDiv || ratingContainer;
    initStarRating(target, recipeSlug);
  }

  // User notes
  const notesSection = document.querySelector('.user-notes[data-recipe]');
  if (notesSection) {
    const noteSlug = notesSection.dataset.recipe;
    const textarea = notesSection.querySelector('.user-notes-input');
    const saveBtn = notesSection.querySelector('#save-notes');
    const savedMsg = notesSection.querySelector('.saved-message');

    if (textarea) {
      textarea.value = Notes.get(noteSlug);
    }

    if (saveBtn && textarea) {
      saveBtn.addEventListener('click', () => {
        Notes.set(noteSlug, textarea.value);
        if (savedMsg) {
          savedMsg.style.display = 'inline';
          setTimeout(() => { savedMsg.style.display = 'none'; }, 2000);
        }
      });
    }
  }

  // Shopping list - add checked ingredients
  const addShoppingBtn = document.querySelector('#add-shopping-list');
  if (addShoppingBtn) {
    addShoppingBtn.addEventListener('click', () => {
      const checked = document.querySelectorAll('.ingredient-checkbox:checked');
      let count = 0;
      checked.forEach(cb => {
        const label = cb.closest('label') || cb.parentElement;
        const text = label ? label.textContent.trim() : cb.value;
        ShoppingList.add({ text, recipe: slug });
        count++;
      });
      if (count > 0) {
        addShoppingBtn.textContent = `✓ נוספו ${count} פריטים`;
        setTimeout(() => { addShoppingBtn.textContent = '🛒 הוסף לרשימת קניות'; }, 2000);
        updateShoppingBadge();
      }
    });
  }

  // Favorite button on recipe page
  initFavoriteButtons();
}

/* 18. Shopping List Floating Button & Panel
   ============================================ */
function initShoppingListPage() {
  // Floating cart button
  const cartBtn = document.createElement('button');
  cartBtn.className = 'shopping-cart-float';
  cartBtn.setAttribute('aria-label', 'רשימת קניות');
  cartBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;width:56px;height:56px;border-radius:50%;border:none;background:var(--accent,#e74c3c);color:#fff;font-size:24px;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;';
  cartBtn.innerHTML = '🛒<span class="cart-badge" style="position:absolute;top:-4px;right:-4px;background:#333;color:#fff;border-radius:50%;min-width:20px;height:20px;font-size:12px;display:flex;align-items:center;justify-content:center;padding:2px;">0</span>';
  document.body.appendChild(cartBtn);

  // Modal overlay
  const overlay = document.createElement('div');
  overlay.className = 'shopping-modal-overlay';
  overlay.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:10000;';

  const panel = document.createElement('div');
  panel.className = 'shopping-modal-panel';
  panel.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:var(--card-bg,#fff);color:var(--text-color,#222);border-radius:12px;padding:24px;max-width:420px;width:90%;max-height:70vh;overflow-y:auto;z-index:10001;box-shadow:0 8px 32px rgba(0,0,0,.3);';

  panel.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
      <h3 style="margin:0;">🛒 רשימת קניות</h3>
      <button class="shopping-modal-close" style="background:none;border:none;font-size:20px;cursor:pointer;color:inherit;">✕</button>
    </div>
    <div class="shopping-items-list"></div>
    <div style="display:flex;gap:8px;margin-top:16px;">
      <button class="shopping-copy-btn" style="flex:1;padding:8px;border:1px solid var(--border-color,#ccc);border-radius:6px;background:var(--card-bg,#fff);color:inherit;cursor:pointer;">📋 העתק</button>
      <button class="shopping-clear-btn" style="flex:1;padding:8px;border:1px solid var(--border-color,#ccc);border-radius:6px;background:var(--card-bg,#fff);color:inherit;cursor:pointer;">🗑️ נקה הכל</button>
    </div>
  `;

  overlay.appendChild(panel);
  document.body.appendChild(overlay);

  function renderItems() {
    const items = ShoppingList.getAll();
    const list = panel.querySelector('.shopping-items-list');
    if (items.length === 0) {
      list.innerHTML = '<p style="text-align:center;opacity:.6;">רשימת הקניות ריקה</p>';
    } else {
      list.innerHTML = items.map((item, idx) =>
        `<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border-color,#eee);">
          <span>${item.text}</span>
          <button class="shopping-remove-btn" data-index="${idx}" style="background:none;border:none;cursor:pointer;font-size:16px;color:inherit;">✕</button>
        </div>`
      ).join('');
    }
    updateShoppingBadge();
  }

  cartBtn.addEventListener('click', () => {
    renderItems();
    overlay.style.display = 'block';
  });

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.style.display = 'none';
  });

  panel.querySelector('.shopping-modal-close').addEventListener('click', () => {
    overlay.style.display = 'none';
  });

  panel.querySelector('.shopping-clear-btn').addEventListener('click', () => {
    ShoppingList.clear();
    renderItems();
  });

  panel.querySelector('.shopping-copy-btn').addEventListener('click', () => {
    const text = ShoppingList.exportText();
    if (text) {
      navigator.clipboard.writeText(text).then(() => {
        const btn = panel.querySelector('.shopping-copy-btn');
        btn.textContent = '✓ Copied!';
        setTimeout(() => { btn.textContent = '📋 Copy'; }, 2000);
      });
    }
  });

  panel.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('.shopping-remove-btn');
    if (removeBtn) {
      const items = ShoppingList.getAll();
      const idx = parseInt(removeBtn.dataset.index, 10);
      if (idx >= 0 && idx < items.length) {
        ShoppingList.remove(items[idx].text);
        renderItems();
      }
    }
  });

  updateShoppingBadge();
}

function updateShoppingBadge() {
  const count = ShoppingList.getAll().length;
  document.querySelectorAll('.cart-badge').forEach(badge => {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
  });
}

/* 19. Debates Page Init
   ============================================ */
function initDebatesPage() {
  document.querySelectorAll('.debate-card[data-debate]').forEach(card => {
    const debateId = card.dataset.debate;
    const savedVote = Votes.getVote(debateId);

    // Restore saved vote state
    if (savedVote) {
      applyVoteState(card, debateId, savedVote);
    }

    card.querySelectorAll('.debate-option[data-value]').forEach(btn => {
      btn.addEventListener('click', () => {
        const option = btn.dataset.value;
        Votes.vote(debateId, option);
        applyVoteState(card, debateId, option);
      });
    });
  });
}

function applyVoteState(card, debateId, selectedOption) {
  // Highlight selected option
  card.querySelectorAll('.debate-option[data-value]').forEach(btn => {
    btn.classList.toggle('selected', btn.dataset.value === selectedOption);
  });

  // Show result bars
  const resultDiv = card.querySelector('.debate-result');
  if (resultDiv) {
    resultDiv.style.display = 'block';
    card.querySelectorAll('.debate-bar-fill[data-option]').forEach(bar => {
      bar.style.transition = 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
      bar.style.width = bar.dataset.option === selectedOption ? '65%' : '35%';
    });
  }

  // Show vote message
  let msg = card.querySelector('.vote-message');
  if (!msg) {
    msg = document.createElement('div');
    msg.className = 'vote-message';
    msg.style.cssText = 'text-align:center;margin-top:12px;font-size:0.9rem;color:var(--olive-green);font-weight:600;';
    const optionsDiv = card.querySelector('.debate-options');
    if (optionsDiv) optionsDiv.after(msg);
  }
  const label = card.querySelector(`.debate-option[data-value="${selectedOption}"] .option-label`);
  msg.textContent = `\u2713 You voted: ${label ? label.textContent : selectedOption}`;
}

/* 20. Favorites Page Init
   ============================================ */
function initFavoritesPage() {
  const grid = document.querySelector('.favorites-grid') || document.querySelector('.recipe-grid');
  if (!grid) return;

  const favSlugs = Favorites.getAll();

  if (favSlugs.length === 0) {
    const emptyMsg = document.querySelector('.favorites-empty');
    if (emptyMsg) {
      emptyMsg.style.display = 'block';
    } else {
      grid.innerHTML = '<p class="favorites-empty" style="text-align:center;padding:48px 0;opacity:.6;grid-column:1/-1;">No favorites yet. Browse recipes and tap ❤️ to save your favorites!</p>';
    }
    return;
  }

  loadRecipes().then(recipes => {
    const favRecipes = favSlugs
      .map(slug => recipes.find(r => r.slug === slug))
      .filter(Boolean);

    if (favRecipes.length === 0) {
      grid.innerHTML = '<p class="favorites-empty" style="text-align:center;padding:48px 0;opacity:.6;grid-column:1/-1;">No favorites found.</p>';
      return;
    }

    grid.innerHTML = favRecipes.map(r => createRecipeCard(r)).join('');
    initFavoriteButtons();
  });
}

/* 21. DOMContentLoaded Init
   ============================================ */
document.addEventListener('DOMContentLoaded', () => {
  Theme.init();
  initNavigation();
  initSearch();
  initFavoriteButtons();
  initScrollAnimations();
  Favorites.updateBadge();

  const path = window.location.pathname.replace(/\\/g, '/');

  // Auto-detect page type
  if (path.includes('/recipes/') || document.querySelector('.star-rating[data-recipe]')) {
    initRecipePage();
  }
  if (path.includes('debates')) {
    initDebatesPage();
  }
  if (path.includes('favorites')) {
    initFavoritesPage();
  }

  // Always show shopping list floating button
  initShoppingListPage();
});
