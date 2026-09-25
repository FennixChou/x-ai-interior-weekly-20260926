import json
from pathlib import Path
from html import escape as e
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'v2/report-data.json').read_text(encoding='utf-8'))
d = DATA
def link(url, text):
    return f'<a href="{e(url, quote=True)}" target="_blank" rel="noopener noreferrer">{e(text)} ↗</a>'
def refs(ids):
    return ' '.join(f'<a class="ref" href="#{i}">{i}</a>' for i in ids)
def lis(items):
    return ''.join(f'<li>{e(x)}</li>' for x in items)
def local(t):
    return datetime.fromisoformat(t.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=8))).strftime('%m/%d %H:%M')

cards = []
for c in d['cases']:
    tags = ''.join(f'<span class="tag">{e(x)}</span>' for x in c['categories'])
    facts = ''.join(f'<div><dt>{name}</dt><dd>{e(c[key])}</dd></div>' for name,key in [('原文說了什麼','claim'),('工作方法','method'),('不能推論什麼','limit'),('可借用的做法','lesson'),('成果檔狀態','artifact')])
    more = link(c['related'],'發布者方法與數據') if c.get('related') else ''
    search = e(' '.join([c['title'],c['model'],c['author'],*c['categories']]), quote=True)
    cards.append(f'''<article class="case" id="{c['id']}" data-cats="{e('|'.join(c['categories']))}" data-search="{search}">
    <div class="case-top"><span class="eyebrow">{c['id']} / {e(c['kind'])}</span><span class="grade">證據 {c['grade']}</span></div>
    <h3>{e(c['title'])}</h3><p class="meta">{e(c['author'])} · @{e(c['handle'])}<br><time datetime="{c['utc']}">2026/{local(c['utc'])}</time> 台灣時間</p>
    <div class="tags">{tags}</div><p class="model">{e(c['model'])}</p><dl>{facts}</dl>
    <footer>{link(c['url'],'查看 X 原文')} {more}</footer></article>''')
