# Plan

## Iteration 1 — Research & Source Discovery
- Read research report for 22 recipe names and attributions
- Search for real source URLs for each recipe + expanded discovery list
- Test accessibility of each URL
- Record findings in knowledge.md (min target: 8 accessible)

## Iteration 2 — Recipe Extraction + Validation + Gap Filling
- Fetch accessible sources, extract complete recipe data
- Search for more if fewer than 12
- Download real images from sources
- Write verified recipes to data/recipes.json
- Create and run validation script (re-fetch + diff)
- Write review_table.md for human verification

## Iteration 3 — Build Recipe Pages + Site Integration
- Generate recipe HTML pages from verified JSON
- Remove old unverified pages and images
- Update index.html with new recipe cards
- Verify links and images

## Iteration 4 — End-to-End Verification + Fixes
- Run validation script as independent re-check
- Verify each page renders correctly
- Fix issues, re-run validation

## Iteration 5 — Final Validation + Summary
- Final validation run — all must PASS
- Self-observation + summary email + dashboard
