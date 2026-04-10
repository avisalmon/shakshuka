#!/usr/bin/env python3
"""Build recipe HTML pages from verified data/recipes.json."""
import json, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
RECIPES_JSON = os.path.join(ROOT, "data", "recipes.json")
RECIPES_DIR = os.path.join(ROOT, "recipes")

CAT_COLORS = {"classic-red":("#C0392B","#E74C3C"),"cheese":("#E67E22","#F39C12"),"green":("#27AE60","#2ECC71"),"meat":("#8E44AD","#9B59B6"),"fusion":("#2980B9","#3498DB")}
BADGE = {"classic-red":"#E74C3C","cheese":"#F39C12","green":"#27AE60","meat":"#9B59B6","fusion":"#3498DB"}

def pmin(s):
    m=re.search(r'(\d+)',str(s))
    return int(m.group(1)) if m else 0

def fmti(i):
    p=[]
    if i.get("amount"): p.append(str(i["amount"]))
    if i.get("unit"): p.append(i["unit"])
    p.append(i["item"])
    return " ".join(p)

def dbl(a):
    if not a: return a
    fr={"1/2":"1","1/3":"2/3","1/4":"1/2","2/3":"1 1/3","3/4":"1 1/2"}
    if a in fr: return fr[a]
    m=re.match(r'^(\d+)-(\d+)$',a)
    if m: return f"{int(m.group(1))*2}-{int(m.group(2))*2}"
    try:
        v=float(a.replace(",","."));d=v*2
        return str(int(d)) if d==int(d) else str(d)
    except: return a

def rel_cards(cur,all_r):
    rel=[r for r in all_r if r["category"]==cur["category"] and r["slug"]!=cur["slug"]]
    if len(rel)<3: rel+=[r for r in all_r if r["slug"]!=cur["slug"] and r not in rel]
    rel=rel[:3]
    if not rel: return ""
    h=""
    for r in rel:
        t=pmin(r.get("prepTime","0"))+pmin(r.get("cookTime","0"))
        bc=BADGE.get(r["category"],"#999")
        ip=os.path.join(ROOT,r.get("image",""))
        ih=f'<img src="../{r["image"]}" alt="{r["titleHe"]}" loading="lazy">' if r.get("image") and os.path.exists(ip) else f'<div class="card-image-placeholder"><span>{r["titleHe"]}</span></div>'
        h+=f'<a href="{r["slug"]}.html" class="recipe-card related-card" data-recipe="{r["slug"]}" style="text-decoration:none;color:inherit;"><div class="card-image">{ih}</div><div class="card-body"><h4 class="card-title" dir="rtl">{r["titleHe"]}</h4><div class="card-meta"><span style="color:{bc};">{r.get("categoryHe","")}</span><span>{t} דק\'</span></div></div><button class="card-favorite-btn" data-recipe="{r["slug"]}" aria-label="מועדף">&#x1F90D;</button></a>\n'
    return f'<section class="related-section"><div class="container"><h3>&#x1F373; אולי תאהבו גם</h3><div class="related-grid">{h}</div></div></section>'

