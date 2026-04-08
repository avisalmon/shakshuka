"""Download images for the shakshuka recipe website from Unsplash."""

import os
import requests
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HERO_DIR = os.path.join(BASE_DIR, "images", "hero")
RECIPE_DIR = os.path.join(BASE_DIR, "images", "recipes")

UNSPLASH_BASE = "https://images.unsplash.com/photo-{id}?w={w}&h={h}&fit=crop&q=80"

# Hero images - wide format for banner/hero sections
HERO_IMAGES = {
    "hero-1": "1593560708920-61dd98c46a4e",   # shakshuka
    "hero-2": "1590412200988-a436970781fa",   # shakshuka eggs
    "hero-3": "1615937722923-67f6deaf2cc9",   # shakshuka
    "hero-4": "1567620905732-2d1ec7ab7445",   # food photography
    "hero-5": "1466637574441-749b8f19452f",   # cooking
}

# Recipe images - mapped to relevant food photo IDs (all unique)
RECIPE_IMAGES = {
    "best-recipe-no-onion":              "1574484284002-952d92456975",  # tomato cooking
    "bino-gabso-dr-shakshuka":           "1546069901-ba9599a7e63c",    # eggs in pan
    "bulgarian-cheese-hashef-halavan":   "1623428187969-5da2dcea5ebf",  # shakshuka top view
    "cheese-shakshuka-mutti":            "1484980972926-edee96e0960d",  # cheese dish
    "classic-shakshuka-orly-shaylee":    "1565299624946-b28f40a0ae38",  # food platter
    "community-museum-simcha-yosef":     "1485963631004-f2f00b1d6606",  # community meal
    "eggplant-shakshuka-leiza-panels":   "1555939594-58d7cb561ad1",    # healthy food
    "eggplant-vegan-cheese-christoph":   "1540189549336-e6e99c3679fe",  # tomato sauce
    "eyal-shani-minimalist":             "1512621776951-a57141f2eefd",  # vegetables
    "italian-shakshuka-eitan-acqua":     "1498837167922-ddd27525d352",  # food
    "jerusalem-scrambled-edi-mizrachi":  "1504674900247-0877df9cc836",  # scrambled eggs
    "kids-friendly-anat-label":          "1482049016688-2d3e1b311543",  # kid-friendly food
    "merguez-shakshuka-rafi-cohen":      "1529042410759-befb1204b468",  # sausage dish
    "optimal-red-synthesis":             "1518779578993-ec3579fee39f",  # red sauce
    "quick-canned-rotem-liberzon":       "1556909114-f6e7ad7d3136",    # quick cooking
    "racheli-krut-most-delicious":       "1547592180-85f173990554",    # delicious meal
    "rafi-cohen-chef":                   "1414235077428-338989a2e8c0",  # chef cooking
    "sarit-atar-homestyle":              "1505253716362-afaea1d3d1af",  # home cooking
    "shakshuka-potatoes-ron":            "1596797038530-2c107229654b",  # potatoes dish
    "single-pan-moshik-roth":            "1490645935967-10de6ba17061",  # single pan
    "spinach-feta-shir-halpern":         "1473093295043-cdd812d0e601",  # spinach dish
    "spinach-mushroom-mozzarella-wine":  "1504544750208-dc0358e63f7f",  # mushroom dish
    "thai-green-shakshuka-curry":        "1455619452474-d2be8b1e70cd",  # thai green curry
    "yolk-only-hila-alpert":             "1510693206972-df098062cb71",  # egg yolk
}

PLACEHOLDER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="#e74c3c"/>
  <text x="50%" y="45%" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="24" dy=".3em">🍳</text>
  <text x="50%" y="60%" text-anchor="middle" fill="white" font-family="Arial,sans-serif" font-size="14" dy=".3em">{name}</text>
</svg>"""


PROXIES = {
    "http": "http://proxy-dmz.intel.com:911",
    "https": "http://proxy-dmz.intel.com:912",
}


def download_image(photo_id, dest_path, width=800, height=600):
    """Download a single image from Unsplash. Returns (success, file_size)."""
    url = UNSPLASH_BASE.format(id=photo_id, w=width, h=height)
    try:
        resp = requests.get(url, timeout=30, allow_redirects=True, proxies=PROXIES)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"  WARNING: Got non-image content-type: {content_type}")
            return False, 0
        with open(dest_path, "wb") as f:
            f.write(resp.content)
        size = len(resp.content)
        print(f"  OK: {os.path.basename(dest_path)} ({size:,} bytes)")
        return True, size
    except Exception as e:
        print(f"  FAIL: {os.path.basename(dest_path)} - {e}")
        return False, 0


def create_placeholder(dest_path, name, width=800, height=600):
    """Create a placeholder SVG when download fails."""
    svg_path = dest_path.rsplit(".", 1)[0] + ".svg"
    svg_content = PLACEHOLDER_SVG.format(w=width, h=height, name=name)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    size = os.path.getsize(svg_path)
    print(f"  PLACEHOLDER: {os.path.basename(svg_path)} ({size:,} bytes)")
    return size


def main():
    os.makedirs(HERO_DIR, exist_ok=True)
    os.makedirs(RECIPE_DIR, exist_ok=True)

    results = {"downloaded": [], "failed": [], "placeholders": []}
    total_size = 0

    # Download hero images (wider aspect ratio)
    print("=" * 60)
    print("Downloading HERO images...")
    print("=" * 60)
    for name, photo_id in HERO_IMAGES.items():
        dest = os.path.join(HERO_DIR, f"{name}.jpg")
        ok, size = download_image(photo_id, dest, width=1600, height=900)
        if ok:
            results["downloaded"].append(f"hero/{name}.jpg")
            total_size += size
        else:
            psize = create_placeholder(dest, name, 1600, 900)
            results["failed"].append(f"hero/{name}.jpg")
            results["placeholders"].append(f"hero/{name}.svg")
            total_size += psize
        time.sleep(0.5)  # be polite to servers

    # Download recipe images
    print()
    print("=" * 60)
    print("Downloading RECIPE images...")
    print("=" * 60)
    for slug, photo_id in RECIPE_IMAGES.items():
        dest = os.path.join(RECIPE_DIR, f"{slug}.jpg")
        ok, size = download_image(photo_id, dest, width=800, height=600)
        if ok:
            results["downloaded"].append(f"recipes/{slug}.jpg")
            total_size += size
        else:
            psize = create_placeholder(dest, slug, 800, 600)
            results["failed"].append(f"recipes/{slug}.jpg")
            results["placeholders"].append(f"recipes/{slug}.svg")
            total_size += psize
        time.sleep(0.3)

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Downloaded: {len(results['downloaded'])} images")
    print(f"Failed:     {len(results['failed'])} images")
    print(f"Placeholders created: {len(results['placeholders'])}")
    print(f"Total size: {total_size:,} bytes ({total_size / 1024 / 1024:.1f} MB)")

    if results["failed"]:
        print("\nFailed downloads:")
        for f in results["failed"]:
            print(f"  - {f}")

    if results["downloaded"]:
        print("\nSuccessful downloads:")
        for d in results["downloaded"]:
            print(f"  + {d}")


if __name__ == "__main__":
    main()
