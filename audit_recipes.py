"""
Audit recipe data integrity across JSON, HTML files, images, and source URLs.

Checks:
1. JSON ↔ HTML file sync (slugs match)
2. JSON ↔ image file sync
3. HTML content matches JSON (title, author, ingredients, steps)
4. Source URLs are reachable and contain relevant content
5. Cross-recipe duplicate detection (same content in different recipes)
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPES_JSON = os.path.join(BASE_DIR, "data", "recipes.json")
RECIPES_DIR = os.path.join(BASE_DIR, "recipes")
IMAGES_DIR = os.path.join(BASE_DIR, "images", "recipes")


class HTMLTextExtractor(HTMLParser):
    """Extract text content and specific elements from HTML."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.title = ""
        self.h1 = ""
        self.in_h1 = False
        self.in_title = False
        self.hero_image = ""
        self.source_url = ""
        self.ingredients = []
        self.steps = []
        self.in_ingredient = False
        self.in_step = False
        self.in_step_text = False
        self._current_tag = None
        self._ingredient_text = []
        self._step_text = []
        self.author_text = ""
        self.in_author = False
        self.data_recipe = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "section" and "recipe-hero" in attrs_dict.get("class", ""):
            style = attrs_dict.get("style", "")
            m = re.search(r"url\(['\"]?([^'\")\s]+)['\"]?\)", style)
            if m:
                self.hero_image = m.group(1)
        elif tag == "a" and self.source_url == "":
            href = attrs_dict.get("href", "")
            # Source attribution link
            if href and ("hashulchan" in href or "mako" in href or "ynet" in href
                         or "walla" in href or "krutit" in href or "saritatar" in href
                         or "chef-lavan" in href or "mutti" in href or "anumuseum" in href
                         or "lizapanelim" in href):
                self.source_url = href
        elif tag == "span" and "recipe-author" in attrs_dict.get("class", ""):
            self.in_author = True
        elif tag == "li" and "ingredient-item" in attrs_dict.get("class", ""):
            self.in_ingredient = True
            self._ingredient_text = []
        elif tag == "li" and "step-item" in attrs_dict.get("class", ""):
            self.in_step = True
        elif tag == "p" and self.in_step and "step-text" in attrs_dict.get("class", ""):
            self.in_step_text = True
            self._step_text = []
        elif tag == "button" and attrs_dict.get("data-recipe"):
            self.data_recipe = attrs_dict["data-recipe"]

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "span" and self.in_author:
            self.in_author = False
        elif tag == "li" and self.in_ingredient:
            self.in_ingredient = False
            text = "".join(self._ingredient_text).strip()
            if text:
                self.ingredients.append(text)
        elif tag == "li" and self.in_step:
            self.in_step = False
            self.in_step_text = False
        elif tag == "p" and self.in_step_text:
            self.in_step_text = False
            text = "".join(self._step_text).strip()
            if text:
                self.steps.append(text)

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_h1:
            self.h1 += data.strip()
        if self.in_author:
            self.author_text += data.strip()
        if self.in_ingredient:
            self._ingredient_text.append(data)
        if self.in_step_text:
            self._step_text.append(data)