def build(r,all_r):
    s=r["slug"];c1,c2=CAT_COLORS.get(r.get("category","classic-red"),("#C0392B","#E74C3C"));bc=BADGE.get(r.get("category","classic-red"),"#E74C3C")
    prep=pmin(r.get("prepTime","0"));cook=pmin(r.get("cookTime","0"));total=prep+cook;svgs=str(r.get("servings",""))
    hbg=f"background-image:url('../{r['image']}');background-size:cover;background-position:center;" if r.get("image") else ""
    il="\n".join(f'<li class="ingredient-item"><label><input type="checkbox" class="ingredient-checkbox" data-ingredient="{i.get("item","")}" data-amount="{i.get("amount","")}" data-unit="{i.get("unit","")}"> <span class="ingredient-text" dir="rtl">{fmti(i)}</span></label></li>' for i in r.get("ingredients",[]))
    sl="\n".join(f'<li class="step-item"><span class="step-number">{j+1}</span><div class="step-content"><p dir="rtl">{st}</p></div></li>' for j,st in enumerate(r.get("steps",[])))
    tips=r.get("proTips",[])
    th=f'<div class="pro-tips"><h3>&#x1F4A1; טיפים מקצועיים</h3><ul>{"".join(f"<li dir=rtl>{t}</li>" for t in tips)}</ul></div>' if tips else ""
    tags=r.get("tags",[])
    tagh='<div class="recipe-tags">'+"".join(f'<span class="recipe-tag">{t}</span>' for t in tags)+'</div>' if tags else ""
    src=r.get("sourceUrl","")
    srch=f'<div class="source-attribution" style="margin:16px 0;padding:12px 20px;background:var(--bg-card,#fff);border-right:4px solid var(--accent,#C0392B);border-radius:8px;font-size:0.95rem;"><span style="opacity:0.7;">&#x1F4D6; מקור המתכון:</span> <a href="{src}" target="_blank" rel="noopener noreferrer" style="color:var(--accent,#C0392B);text-decoration:none;font-weight:600;margin-right:8px;">{r["author"]}</a> <span style="opacity:0.5;font-size:0.85em;">&#x2197;</span></div>' if src else ""
    relh=rel_cards(r,all_r)
    x1j=json.dumps([fmti(i) for i in r.get("ingredients",[])],ensure_ascii=False)
    x2j=json.dumps([fmti({**i,"amount":dbl(i.get("amount",""))}) for i in r.get("ingredients",[])],ensure_ascii=False)
    p2=max(prep,int(prep*1.3));ck2=max(cook,int(cook*1.4));t2=p2+ck2
    mr=re.match(r'^(\d+)-(\d+)$',svgs);ms=re.match(r'^(\d+)$',svgs)
    s2=f"{int(mr.group(1))*2}-{int(mr.group(2))*2}" if mr else (str(int(ms.group(1))*2) if ms else svgs)
    return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{r["titleHe"]} | שקשוקה</title>
  <link rel="stylesheet" href="../css/style.css">
  <script src="../js/app.js" defer></script>
</head>
<body>
<nav class="navbar"><div class="nav-container">
  <a href="../index.html" class="nav-logo"><span>&#x1F373;</span> שקשוקה</a>
  <div class="nav-links">
    <a href="../index.html" class="nav-link">בית</a>
    <a href="../index.html#recipes" class="nav-link">מתכונים</a>
    <a href="../history.html" class="nav-link">היסטוריה</a>
    <a href="../techniques.html" class="nav-link">טכניקות</a>
    <a href="../debates.html" class="nav-link">ויכוחים</a>
  </div>
  <div class="nav-actions">
    <div class="search-container" style="max-width:200px;">
      <span class="search-icon">&#x1F50D;</span>
      <input type="text" class="search-input" placeholder="חיפוש מתכונים..." aria-label="חיפוש מתכונים">
      <div class="search-results"></div>
    </div>
    <a href="../favorites.html" class="nav-favorites" aria-label="מועדפים">&#x2764;&#xFE0F; <span class="favorites-badge" style="display:none">0</span></a>
    <button class="theme-toggle" aria-label="החלפת ערכת נושא">&#x1F319;</button>
    <button class="hamburger" aria-label="תפריט"><span></span><span></span><span></span></button>
  </div>
</div></nav>
<div class="mobile-overlay"></div>
<div class="mobile-nav">
  <a href="../index.html" class="mobile-nav-link">&#x1F3E0; בית</a>
  <a href="../index.html#recipes" class="mobile-nav-link">&#x1F373; כל המתכונים</a>
  <a href="../history.html" class="mobile-nav-link">&#x1F4DC; היסטוריה</a>
  <a href="../techniques.html" class="mobile-nav-link">&#x1F468;&#x200D;&#x1F373; טכניקות</a>
  <a href="../debates.html" class="mobile-nav-link">&#x2694; ויכוחים</a>
  <a href="../favorites.html" class="mobile-nav-link">&#x2764;&#xFE0F; מועדפים</a>
  <a href="../about.html" class="mobile-nav-link">&#x2139;&#xFE0F; אודות</a>
</div>

<section class="recipe-hero" style="{hbg}">
  <div class="hero-overlay" style="background:linear-gradient(135deg,{c1}cc,{c2}99);">
    <div class="hero-content">
      <span class="recipe-tag" style="background:{bc};color:#fff;font-size:0.9rem;padding:6px 16px;border-radius:20px;display:inline-block;margin-bottom:12px;">{r.get("categoryHe","")}</span>
      <h1>{r["titleHe"]}</h1>
      <p style="opacity:0.9;margin-top:8px;">מאת {r["author"]}</p>
    </div>
  </div>