sections = ''.join(f'''<article class="analysis"><span class="eyebrow">0{i+1} / {e(s['name'])}</span><h3>{e(s['headline'])}</h3><p>{e(s['body'])}</p><p class="insight">{e(s['inference'])}</p><p>{e(s['test'])}</p><div>{refs(s['refs'])}</div></article>''' for i,s in enumerate(d['sections']))
bench = ''.join(f'''<tr><th scope="row">{e(r['name'])}</th><td>{r['overall']:.2f} ± {r['ci']:.2f}</td><td>{r['create']:.2f}</td><td>{r['edit']:.2f}</td><td>{r['image']:.2f}</td><td>{r['perfect']}</td><td>${r['cost']:.2f}</td></tr>''' for r in d['benchmark']['rows'])
models = ''.join(f'<div><h3>{e(m["name"])}</h3><p>{e(m["text"])}</p>{link(m["url"],"官方來源")}</div>' for m in d['models'])
workflow = ''.join(f'<div class="step"><span>0{i+1}</span><h3>{e(w["title"])}</h3><p>{e(w["text"])}</p></div>' for i,w in enumerate(d['workflow']))
background = ''.join(f'<article><h3>{e(b["title"])}</h3><p class="meta">{e(b["date"])}</p><p>{e(b["text"])}</p>{link(b["url"],"背景原文")}</article>' for b in d['background'])
filters = ''.join(f'<button type="button" data-filter="{e(s["name"])}" aria-pressed="false">{e(s["name"])}</button>' for s in d['sections'])
html = f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(d['title'])}｜2026.09.26 v2</title><meta name="description" content="14 則本週 X 原文深讀：Opus 5.5、GPT-6 Astra 在 CAD、SketchUp、室內建模、風格生圖與效果圖的證據、限制及可實作方法。">
<link rel="stylesheet" href="style.css"></head><body>
<a class="skip" href="#main">跳至內容</a><header class="top"><a href="#">FIELDNOTES / AI × SPACE</a><span>WEEK 39 · 2026 · v2</span></header>
<main id="main"><section class="hero"><div class="eyebrow">本週 X 研究 / {e(d['period'])}</div><h1>從會畫圖，<br>走向可修改的空間。</h1><p class="lead">Opus 5.5 與 GPT-6 在設計工作裡，<br class="desktop">哪些已經有證據，哪些仍只是展示？</p><p class="intro">{e(d['intro'])}</p><div class="stats"><div><strong>14</strong><span>核讀 X 原文</span></div><div><strong>9</strong><span>作者／帳號</span></div><div><strong>5</strong><span>應用面向</span></div><div><strong>0</strong><span>本輪原檔重現</span></div></div><p class="meta">蒐集截止：2026/9/26 03:55（台灣） · 原文核讀不代表成果已重現</p></section>
<nav class="toc" aria-label="報告章節"><a href="#findings">五項發現</a><a href="#bench">CAD 數據</a><a href="#analysis">深度分析</a><a href="#cases">14 則原文</a><a href="#practice">實作建議</a><a href="#method">研究方法</a></nav>
<section id="findings"><div class="section-head"><span class="eyebrow">01 / EXECUTIVE READOUT</span><h2>先看這五件事</h2></div><ol class="takeaways">{lis(d['takeaways'])}</ol><div class="model-grid">{models}</div></section>
<section id="bench"><div class="section-head"><span class="eyebrow">02 / READ THE BENCHMARK</span><h2>61.03 分，不等於 61% 的案件能交付。</h2></div><p>{e(d['benchmark']['method'])}</p><div class="table-wrap" tabindex="0" role="region" aria-label="CAD 評測比較表，可水平捲動"><table><caption>CAD Bench V3｜分數 0–100；± 為 95% 信賴區間半寬</caption><thead><tr><th>模型＋執行工具</th><th>總分 ± CI</th><th>建立</th><th>建立＋修改</th><th>圖轉 CAD</th><th>滿分任務</th><th>評測成本 USD</th></tr></thead><tbody>{bench}</tbody></table></div><p class="notice">{e(d['benchmark']['caution'])}</p><p>{refs(['X01'])} {link(d['benchmark']['url'],'評測方法與完整表')}</p></section>
<section id="analysis"><div class="section-head"><span class="eyebrow">03 / FIVE APPLICATIONS</span><h2>五個面向，五種驗收方式。</h2></div><div class="analysis-grid">{sections}</div></section>
<section id="cases"><div class="section-head"><span class="eyebrow">04 / SOURCE-BY-SOURCE</span><h2>逐篇原文與判讀</h2><p>先讀作者實際說了什麼，再看證據缺口。A／B／C 代表資料完整度，不是模型排名。</p></div><div class="controls"><div class="filters" aria-label="依應用面向篩選"><button type="button" data-filter="all" aria-pressed="true">全部</button>{filters}</div><label for="query">搜尋模型、作者或案例<input id="query" type="search" placeholder="例如：Astra、Higgsfield、SketchUp"></label><p id="count" role="status" aria-live="polite">顯示 14 / 14 則</p></div><div class="case-grid">{''.join(cards)}</div><p id="empty" hidden>沒有符合條件的案例，請更換分類或搜尋詞。</p></section>
<section id="practice"><div class="section-head"><span class="eyebrow">05 / WHAT TO TRY NEXT</span><h2>適合設計工作室的小型驗證流程</h2><p>以下是根據文獻整理的試驗建議，並非本報告已執行的測試成果。</p></div><div class="workflow">{workflow}</div><aside class="limitations"><h3>這份研究還不能回答的事</h3><ul>{lis(d['gaps'])}</ul></aside></section>
<section id="method"><div class="section-head"><span class="eyebrow">06 / METHOD & PROVENANCE</span><h2>讓每個結論都有邊界。</h2></div><ol class="method-list">{lis(d['methodology'])}</ol><div class="background"><span class="eyebrow">補充背景 / 不計入 X 樣本</span>{background}</div><p class="downloads"><a href="report-data.json" download>下載研究資料 JSON</a><a href="../index.html">查看既有週報</a></p><p class="meta">既有週報的觀察窗為 9/19–9/25；本版使用已確認的本週 9/21–9/26 範圍，兩版分開保留。</p></section>
</main><footer class="site-footer"><strong>AI × SPACE / FIELDNOTES</strong><span>2026.09.26 · v2 · 原創研究 CC BY-SA 4.0<br>第三方貼文與媒體權利歸原作者；本站不鏡像發布媒體。</span></footer><script src="app.js"></script></body></html>'''
(ROOT/'v2/index.html').write_text(html,encoding='utf-8')
print(f'Built v2/index.html: {len(d["cases"])} sources, {len(set(c["handle"] for c in d["cases"]))} authors')
