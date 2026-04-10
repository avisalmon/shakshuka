#!/usr/bin/env python3
"""Validate all recipes in recipes.json for completeness and correctness."""

import json
import os
import re
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes.json')
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

REQUIRED_FIELDS = [
    'id', 'slug', 'titleHe', 'titleEn', 'author', 'sourceUrl',
    'image', 'category', 'categoryHe', 'ingredients', 'steps'
]

URL_PATTERN = re.compile(r'^https?://.+')


def validate_recipe(recipe, idx):
    errors = []

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in recipe or recipe[field] is None:
            errors.append(f"missing field '{field}'")
        elif isinstance(recipe[field], str) and not recipe[field].strip():
            errors.append(f"empty field '{field}'")

    # sourceVerified
    if not recipe.get('sourceVerified'):
        errors.append("sourceVerified is not True")

    # sourceUrl valid
    source_url = recipe.get('sourceUrl', '')
    if source_url and not URL_PATTERN.match(source_url):
        errors.append(f"invalid sourceUrl: {source_url}")

    # Ingredients: at least 3, each with 'item'
    ingredients = recipe.get('ingredients', [])
    if isinstance(ingredients, list):
        if len(ingredients) < 3:
            errors.append(f"only {len(ingredients)} ingredients (need >=3)")
        for i, ing in enumerate(ingredients):
            if not isinstance(ing, dict) or not ing.get('item'):
                errors.append(f"ingredient[{i}] missing 'item'")
    else:
        errors.append("ingredients is not a list")

    # Steps: at least 2, each non-empty
    steps = recipe.get('steps', [])
    if isinstance(steps, list):
        if len(steps) < 2:
            errors.append(f"only {len(steps)} steps (need >=2)")
        for i, step in enumerate(steps):
            if not isinstance(step, str) or not step.strip():
                errors.append(f"step[{i}] is empty")
    else:
        errors.append("steps is not a list")

    # Image file exists
    image_path = recipe.get('image', '')
    if image_path:
        full_path = os.path.join(BASE_DIR, image_path)
        if not os.path.isfile(full_path):
            errors.append(f"image not found: {image_path}")

    # Slug matches filename pattern
    slug = recipe.get('slug', '')
    if slug and image_path:
        expected_name = f"{slug}.jpg"
        actual_name = os.path.basename(image_path)
        if actual_name != expected_name:
            errors.append(f"slug '{slug}' doesn't match image filename '{actual_name}'")

    return errors


def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    all_pass = True
    results = []

    for idx, recipe in enumerate(recipes):
        slug = recipe.get('slug', f'recipe-{idx}')
        errors = validate_recipe(recipe, idx)
        status = 'PASS' if not errors else 'FAIL'
        if errors:
            all_pass = False
        results.append((slug, status, errors))

    # Print summary table
    slug_width = max(len(r[0]) for r in results) + 2
    print(f"{'Recipe':<{slug_width}} {'Status':<8} Errors")
    print(f"{'-'*slug_width} {'-'*6}  {'-'*40}")

    for slug, status, errors in results:
        if errors:
            print(f"{slug:<{slug_width}} {status:<8} {errors[0]}")
            for e in errors[1:]:
                print(f"{'':<{slug_width}} {'':8} {e}")
        else:
            print(f"{slug:<{slug_width}} {status:<8}")

    total = len(results)
    passed = sum(1 for _, s, _ in results if s == 'PASS')
    failed = total - passed
    print(f"\n{'='*50}")
    print(f"Total: {total}  |  PASS: {passed}  |  FAIL: {failed}")

    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