</section>

<main class="recipe-detail"><div class="container">
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <a href="../index.html">בית</a> &rsaquo; <a href="../index.html#recipes">מתכונים</a> &rsaquo; <span class="breadcrumb-current">{r["titleEn"]}</span>
  </nav>

  <div class="recipe-meta-bar">
    <div class="meta-item"><span class="meta-icon">&#x23F1;&#xFE0F;</span><span class="meta-label">הכנה</span><span class="meta-value" data-field="prep">{prep} דק׳</span></div>
    <div class="meta-item"><span class="meta-icon">&#x1F525;</span><span class="meta-label">בישול</span><span class="meta-value" data-field="cook">{cook} דק׳</span></div>
    <div class="meta-item"><span class="meta-icon">&#x23F0;</span><span class="meta-label">סה"כ</span><span class="meta-value" data-field="total">{total} דק׳</span></div>
    <div class="meta-item"><span class="meta-icon">&#x1F37D;&#xFE0F;</span><span class="meta-label">מנות</span><span class="meta-value" data-field="servings">{svgs}</span></div>
    <div class="meta-item"><span class="meta-icon">&#x1F7E2;</span><span class="meta-label">רמת קושי</span><span class="meta-value">{r.get("difficulty","קל")}</span></div>
    <div class="meta-item"><button class="meta-print-btn" onclick="window.print()" aria-label="הדפסת מתכון" title="הדפסה">&#x1F5A8;&#xFE0F;</button></div>
    <div class="meta-item"><button class="meta-fav-btn" data-recipe="{s}" aria-label="הוספה למועדפים">&#x1F90D;</button></div>
  </div>

  <div class="recipe-description"><p>{r.get("description","")}</p></div>
  {srch}
  {tagh}

  <div class="recipe-content-grid">
    <div class="ingredients-section">
      <div class="ingredients-header">
        <h3>&#x1F9FE; מרכיבים</h3>
        <button class="btn btn-sm btn-outline" id="add-shopping-list">&#x1F6D2; הוסף לרשימת קניות</button>
        <button class="btn btn-sm btn-outline" id="double-qty-btn" style="margin-right:8px;">&#xD7;2 הכפלת כמויות</button>
      </div>
      <ul class="ingredients-list">
{il}
      </ul>
    </div>
    <div class="steps-section">
      <h3>&#x1F468;&#x200D;&#x1F373; הוראות הכנה</h3>
      <ol class="steps-list">
{sl}
      </ol>
    </div>
  </div>

  {th}

  <div class="user-notes" data-recipe="{s}">
    <h3>&#x1F4DD; ההערות שלי</h3>
    <textarea class="user-notes-input" placeholder="כתבו הערות על המתכון הזה..." rows="4"></textarea>
    <button class="btn btn-sm" id="save-notes">שמירה</button>
    <span class="saved-message" style="display:none;color:#27ae60;margin-right:8px;">&#x2713; נשמר!</span>
  </div>
</div></main>

{relh}

<footer class="footer"><div class="container">
  <div class="footer-grid">
    <div><h4>&#x1F373; שקשוקה</h4><p>אתר השקשוקה של אבי סלמון</p></div>
    <div><h4>קטגוריות</h4><ul><li><a href="../index.html#classic-red">קלאסית אדומה</a></li><li><a href="../index.html#cheese">עם גבינות</a></li></ul></div>
    <div><h4>גלו</h4><ul><li><a href="../history.html">היסטוריה</a></li><li><a href="../techniques.html">טכניקות</a></li><li><a href="../debates.html">ויכוחים</a></li><li><a href="../favorites.html">מועדפים</a></li></ul></div>
    <div><h4>אודות</h4><p>10 מתכוני שקשוקה מאומתים</p><a href="../about.html">עוד</a></div>
  </div>
  <div class="footer-bottom"><p>&copy; 2025 שקשוקה</p></div>
</div></footer>