def parse_html(filepath):
    """Parse a recipe HTML file and extract key data."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    parser = HTMLTextExtractor()
    parser.feed(content)
    return {
        "title": parser.title.strip(),
        "h1": parser.h1.strip(),
        "hero_image": parser.hero_image,
        "source_url": parser.source_url,
        "author": parser.author_text.strip(),
        "ingredients_count": len(parser.ingredients),
        "steps_count": len(parser.steps),
        "ingredients": parser.ingredients,
        "steps": parser.steps,
        "data_recipe": parser.data_recipe,
    }


def check_url_reachable(url, timeout=10):
    """Check if a URL is reachable. Returns (status_code, title_or_error)."""
    try:
        import requests
        proxies = {
            "http": "http://proxy-dmz.intel.com:911",
            "https": "http://proxy-dmz.intel.com:912",
        }
        resp = requests.get(url, timeout=timeout, proxies=proxies,
                           headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        # Extract page title
        m = re.search(r"<title[^>]*>(.*?)</title>", resp.text, re.IGNORECASE | re.DOTALL)
        title = m.group(1).strip() if m else "(no title)"
        return resp.status_code, title, resp.url
    except Exception as e:
        return 0, str(e), url


def main():
    print("=" * 70)
    print("  RECIPE DATA INTEGRITY AUDIT")
    print("=" * 70)

    # Load JSON
    with open(RECIPES_JSON, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    json_slugs = {r["slug"] for r in recipes}
    json_by_slug = {r["slug"]: r for r in recipes}

    # Get files
    html_files = {f.replace(".html", "") for f in os.listdir(RECIPES_DIR) if f.endswith(".html")}
    image_files = {f.replace(".jpg", "") for f in os.listdir(IMAGES_DIR) if f.endswith(".jpg")}

    issues = []
    warnings = []
    info = []

    # ─── CHECK 1: File existence sync ───
    print("\n" + "─" * 70)
    print("CHECK 1: JSON ↔ HTML ↔ Image file sync")
    print("─" * 70)

    missing_html = json_slugs - html_files
    extra_html = html_files - json_slugs
    missing_img = json_slugs - image_files
    extra_img = image_files - json_slugs

    if missing_html:
        for s in missing_html:
            issues.append(f"JSON recipe '{s}' has NO HTML file")
        print(f"  ❌ Missing HTML files: {missing_html}")
    if extra_html:
        for s in extra_html:
            warnings.append(f"HTML file '{s}.html' has no JSON entry")
        print(f"  ⚠️  Extra HTML files (no JSON): {extra_html}")
    if missing_img:
        for s in missing_img:
            issues.append(f"JSON recipe '{s}' has NO image file")
        print(f"  ❌ Missing images: {missing_img}")
    if extra_img:
        for s in extra_img:
            warnings.append(f"Image '{s}.jpg' has no JSON entry")
        print(f"  ⚠️  Extra images (no JSON): {extra_img}")
    if not (missing_html or extra_html or missing_img or extra_img):
        print("  ✅ All 24 JSON slugs have matching HTML and image files")

    # ─── CHECK 2: JSON ↔ HTML content comparison ───
    print("\n" + "─" * 70)
    print("CHECK 2: JSON ↔ HTML content comparison")
    print("─" * 70)

    for recipe in recipes:
        slug = recipe["slug"]
        html_path = os.path.join(RECIPES_DIR, f"{slug}.html")
        if not os.path.exists(html_path):
            continue

        html_data = parse_html(html_path)

        # Title check
        json_title = recipe["titleHe"]
        html_h1 = html_data["h1"]
        if json_title != html_h1:
            issues.append(f"[{slug}] Title mismatch: JSON='{json_title}' vs HTML h1='{html_h1}'")
            print(f"  ❌ [{slug}] Title: JSON='{json_title}' ≠ HTML='{html_h1}'")

        # Image path check
        expected_img = f"../images/recipes/{slug}.jpg"
        if html_data["hero_image"] and html_data["hero_image"] != expected_img:
            issues.append(f"[{slug}] Hero image mismatch: expected '{expected_img}', got '{html_data['hero_image']}'")
            print(f"  ❌ [{slug}] Hero image: expected '{expected_img}' got '{html_data['hero_image']}'")

        # Ingredient count
        json_ing = len(recipe.get("ingredients", []))
        html_ing = html_data["ingredients_count"]
        if json_ing != html_ing:
            issues.append(f"[{slug}] Ingredients count: JSON={json_ing} vs HTML={html_ing}")
            print(f"  ❌ [{slug}] Ingredients: JSON={json_ing} vs HTML={html_ing}")

        # Steps count
        json_steps = len(recipe.get("steps", []))
        html_steps = html_data["steps_count"]
        if json_steps != html_steps:
            issues.append(f"[{slug}] Steps count: JSON={json_steps} vs HTML={html_steps}")
            print(f"  ❌ [{slug}] Steps: JSON={json_steps} vs HTML={html_steps}")

        # data-recipe slug check
        if html_data["data_recipe"] and html_data["data_recipe"] != slug:
            issues.append(f"[{slug}] data-recipe='{html_data['data_recipe']}' doesn't match slug")
            print(f"  ❌ [{slug}] data-recipe mismatch: '{html_data['data_recipe']}'")

        # Source URL check
        json_url = recipe.get("sourceUrl", "")
        html_url = html_data["source_url"]
        if json_url and html_url:
            # Normalize for comparison
            j = json_url.rstrip("/").lower()
            h = html_url.rstrip("/").lower()
            if j != h:
                warnings.append(f"[{slug}] Source URL differs: JSON='{json_url}' vs HTML='{html_url}'")
                print(f"  ⚠️  [{slug}] Source URL: JSON≠HTML")

    if not any("CHECK 2" in str(i) for i in issues):
        count = sum(1 for r in recipes if os.path.exists(os.path.join(RECIPES_DIR, f"{r['slug']}.html")))
        # Only print OK if no issues were found in this section
        has_check2_issues = any(f"[{r['slug']}]" in i for r in recipes for i in issues)
        if not has_check2_issues:
            print(f"  ✅ All {count} recipes match between JSON and HTML")

    # ─── CHECK 3: Duplicate content detection ───
    print("\n" + "─" * 70)
    print("CHECK 3: Duplicate/similar content detection")
    print("─" * 70)

    # Check for duplicate ingredients lists
    ing_hashes = defaultdict(list)
    step_hashes = defaultdict(list)
    for recipe in recipes:
        slug = recipe["slug"]
        ing_key = tuple(sorted(i["item"] for i in recipe.get("ingredients", [])))
        step_key = tuple(s["text"] for s in recipe.get("steps", []))
        if ing_key:
            ing_hashes[ing_key].append(slug)
        if step_key:
            step_hashes[step_key].append(slug)

    for ing, slugs in ing_hashes.items():
        if len(slugs) > 1:
            issues.append(f"Identical ingredients in: {', '.join(slugs)}")
            print(f"  ❌ Same ingredients: {', '.join(slugs)}")

    for steps, slugs in step_hashes.items():
        if len(slugs) > 1:
            issues.append(f"Identical steps in: {', '.join(slugs)}")
            print(f"  ❌ Same steps: {', '.join(slugs)}")

    # Check for duplicate source URLs
    url_map = defaultdict(list)
    for recipe in recipes:
        url = recipe.get("sourceUrl", "").rstrip("/").lower()
        if url:
            url_map[url].append(recipe["slug"])
    for url, slugs in url_map.items():
        if len(slugs) > 1:
            warnings.append(f"Same source URL '{url}' for: {', '.join(slugs)}")
            print(f"  ⚠️  Same URL for multiple recipes: {', '.join(slugs)}")
            print(f"      URL: {url}")

    if not any("CHECK 3" in str(i) or "Same" in str(i) for i in issues + warnings):
        print("  ✅ No duplicate content detected")

    # ─── CHECK 4: Source URL reachability ───
    print("\n" + "─" * 70)
    print("CHECK 4: Source URL reachability (this may take a minute...)")
    print("─" * 70)

    try:
        import requests
        for recipe in recipes:
            slug = recipe["slug"]
            url = recipe.get("sourceUrl", "")
            if not url:
                warnings.append(f"[{slug}] No source URL")
                print(f"  ⚠️  [{slug}] No source URL defined")
                continue

            status, title, final_url = check_url_reachable(url)
            if status == 0:
                issues.append(f"[{slug}] URL unreachable: {url} — {title}")
                print(f"  ❌ [{slug}] UNREACHABLE: {url}")
                print(f"      Error: {title}")
            elif status >= 400:
                issues.append(f"[{slug}] URL error {status}: {url}")
                print(f"  ❌ [{slug}] HTTP {status}: {url}")
            else:
                # Check if redirected to homepage (generic page)
                if final_url.rstrip("/") != url.rstrip("/"):
                    redirect_note = f" → {final_url}"
                else:
                    redirect_note = ""
                
                # Check title relevance
                title_lower = title.lower()
                recipe_name = recipe["titleHe"]
                author = recipe.get("author", "")
                
                has_shakshuka = "שקשוקה" in title or "shakshuka" in title_lower
                has_recipe_word = "מתכון" in title or "recipe" in title_lower
                
                print(f"  {'✅' if has_shakshuka else '⚠️ '} [{slug}] HTTP {status}{redirect_note}")
                print(f"      Page title: {title[:80]}")
                
                if not has_shakshuka and not has_recipe_word:
                    warnings.append(f"[{slug}] Page title doesn't mention shakshuka: '{title[:60]}'")

    except ImportError:
        print("  ⚠️  'requests' not installed — skipping URL checks")
        print("     Install with: pip install requests")

    # ─── CHECK 5: Image file sizes ───
    print("\n" + "─" * 70)
    print("CHECK 5: Image file analysis")
    print("─" * 70)
    
    for recipe in recipes:
        slug = recipe["slug"]
        img_path = os.path.join(IMAGES_DIR, f"{slug}.jpg")
        if os.path.exists(img_path):
            size = os.path.getsize(img_path)
            if size < 5000:
                issues.append(f"[{slug}] Image suspiciously small: {size} bytes (likely placeholder)")
                print(f"  ❌ [{slug}] Image only {size} bytes — likely placeholder/broken")
            elif size < 20000:
                warnings.append(f"[{slug}] Image small: {size} bytes")
                print(f"  ⚠️  [{slug}] Image only {size:,} bytes — might be low quality")
            else:
                info.append(f"[{slug}] Image OK: {size:,} bytes")

    # ─── SUMMARY ───
    print("\n" + "=" * 70)
    print("  AUDIT SUMMARY")
    print("=" * 70)
    print(f"  Total recipes: {len(recipes)}")
    print(f"  ❌ Issues:   {len(issues)}")
    print(f"  ⚠️  Warnings: {len(warnings)}")
    print(f"  ✅ Info:     {len(info)}")

    if issues:
        print("\n  ISSUES (must fix):")
        for i, issue in enumerate(issues, 1):
            print(f"    {i}. {issue}")

    if warnings:
        print("\n  WARNINGS (review):")
        for i, w in enumerate(warnings, 1):
            print(f"    {i}. {w}")

    return len(issues)


if __name__ == "__main__":
    sys.exit(main())
