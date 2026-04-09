"""Add self-contained star rating initialization to each recipe page inline script."""
import os, re, glob

recipes_dir = os.path.join(os.path.dirname(__file__), 'recipes')
fixed_count = 0

STAR_INIT_CODE = """  // Star rating - self-contained init
  var ratingDiv = document.querySelector('.star-rating[data-recipe]');
  if (ratingDiv) {
    var starsDiv = ratingDiv.querySelector('.stars');
    if (starsDiv) {
      var recipeKey = 'shakshuka_ratings';
      var allRatings = {};
      try { allRatings = JSON.parse(localStorage.getItem(recipeKey) || '{}'); } catch(e) {}
      var mySlug = ratingDiv.dataset.recipe;
      var savedVal = allRatings[mySlug] || 0;
      starsDiv.innerHTML = '';
      for (var i = 1; i <= 5; i++) {
        var s = document.createElement('span');
        s.className = 'star';
        s.textContent = i <= savedVal ? '\\u2605' : '\\u2606';
        s.dataset.value = String(i);
        s.style.cssText = 'font-size:2rem;cursor:pointer;user-select:none;';
        (function(val) {
          s.addEventListener('click', function() {
            try {
              var r = JSON.parse(localStorage.getItem(recipeKey) || '{}');
              r[mySlug] = val;
              localStorage.setItem(recipeKey, JSON.stringify(r));
            } catch(e) {}
            starsDiv.querySelectorAll('.star').forEach(function(st) {
              st.textContent = parseInt(st.dataset.value) <= val ? '\\u2605' : '\\u2606';
            });
          });
          s.addEventListener('mouseenter', function() {
            starsDiv.querySelectorAll('.star').forEach(function(st) {
              st.textContent = parseInt(st.dataset.value) <= val ? '\\u2605' : '\\u2606';
            });
          });
        })(i);
        starsDiv.appendChild(s);
      }
      starsDiv.addEventListener('mouseleave', function() {
        var r2 = {};
        try { r2 = JSON.parse(localStorage.getItem(recipeKey) || '{}'); } catch(e) {}
        var cur = r2[mySlug] || 0;
        starsDiv.querySelectorAll('.star').forEach(function(st) {
          st.textContent = parseInt(st.dataset.value) <= cur ? '\\u2605' : '\\u2606';
        });
      });
    }
  }"""

for html_file in glob.glob(os.path.join(recipes_dir, '*.html')):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Replace the comment placeholder with actual working code
    content = content.replace(
        '  // Star rating handled by app.js initRecipePage()',
        STAR_INIT_CODE
    )
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
        print(f'Fixed: {os.path.basename(html_file)}')

print(f'\nDone - fixed {fixed_count} files')