<script>
document.addEventListener('DOMContentLoaded', function() {{
  if (typeof RecentlyViewed!=='undefined'&&RecentlyViewed.add) RecentlyViewed.add('{s}');
  if (typeof initFavoriteButtons==='function') initFavoriteButtons();
  if (typeof Favorites!=='undefined'&&Favorites.updateBadge) Favorites.updateBadge();
  var na=document.querySelector('.user-notes-input'),sb=document.getElementById('save-notes'),sm=document.querySelector('.saved-message');
  if(na&&sb){{var nk='notes_{s}',en=localStorage.getItem(nk);if(en)na.value=en;sb.addEventListener('click',function(){{localStorage.setItem(nk,na.value);if(sm){{sm.style.display='inline';setTimeout(function(){{sm.style.display='none';}},2000);}}}});}}
  var ab=document.getElementById('add-shopping-list');
  if(ab){{ab.addEventListener('click',function(){{var items=[];document.querySelectorAll('.ingredient-checkbox').forEach(function(cb){{items.push({{ingredient:cb.dataset.ingredient,amount:cb.dataset.amount,unit:cb.dataset.unit,recipe:'{s}'}});}});if(typeof ShoppingList!=='undefined'&&ShoppingList.addAll)ShoppingList.addAll(items);else{{var ex=JSON.parse(localStorage.getItem('shoppingList')||'[]');items.forEach(function(i){{ex.push(i);}});localStorage.setItem('shoppingList',JSON.stringify(ex));}}ab.textContent='\\u2713 נוסף!';setTimeout(function(){{ab.textContent='\\u1F6D2 הוסף לרשימת קניות';}},2000);}});}}
  document.querySelectorAll('.ingredient-checkbox').forEach(function(cb){{cb.addEventListener('change',function(){{if(this.checked){{var item={{ingredient:this.dataset.ingredient,amount:this.dataset.amount,unit:this.dataset.unit,recipe:'{s}'}};if(typeof ShoppingList!=='undefined'&&ShoppingList.add)ShoppingList.add(item);else{{var ex=JSON.parse(localStorage.getItem('shoppingList')||'[]');ex.push(item);localStorage.setItem('shoppingList',JSON.stringify(ex));}}}}}});}});
  var ds=false,x1={x1j},x2={x2j};
  var t1={{prep:'{prep} דק׳',cook:'{cook} דק׳',total:'{total} דק׳',servings:'{svgs}'}};
  var t2={{prep:'{p2} דק׳',cook:'{ck2} דק׳',total:'{t2} דק׳',servings:'{s2}'}};
  var db=document.getElementById('double-qty-btn');
  if(db){{db.addEventListener('click',function(){{ds=!ds;var tx=ds?x2:x1,tm=ds?t2:t1;db.textContent=ds?'\\xD71 כמות רגילה':'\\xD72 הכפלת כמויות';db.style.background=ds?'var(--accent,#e74c3c)':'';db.style.color=ds?'#fff':'';document.querySelectorAll('.ingredient-text').forEach(function(el,idx){{if(idx<tx.length)el.textContent=tx[idx];}});['prep','cook','total','servings'].forEach(function(k){{var f=document.querySelector('.meta-value[data-field="'+k+'"]');if(f)f.textContent=tm[k];}});}});}}
}});
</script>
</body></html>'''

def main():
    with open(RECIPES_JSON,"r",encoding="utf-8") as f: recipes=json.load(f)
    print(f"Loaded {len(recipes)} verified recipes")
    os.makedirs(RECIPES_DIR,exist_ok=True)
    gen=[]
    for r in recipes:
        html=build(r,recipes)
        with open(os.path.join(RECIPES_DIR,f"{r['slug']}.html"),"w",encoding="utf-8") as f: f.write(html)
        gen.append(r["slug"])
        print(f"  OK  {r['slug']}.html")
    print(f"\nGenerated {len(gen)} recipe pages")
    existing={f.replace(".html","") for f in os.listdir(RECIPES_DIR) if f.endswith(".html")}
    valid={r["slug"] for r in recipes}
    orphans=existing-valid
    if orphans:
        print(f"\nDeleting {len(orphans)} orphaned pages:")
        for o in sorted(orphans):
            os.remove(os.path.join(RECIPES_DIR,f"{o}.html"))
            print(f"  DEL {o}.html")
    return gen

if __name__=="__main__": main()
