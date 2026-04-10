#!/usr/bin/env python3
"""Download recipe images from imageUrl fields in recipes.json."""

import json
import os
import sys

import requests

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'recipes.json')
IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'images', 'recipes')
MIN_SIZE = 5 * 1024  # 5 KB minimum

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

PROXY = 'http://proxy-dmz.intel.com:911'
PROXIES = {'http': PROXY, 'https': PROXY}


def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    os.makedirs(IMAGES_DIR, exist_ok=True)

    succeeded = []
    failed = []
    skipped = []

    for recipe in recipes:
        slug = recipe.get('slug', '')
        url = recipe.get('imageUrl', '')
        dest = os.path.join(IMAGES_DIR, f'{slug}.jpg')

        # Skip if already downloaded and large enough
        if os.path.isfile(dest) and os.path.getsize(dest) >= MIN_SIZE:
            size_kb = os.path.getsize(dest) / 1024
            print(f"  EXIST {slug}: {size_kb:.1f} KB (skipped)")
            skipped.append(slug)
            continue

        if not url:
            print(f"  SKIP  {slug}: no imageUrl")
            failed.append((slug, 'no imageUrl'))
            continue

        # Try with proxy first, then without
        last_err = None
        for attempt, proxies in enumerate([PROXIES, None]):
            try:
                resp = requests.get(url, headers=HEADERS, timeout=30,
                                    allow_redirects=True, proxies=proxies)
                resp.raise_for_status()
                last_err = None
                break
            except Exception as e:
                last_err = e

        if last_err:
            print(f"  FAIL  {slug}: {last_err}")
            failed.append((slug, str(last_err)))
            continue

        resp  # from successful attempt

        if len(resp.content) < MIN_SIZE:
            print(f"  FAIL  {slug}: too small ({len(resp.content)} bytes)")
            failed.append((slug, f'too small ({len(resp.content)} bytes)'))
            continue

        with open(dest, 'wb') as out:
            out.write(resp.content)

        size_kb = len(resp.content) / 1024
        print(f"  OK    {slug}: {size_kb:.1f} KB")
        succeeded.append(slug)

    print(f"\n{'='*50}")
    print(f"Downloaded: {len(succeeded)}/{len(recipes)}")
    print(f"Skipped:    {len(skipped)} (already exist)")
    if failed:
        print(f"Failed:     {len(failed)}")
        for slug, reason in failed:
            print(f"  - {slug}: {reason}")

    return 0 if not failed else 1


if __name__ == '__main__':
    sys.exit(main())
