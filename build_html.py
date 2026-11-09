# -*- coding: utf-8 -*-
"""作品集看板 HTML 构建器：读 portfolio_data.json → 单文件 index.html。

设计遵循 dataviz skill：默认校验过的参考调色板、细标记、发丝网格、悬浮层、
表格孪生、深浅双主题。美观优先。
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
with io.open(os.path.join(HERE, "portfolio_data.json"), encoding="utf-8") as f:
    DATA = json.load(f)

HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>订阅业务收入成本监控看板 · 数据产品作品集</title>
<style>
  :root {
    color-scheme: light;
    --surface-1:#fcfcfb; --page:#f9f9f7;
    --ink-1:#0b0b0b; --ink-2:#52514e; --ink-3:#898781;
    --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,.10);
    --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s5:#e87ba4;
    --good:#006300;
    --tooltip-bg:#ffffff; --tooltip-ring:rgba(11,11,11,.14);
  }
  :root:where(:not([data-theme="dark"])) { }
  @media (prefers-color-scheme: dark) {
    :root:where(:not([data-theme="light"])) {
      color-scheme: dark;
      --surface-1:#1a1a19; --page:#0d0d0d;
      --ink-1:#ffffff; --ink-2:#c3c2b7; --ink-3:#898781;
      --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.10);
      --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s5:#d55181;
      --good:#0ca30c;
      --tooltip-bg:#242423; --tooltip-ring:rgba(255,255,255,.16);
    }
  }
  :root[data-theme="dark"] {
    color-scheme: dark;
    --surface-1:#1a1a19; --page:#0d0d0d;
    --ink-1:#ffffff; --ink-2:#c3c2b7; --ink-3:#898781;
    --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.10);
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s5:#d55181;
    --good:#0ca30c;
    --tooltip-bg:#242423; --tooltip-ring:rgba(255,255,255,.16);
  }
  * { box-sizing:border-box; margin:0; padding:0; }
  html { scroll-behavior:smooth; }
  body {
    font-family:system-ui,-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
    background:var(--page); color:var(--ink-1); line-height:1.6; font-size:15px;
    -webkit-font-smoothing:antialiased;
  }
  .wrap { max-width:1120px; margin:0 auto; padding:0 24px 64px; }

  /* ---------- 头部 ---------- */
  .hero { padding:64px 0 8px; }
  .kicker { font-size:13px; letter-spacing:.14em; color:var(--ink-3); font-weight:600; }
  h1 { font-size:34px; font-weight:700; letter-spacing:.01em; margin:10px 0 6px; }
  .herosub { color:var(--ink-2); font-size:15px; }
  .intro { display:grid; grid-template-columns:1.2fr 1fr 1.4fr; gap:20px; margin-top:28px;
    background:var(--surface-1); border:1px solid var(--ring); border-radius:12px; padding:24px; }
  .intro h3 { font-size:12px; color:var(--ink-3); font-weight:600; letter-spacing:.08em; margin-bottom:8px; }
  .intro p, .intro li { font-size:14px; color:var(--ink-2); }
  .intro ul { list-style:none; }
  .intro li { padding-left:16px; position:relative; margin-bottom:6px; }
  .intro li::before { content:""; position:absolute; left:0; top:.62em; width:8px; height:2px; background:var(--s1); }
  .disclaimer { margin-top:16px; display:flex; gap:8px; align-items:flex-start;
    font-size:13px; color:var(--ink-2); background:var(--surface-1);
    border:1px solid var(--ring); border-left:3px solid var(--s2); border-radius:10px; padding:12px 16px; }
  .disclaimer b { color:var(--ink-1); }

  /* ---------- 导航 + 筛选 ---------- */
  .navbar { position:sticky; top:0; z-index:30; background:var(--page);
    border-bottom:1px solid var(--ring); margin-top:36px; padding:10px 0; }
  .navbar .row { display:flex; align-items:center; gap:18px; flex-wrap:wrap; }
  .navbar a { color:var(--ink-2); text-decoration:none; font-size:14px; padding:4px 2px; }
  .navbar a:hover { color:var(--ink-1); }
  .spacer { flex:1; }
  .seg { display:flex; gap:4px; background:var(--surface-1); border:1px solid var(--ring); border-radius:9px; padding:3px; }
  .seg button { border:0; background:transparent; color:var(--ink-2); font:inherit; font-size:13px;
    padding:5px 12px; border-radius:6px; cursor:pointer; }
  .seg button[aria-pressed="true"] { background:var(--page); color:var(--ink-1); font-weight:600;
    box-shadow:inset 0 0 0 1px var(--ring); }
  .iconbtn { border:1px solid var(--ring); background:var(--surface-1); border-radius:9px;
    font-size:14px; padding:6px 10px; cursor:pointer; color:var(--ink-2); }

  /* ---------- 区块与卡片 ---------- */
  section { margin-top:44px; }
  .sec-head { display:flex; align-items:baseline; gap:12px; margin-bottom:6px; }
  .sec-no { font-size:13px; color:var(--ink-3); font-weight:600; letter-spacing:.1em; }
  h2 { font-size:21px; font-weight:700; }
  .sec-note { color:var(--ink-2); font-size:14px; margin-bottom:18px; max-width:820px; }
  .card { background:var(--surface-1); border:1px solid var(--ring); border-radius:12px; padding:20px 20px 12px; }
  .card h4 { font-size:14.5px; font-weight:600; }
  .card .sub { font-size:12.5px; color:var(--ink-3); margin:2px 0 10px; }
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  @media (max-width:860px){ .grid2{grid-template-columns:1fr;} .intro{grid-template-columns:1fr;} }

  /* ---------- KPI ---------- */
  .kpis { display:grid; grid-template-columns:repeat(7,1fr); gap:16px; margin-top:28px; }
  @media (max-width:1020px){ .kpis{grid-template-columns:repeat(2,1fr);} .tile.hero{grid-column:span 2;} }
  @media (max-width:560px){ .kpis{grid-template-columns:1fr;} .tile.hero{grid-column:span 1;} }
  .tile { background:var(--surface-1); border:1px solid var(--ring); border-radius:12px; padding:16px; }
  .tile .lb { font-size:12.5px; color:var(--ink-3); }
  .tile .v { font-size:26px; font-weight:600; margin:4px 0 2px; }
  .tile.hero .v { font-size:48px; line-height:1.15; }
  .tile.hero { grid-column:span 2; }
  .tile .d { font-size:12.5px; color:var(--ink-3); }
  .tile .d .up { color:var(--good); font-weight:600; }
  .tile svg { display:block; margin-top:8px; }

  /* ---------- 图例 / 表格 / 脚注 ---------- */
  .legend { display:flex; gap:16px; flex-wrap:wrap; font-size:12.5px; color:var(--ink-2); margin:2px 0 4px; }
  .legend .li { display:flex; align-items:center; gap:6px; }
  .legend .sw { width:10px; height:10px; border-radius:3px; }
  .legend .ln { width:14px; height:2px; border-radius:1px; }
  details.tbl { margin:6px 0 10px; border-top:1px solid var(--grid); padding-top:8px; }
  details.tbl summary { font-size:12.5px; color:var(--ink-3); cursor:pointer; }
  details.tbl summary:hover { color:var(--ink-2); }
  .tblwrap { max-height:260px; overflow:auto; margin-top:8px; border:1px solid var(--grid); border-radius:8px; }
  table { border-collapse:collapse; width:100%; font-size:12.5px; }
  th,td { text-align:right; padding:5px 10px; white-space:nowrap; font-variant-numeric:tabular-nums; }
  th:first-child, td:first-child { text-align:left; }
  thead th { position:sticky; top:0; background:var(--surface-1); color:var(--ink-2); font-weight:600;
    border-bottom:1px solid var(--grid); }
  tbody tr + tr td { border-top:1px solid var(--grid); }
  .foot { margin-top:56px; border-top:1px solid var(--ring); padding-top:20px;
    color:var(--ink-2); font-size:13.5px; max-width:860px; }
  .foot h4 { color:var(--ink-1); font-size:14px; margin-bottom:6px; }
  .foot .fine { color:var(--ink-3); font-size:12.5px; margin-top:14px; }

  /* ---------- 提示框 ---------- */
  .tip { position:fixed; z-index:50; pointer-events:none; background:var(--tooltip-bg);
    border:1px solid var(--tooltip-ring); border-radius:9px; padding:9px 12px;
    font-size:12.5px; color:var(--ink-2); box-shadow:0 4px 16px rgba(0,0,0,.10);
    opacity:0; transition:opacity .12s; max-width:260px; }
  .tip .t { color:var(--ink-3); font-size:11.5px; margin-bottom:4px; }
  .tip .r { display:flex; align-items:center; gap:7px; margin-top:2px; }
  .tip .k { width:12px; height:2px; border-radius:1px; flex:none; }
  .tip .v { color:var(--ink-1); font-weight:600; }
</style>
</head>
<body>
<div class="wrap">

  <header class="hero">
    <p class="kicker">数据产品作品集</p>
    <h1>订阅业务收入成本监控看板</h1>
    <p class="herosub">某海外 AI 创作平台 · 订阅会员与积分购买双轨商业化 · 数据产品经理独立建设</p>

    <div class="intro">
      <div><h3>业务背景</h3>
        <p>平台以积分制售卖 AI 功能用量，收入在订单系统，成本散落在模型调用、渲染、创作者分成等环节。订阅业务上线前，没有一张报表能回答「每条业务赚不赚钱」。</p></div>
      <div><h3>我的角色</h3>
        <p>独立完成从成本核算方法、数仓建模到看板交付的全链路，并建立逐笔对账与校验发布机制。</p></div>
      <div><h3>方法要点</h3>
        <ul>
          <li>模型调用、渲染、创作者分成等成本，按购买、订阅、赠送三类积分的实际用量比例分摊</li>
          <li>单位积分成本可拆解到具体模型，异常波动当日可定位</li>
          <li>数据校验未通过的日期不发布成本数据；报表与订单流水逐笔核对</li>
        </ul></div>
    </div>
    <div class="disclaimer"><span>⚠</span><span><b>数据说明：</b>本页为仿真数据。曲线形状参考真实业务趋势，数值已缩放与扰动，不对应任何真实经营数字，仅用于展示分析方法与看板设计。</span></div>
  </header>

  <div class="navbar"><div class="row">
    <a href="#revenue">收入概览</a><a href="#subroi">订阅 ROI</a><a href="#purchroi">购买 ROI</a><a href="#cost">购买成本</a>
    <span class="spacer"></span>
    <div class="seg" role="group" aria-label="时间范围">
      <button data-win="all" aria-pressed="true">全部窗口</button>
      <button data-win="30" aria-pressed="false">近 30 天</button>
      <button data-win="launch" aria-pressed="false">订阅上线以来</button>
    </div>
    <button class="iconbtn" id="themeBtn" title="切换深浅色">◐</button>
  </div></div>

  <div class="kpis" id="kpis"></div>

  <section id="revenue">
    <div class="sec-head"><span class="sec-no">01</span><h2>收入概览</h2></div>
    <p class="sec-note">订阅业务上线首日即有日级收入追踪：每日净收入与每日新增付费会员。竖线标注为订阅上线日。</p>
    <div class="grid2">
      <div class="card"><h4>每日净收入</h4><p class="sub">订单流水核算 · 仿真口径：美元</p><div id="c_rev"></div><details class="tbl" id="t_rev"></details></div>
      <div class="card"><h4>每日新增付费会员</h4><p class="sub">会员系统 · 去重人数</p><div id="c_mem"></div><details class="tbl" id="t_mem"></details></div>
    </div>
  </section>

  <section id="subroi">
    <div class="sec-head"><span class="sec-no">02</span><h2>订阅 ROI</h2></div>
    <p class="sec-note">订阅收入指数与订阅分摊成本指数（区间首日 = 100）。收入增长远快于成本增长，是订阅毛利结构的直观证据；收入成本比见指标卡。</p>
    <div class="card"><h4>订阅收入指数 vs 订阅分摊成本指数</h4><p class="sub">同轴双指数线，避免双轴误读</p><div id="c_subroi"></div><details class="tbl" id="t_subroi"></details></div>
  </section>

  <section id="purchroi">
    <div class="sec-head"><span class="sec-no">03</span><h2>购买 ROI</h2></div>
    <p class="sec-note">购买积分的消耗等效金额指数与分摊成本指数（区间首日 = 100）。两条线的距离即购买业务的毛利空间。</p>
    <div class="card"><h4>购买消耗等效金额指数 vs 购买分摊成本指数</h4><p class="sub">等效金额按积分面值折算，非现金收入</p><div id="c_proi"></div><details class="tbl" id="t_proi"></details></div>
  </section>

  <section id="cost">
    <div class="sec-head"><span class="sec-no">04</span><h2>购买成本</h2></div>
    <p class="sec-note">左图：每 100 积分分摊成本的指数走势（区间首日 = 100），用于监控定价与成本的匹配度。右图：购买、订阅、赠送三桶的周度消耗构成——分摊比例的来源。</p>
    <div class="grid2">
      <div class="card"><h4>单位积分成本指数</h4><p class="sub">每 100 积分分摊成本 · 区间首日 = 100</p><div id="c_unit"></div><details class="tbl" id="t_unit"></details></div>
      <div class="card"><h4>三桶积分消耗构成（周度）</h4><p class="sub">成本按各桶消耗占比分摊的依据</p><div id="c_bucket"></div><details class="tbl" id="t_bucket"></details></div>
    </div>
  </section>

  <footer class="foot">
    <h4>方法注记</h4>
    <p>每日已纳入成本（模型网关调用、3D 渲染、创作者分成）乘以各桶消耗占比得到分摊成本；跨日只求和。单位成本 = 区间分摊成本 ÷ 区间消耗，不做日均的简单平均。数据校验未通过的日期不发布成本指标；报表数字与订单流水逐笔核对。</p>
    <p class="fine">本页数据为仿真数据，仅用于作品展示 · 图表与代码可复现 · 生成器与数据形状见仓库</p>
  </footer>
</div>

<script>
const DATA = __DATA__;
const C = { s1:'var(--s1)', s2:'var(--s2)', s3:'var(--s3)', ink3:'var(--ink-3)',
            grid:'var(--grid)', axis:'var(--axis)', surface:'var(--surface-1)' };

/* ---------- 工具 ---------- */
const $ = s => document.querySelector(s);
const el = (t, a) => { const n = document.createElementNS('http://www.w3.org/2000/svg', t);
  for (const k in a) n.setAttribute(k, a[k]); return n; };
const div = c => { const n = document.createElement('div'); if (c) n.className = c; return n; };
const money = v => '$' + Math.round(v).toLocaleString('en-US');
const wan = v => v >= 100 ? Math.round(v).toLocaleString('en-US') : v.toFixed(1);
const intc = v => Math.round(v).toLocaleString('en-US');
const md = d => d.slice(5).replace('-', '/');

function niceTicks(max, n) {
  if (max <= 0) return [0, 1];
  const raw = max / n, p = Math.pow(10, Math.floor(Math.log10(raw))), r = raw / p;
  const step = (r <= 1 ? 1 : r <= 2 ? 2 : r <= 2.5 ? 2.5 : r <= 5 ? 5 : 10) * p;
  const top = Math.ceil(max / step) * step, out = [];
  for (let v = 0; v <= top + 1e-9; v += step) out.push(v);
  return out;
}

/* 提示框（全局唯一） */
const tip = div('tip'); document.body.appendChild(tip);
function tipShow(node, x, y) {
  tip.textContent = ''; tip.append(node); tip.style.opacity = 1;
  const r = tip.getBoundingClientRect();
  let L = x + 14; if (L + r.width > innerWidth - 8) L = x - r.width - 14;
  tip.style.left = Math.max(8, L) + 'px';
  tip.style.top = Math.min(innerHeight - r.height - 8, Math.max(8, y + 12)) + 'px';
}
function tipRow(color, value, name) {
  const r = div('r'), k = div(); k.className = 'k'; k.style.background = color;
  const v = document.createElement('span'); v.className = 'v'; v.textContent = value;
  const s = document.createElement('span'); s.textContent = name;
  r.append(k, v, s); return r;
}
function tipHide() { tip.style.opacity = 0; }
function tipDate(d) { const t = document.createElement('div'); t.className = 't'; t.textContent = d; return t; }
function legendRow(items) {
  const lg = div('legend');
  items.forEach(it => {
    const li = div('li'), k = div(); k.className = it.rect ? 'sw' : 'ln'; k.style.background = it.color;
    const s = document.createElement('span'); s.textContent = it.name;
    li.append(k, s); lg.append(li);
  });
  return lg;
}

/* ---------- 折线图（支持多序列 / 面积 / 竖线标注 / 十字线悬浮） ---------- */
function lineChart(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const W = box.clientWidth || 480, H = cfg.h || 260, m = { t: 14, r: 58, b: 26, l: 46 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const n = cfg.dates.length;
  const all = cfg.series.flatMap(s => s.values);
  const ticks = niceTicks(Math.max(...all), 4);
  const yMax = ticks[ticks.length - 1];
  const X = i => m.l + (n === 1 ? iw / 2 : i * iw / (n - 1));
  const Y = v => m.t + ih - v / yMax * ih;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block' });

  ticks.forEach(v => {
    svg.append(el('line', { x1: m.l, x2: m.l + iw, y1: Y(v), y2: Y(v), stroke: v === 0 ? C.axis : C.grid, 'stroke-width': 1 }));
    const t = el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 11, fill: C.ink3 });
    t.textContent = cfg.tickFmt ? cfg.tickFmt(v) : v; svg.append(t);
  });
  const nt = Math.min(6, n);
  for (let k = 0; k < nt; k++) {
    const i = Math.round(k * (n - 1) / (nt - 1 || 1));
    const t = el('text', { x: X(i), y: H - 8, 'text-anchor': 'middle', 'font-size': 11, fill: C.ink3 });
    t.textContent = md(cfg.dates[i]); svg.append(t);
  }

  (cfg.notes || []).forEach(nt2 => {
    const i = cfg.dates.indexOf(nt2.d); if (i < 0) return;
    svg.append(el('line', { x1: X(i), x2: X(i), y1: m.t, y2: m.t + ih, stroke: C.axis, 'stroke-width': 1 }));
    const t = el('text', { x: X(i) + 5, y: m.t + 12, 'font-size': 11, fill: C.ink3 });
    t.textContent = nt2.label; svg.append(t);
  });

  cfg.series.forEach((s, si) => {
    const pts = s.values.map((v, i) => [X(i), Y(v)]);
    if (cfg.area && si === 0) {
      const d = [`M ${pts[0][0]} ${Y(0)}`].concat(pts.map(p => `L ${p[0]} ${p[1]}`),
        [`L ${pts[pts.length - 1][0]} ${Y(0)}`, 'Z']).join(' ');
      svg.append(el('path', { d, fill: s.color, opacity: .10 }));
    }
    svg.append(el('path', { d: pts.map((p, i) => (i ? 'L' : 'M') + ` ${p[0]} ${p[1]}`).join(' '),
      fill: 'none', stroke: s.color, 'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }));
    const last = pts[pts.length - 1];
    svg.append(el('circle', { cx: last[0], cy: last[1], r: 4, fill: s.color, stroke: C.surface, 'stroke-width': 2 }));
    const t = el('text', { x: last[0] + 8, y: last[1] + 4, 'font-size': 11, fill: 'var(--ink-2)', 'font-weight': 600 });
    t.textContent = cfg.endFmt ? cfg.endFmt(s.values[s.values.length - 1]) : Math.round(s.values[s.values.length - 1]);
    svg.append(t);
  });

  const cross = el('line', { y1: m.t, y2: m.t + ih, stroke: C.axis, 'stroke-width': 1, visibility: 'hidden' });
  svg.append(cross);
  const hit = el('rect', { x: m.l, y: m.t, width: iw, height: ih, fill: 'transparent' });
  hit.style.cursor = 'crosshair'; hit.tabIndex = 0;
  hit.setAttribute('role', 'img'); hit.setAttribute('aria-label', cfg.name || '折线图');
  svg.append(hit); box.append(svg);

  if (cfg.series.length >= 2) box.append(legendRow(cfg.series.map(s => ({ name: s.name, color: s.color }))));
  box.append(svg);

  let idx = n - 1;
  function show(i, cx, cy) {
    idx = i;
    cross.setAttribute('x1', X(i)); cross.setAttribute('x2', X(i));
    cross.setAttribute('visibility', 'visible');
    const tt = tipDate(cfg.dates[i]);
    cfg.series.forEach(s => tt.append(tipRow(s.color, (cfg.tipFmt || (v => Math.round(v)))(s.values[i]), s.name)));
    tipShow(tt, cx, cy);
  }
  hit.addEventListener('pointermove', e => {
    const r = svg.getBoundingClientRect(), sx = (e.clientX - r.left) * W / r.width;
    const i = Math.max(0, Math.min(n - 1, Math.round((sx - m.l) / (iw / (n - 1 || 1)))));
    show(i, e.clientX, e.clientY);
  });
  hit.addEventListener('pointerleave', () => { cross.setAttribute('visibility', 'hidden'); tipHide(); });
  hit.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') { show(Math.max(0, idx - 1), innerWidth / 2, 120); e.preventDefault(); }
    if (e.key === 'ArrowRight') { show(Math.min(n - 1, idx + 1), innerWidth / 2, 120); e.preventDefault(); }
    if (e.key === 'Escape') { cross.setAttribute('visibility', 'hidden'); tipHide(); }
  });
  addTable(sel.replace('#c_', '#t_'), cfg.dates, cfg.series, cfg.tipFmt, cfg.head || '');
}

/* ---------- 柱状图（单序列，逐柱悬浮） ---------- */
function colChart(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const W = box.clientWidth || 480, H = cfg.h || 260, m = { t: 14, r: 12, b: 26, l: 46 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b, n = cfg.values.length;
  const ticks = niceTicks(Math.max(...cfg.values), 4);
  const yMax = ticks[ticks.length - 1];
  const Y = v => m.t + ih - v / yMax * ih;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block' });
  ticks.forEach(v => {
    svg.append(el('line', { x1: m.l, x2: m.l + iw, y1: Y(v), y2: Y(v), stroke: v === 0 ? C.axis : C.grid, 'stroke-width': 1 }));
    const t = el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 11, fill: C.ink3 });
    t.textContent = cfg.tickFmt ? cfg.tickFmt(v) : v; svg.append(t);
  });
  const slot = iw / n, bw = Math.min(24, slot * 0.62);
  const nt = Math.min(6, n);
  for (let k = 0; k < nt; k++) {
    const i = Math.round(k * (n - 1) / (nt - 1 || 1));
    const t = el('text', { x: m.l + slot * i + slot / 2, y: H - 8, 'text-anchor': 'middle', 'font-size': 11, fill: C.ink3 });
    t.textContent = md(cfg.dates[i]); svg.append(t);
  }
  cfg.values.forEach((v, i) => {
    if (v <= 0) return;
    const x = m.l + slot * i + (slot - bw) / 2, h = Math.max(1, Y(0) - Y(v)), r = Math.min(4, h / 2);
    svg.append(el('path', { fill: cfg.color, opacity: 1,
      d: `M ${x} ${Y(0)} V ${Y(v) + r} Q ${x} ${Y(v)} ${x + r} ${Y(v)} H ${x + bw - r} Q ${x + bw} ${Y(v)} ${x + bw} ${Y(v) + r} V ${Y(0)} Z` }));
  });
  cfg.dates.forEach((d, i) => {
    const x = m.l + slot * i;
    const hit = el('rect', { x, y: m.t, width: Math.max(24, slot), height: ih, fill: 'transparent' });
    hit.addEventListener('pointermove', e => {
      const tt = tipDate(d); tt.append(tipRow(cfg.color, cfg.tipFmt(cfg.values[i]), cfg.name));
      tipShow(tt, e.clientX, e.clientY);
    });
    hit.addEventListener('pointerleave', tipHide);
    svg.append(hit);
  });
  box.append(svg);
  addTable(sel.replace('#c_', '#t_'), cfg.dates,
    [{ name: cfg.name, color: cfg.color, values: cfg.values }], cfg.tipFmt, cfg.head || '');
}

/* ---------- 堆叠柱（三桶周度构成） ---------- */
function stackChart(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const W = box.clientWidth || 480, H = cfg.h || 260, m = { t: 14, r: 12, b: 26, l: 46 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b, n = cfg.buckets.length;
  const totals = cfg.buckets.map(b => b.parts.reduce((a, p) => a + p.v, 0));
  const ticks = niceTicks(Math.max(...totals), 4);
  const yMax = ticks[ticks.length - 1];
  const Y = v => m.t + ih - v / yMax * ih;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block' });
  ticks.forEach(v => {
    svg.append(el('line', { x1: m.l, x2: m.l + iw, y1: Y(v), y2: Y(v), stroke: v === 0 ? C.axis : C.grid, 'stroke-width': 1 }));
    const t = el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 11, fill: C.ink3 });
    t.textContent = v; svg.append(t);
  });
  const slot = iw / n, bw = Math.min(24, slot * 0.62);
  cfg.buckets.forEach((b, i) => {
    const x = m.l + slot * i + (slot - bw) / 2; let acc = 0;
    b.parts.forEach(p => {
      const y1 = Y(acc), y0 = Y(acc + p.v), h = Math.max(1, y1 - y0 - 2), r = Math.min(4, h / 2);
      const top = acc + p.v === totals[i] ? y0 + r : y0; /* 顶端圆角只在最上段 */
      if (acc + p.v === totals[i]) {
        svg.append(el('path', { fill: p.color, d: `M ${x} ${y1} V ${top} Q ${x} ${y0} ${x + r} ${y0} H ${x + bw - r} Q ${x + bw} ${y0} ${x + bw} ${top} V ${y1} Z` }));
      } else {
        svg.append(el('rect', { x, y: y0 + 1, width: bw, height: Math.max(1, h), fill: p.color }));
      }
      acc += p.v;
    });
  });
  const nt = Math.min(6, n);
  for (let k = 0; k < nt; k++) {
    const i = Math.round(k * (n - 1) / (nt - 1 || 1));
    const t = el('text', { x: m.l + slot * i + slot / 2, y: H - 8, 'text-anchor': 'middle', 'font-size': 11, fill: C.ink3 });
    t.textContent = cfg.buckets[i].label; svg.append(t);
  }
  cfg.buckets.forEach((b, i) => {
    const x = m.l + slot * i;
    const hit = el('rect', { x, y: m.t, width: Math.max(24, slot), height: ih, fill: 'transparent' });
    hit.addEventListener('pointermove', e => {
      const tt = tipDate(b.full);
      b.parts.forEach(p => tt.append(tipRow(p.color, wan(p.v) + ' 万', p.name)));
      tt.append(tipRow('var(--ink-3)', wan(totals[i]) + ' 万', '合计'));
      tipShow(tt, e.clientX, e.clientY);
    });
    hit.addEventListener('pointerleave', tipHide);
    svg.append(hit);
  });
  const lg = div('legend');
  cfg.parts.forEach(p => {
    const li = div('li'), sw = div(); sw.className = 'sw'; sw.style.background = p.color;
    const s = document.createElement('span'); s.textContent = p.name;
    li.append(sw, s); lg.append(li);
  });
  box.append(lg, svg);
  addTableStack(sel.replace('#c_', '#t_'), cfg);
}

/* ---------- 表格孪生 ---------- */
function addTable(sel, dates, series, fmt, head) {
  const box = $(sel); if (!box) return; box.textContent = '';
  box.innerHTML = '';
  const d = document.createElement('details'), s = document.createElement('summary');
  s.textContent = '查看数据表'; d.append(s);
  const w = div('tblwrap'), t = document.createElement('table');
  const thead = document.createElement('thead'), trh = document.createElement('tr');
  const th0 = document.createElement('th'); th0.textContent = head || '日期'; trh.append(th0);
  series.forEach(sr => { const th = document.createElement('th'); th.textContent = sr.name; trh.append(th); });
  thead.append(trh); t.append(thead);
  const tb = document.createElement('tbody');
  dates.forEach((dd, i) => {
    const tr = document.createElement('tr');
    const td0 = document.createElement('td'); td0.textContent = dd; tr.append(td0);
    series.forEach(sr => { const td = document.createElement('td'); td.textContent = fmt ? fmt(sr.values[i]) : sr.values[i]; tr.append(td); });
    tb.append(tr);
  });
  t.append(tb); w.append(t); d.append(w); box.append(d);
}
function addTableStack(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const d = document.createElement('details'), s = document.createElement('summary');
  s.textContent = '查看数据表'; d.append(s);
  const w = div('tblwrap'), t = document.createElement('table');
  const thead = document.createElement('thead'), trh = document.createElement('tr');
  ['周', ...cfg.parts.map(p => p.name), '合计'].forEach(hh => {
    const th = document.createElement('th'); th.textContent = hh; trh.append(th); });
  thead.append(trh); t.append(thead);
  const tb = document.createElement('tbody');
  cfg.buckets.forEach(b => {
    const tr = document.createElement('tr');
    const td0 = document.createElement('td'); td0.textContent = b.full; tr.append(td0);
    b.parts.forEach(p => { const td = document.createElement('td'); td.textContent = wan(p.v); tr.append(td); });
    const tt = document.createElement('td'); tt.textContent = wan(b.parts.reduce((a, p) => a + p.v, 0)); tr.append(tt);
    tb.append(tr);
  });
  t.append(tb); w.append(t); d.append(w); box.append(d);
}

/* ---------- 迷你走势 ---------- */
function spark(vals, color) {
  const W = 120, H = 26, mn = Math.min(...vals), mx = Math.max(...vals);
  const X = i => 2 + i * (W - 4) / (vals.length - 1);
  const Y = v => 3 + (H - 6) * (1 - (v - mn) / ((mx - mn) || 1));
  const s = el('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H });
  s.append(el('path', { d: vals.map((v, i) => (i ? 'L' : 'M') + ` ${X(i)} ${Y(v)}`).join(' '),
    fill: 'none', stroke: 'var(--grid)', 'stroke-width': 2, 'stroke-linecap': 'round' }));
  s.append(el('circle', { cx: X(vals.length - 1), cy: Y(vals[vals.length - 1]), r: 4, fill: color, stroke: C.surface, 'stroke-width': 2 }));
  return s;
}

/* ---------- 窗口与渲染 ---------- */
let WIN = 'all';
const LAUNCH = DATA.launch;
function sliceDays(days, win) {
  if (win === 'all') return days;
  const last = days[days.length - 1].d;
  if (win === '30') {
    const cut = new Date(last); cut.setDate(cut.getDate() - 29);
    const cs = cut.toISOString().slice(0, 10);
    return days.filter(x => x.d >= cs);
  }
  return days.filter(x => x.d >= LAUNCH);
}
function idx(vals) { const b = vals.find(v => v > 0) || vals[0] || 1; return vals.map(v => v / b * 100); }

function renderKpis(cost, mem) {
  const box = $('#kpis'); box.textContent = '';
  const totRev = mem.reduce((a, m) => a + m.net_rev, 0);
  const totMem = mem.reduce((a, m) => a + m.members, 0);
  const totCr = cost.reduce((a, c) => a + c.p_cr + c.s_cr + c.g_cr, 0);
  const subCost = cost.reduce((a, c) => a + c.s_cost, 0);
  const pEq = cost.reduce((a, c) => a + c.p_cr * 100, 0);
  const pCost = cost.reduce((a, c) => a + c.p_cost, 0);
  const tiles = [
    { lb: '窗口累计净收入（仿真）', v: money(totRev), hero: true, spark: mem.map(m => m.net_rev), color: C.s1 },
    { lb: '新增付费会员', v: intc(totMem) + ' 名', spark: mem.map(m => m.members), color: C.s1,
      d: prevDelta(mem.map(m => m.members)) },
    { lb: '期末 MRR（仿真）', v: money(mem[mem.length - 1].mrr), spark: mem.map(m => m.mrr), color: C.s1 },
    { lb: '累计核算积分消耗', v: wan(totCr) + ' 万', spark: cost.map(c => c.p_cr + c.s_cr + c.g_cr), color: C.s1 },
    { lb: '订阅收入成本比', v: subCost ? (totRev / subCost).toFixed(1) + ' 倍' : '—',
      d: '订阅分摊成本 ' + money(subCost) },
    { lb: '购买收入成本比', v: pCost ? (pEq / pCost).toFixed(2) + ' 倍' : '—',
      d: '等效 ' + money(pEq) + ' / 成本 ' + money(pCost) },
  ];
  tiles.forEach(t => {
    const c = div('tile' + (t.hero ? ' hero' : ''));
    const lb = document.createElement('div'); lb.className = 'lb'; lb.textContent = t.lb; c.append(lb);
    const v = document.createElement('div'); v.className = 'v'; v.textContent = t.v; c.append(v);
    if (t.d !== undefined) {
      const dd = document.createElement('div'); dd.className = 'd';
      if (typeof t.d === 'string') dd.textContent = t.d;
      else { const u = document.createElement('span'); u.className = 'up'; u.textContent = t.d.txt; dd.append(u); }
      c.append(dd);
    }
    if (t.spark) c.append(spark(t.spark, t.color));
    box.append(c);
  });
  function prevDelta(a) {
    if (a.length < 8) return undefined;
    const prev = a.slice(-8, -1).reduce((x, y) => x + y, 0) / 7;
    const last = a[a.length - 1];
    const pct = Math.round((last / prev - 1) * 100);
    return { txt: `末日 ${last} 人，较前 7 日均值 ${pct >= 0 ? '+' : ''}${pct}%` };
  }
}

function renderAll() {
  const costAll = DATA.cost, memAll = DATA.mem;
  const cost = sliceDays(costAll, WIN);
  const mem = sliceDays(memAll, WIN);
  renderKpis(cost, mem);

  lineChart('#c_rev', { h: 250, dates: mem.map(m => m.d), name: '净收入',
    area: true, color: C.s1, tickFmt: v => v >= 1000 ? (v / 1000) + 'k' : v,
    tipFmt: v => money(v), endFmt: v => money(v), head: '日期',
    notes: WIN !== '30' ? [{ d: LAUNCH, label: '订阅上线' }] : [],
    series: [{ name: '净收入（仿真）', color: C.s1, values: mem.map(m => m.net_rev) }] });
  colChart('#c_mem', { h: 250, dates: mem.map(m => m.d), name: '新增会员',
    color: C.s1, tipFmt: v => intc(v) + ' 名', head: '日期',
    values: mem.map(m => m.members) });

  /* 订阅 ROI：仅取分摊成本开始产生的日期；两条线共用同一基准日（成本首日 = 100） */
  const subDays = cost.filter(c => c.d >= LAUNCH);
  const subRev = subDays.map(c => c.s_cost ? c2rev(costAll, c.d) : 0);
  const subCst = subDays.map(c => c.s_cost);
  const bi = subCst.findIndex(v => v > 0);
  const bR = (subRev[bi] || 1), bC = (subCst[bi] || 1);
  lineChart('#c_subroi', { h: 270, dates: subDays.map(c => c.d),
    tickFmt: v => v, tipFmt: v => v.toFixed(1), head: '日期',
    name: '订阅ROI指数',
    series: [
      { name: '订阅收入指数', color: C.s1, values: subRev.map(v => +(v / bR * 100).toFixed(1)) },
      { name: '订阅分摊成本指数', color: C.s2, values: subCst.map(v => +(v / bC * 100).toFixed(1)) },
    ] });

  lineChart('#c_proi', { h: 270, dates: cost.map(c => c.d),
    tickFmt: v => v, tipFmt: v => v.toFixed(1), head: '日期',
    name: '购买ROI指数',
    series: [
      { name: '购买消耗等效指数', color: C.s3, values: idx(cost.map(c => c.p_cr * 100)) },
      { name: '购买分摊成本指数', color: C.s2, values: idx(cost.map(c => c.p_cost)) },
    ] });

  lineChart('#c_unit', { h: 250, dates: cost.map(c => c.d), name: '单位成本指数',
    area: true, color: C.s1, tickFmt: v => v, tipFmt: v => v.toFixed(1), head: '日期',
    series: [{ name: '单位积分成本指数', color: C.s1, values: idx(cost.map(c => c.unit_idx)) }] });

  /* 三桶周度 */
  const buckets = [];
  for (let i = 0; i < cost.length; i += 7) {
    const g = cost.slice(i, i + 7);
    buckets.push({ full: g[0].d + ' 周', label: md(g[0].d),
      parts: [
        { name: '购买', color: C.s1, v: g.reduce((a, c) => a + c.p_cr, 0) },
        { name: '订阅', color: C.s2, v: g.reduce((a, c) => a + c.s_cr, 0) },
        { name: '赠送', color: C.s3, v: g.reduce((a, c) => a + c.g_cr, 0) },
      ] });
  }
  stackChart('#c_bucket', { buckets, parts: [
    { name: '购买', color: C.s1 }, { name: '订阅', color: C.s2 }, { name: '赠送', color: C.s3 }] });
}
function c2rev(costAll, d) {
  return DATA.mem.find(m => m.d === d)?.net_rev || 0;
}

/* ---------- 筛选与主题 ---------- */
document.querySelectorAll('.seg button').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('.seg button').forEach(x => x.setAttribute('aria-pressed', 'false'));
    b.setAttribute('aria-pressed', 'true');
    WIN = b.dataset.win; renderAll();
  });
});
const themeBtn = $('#themeBtn');
const saved = localStorage.getItem('pf-theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);
themeBtn.addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme');
  const dark = cur === 'dark' || (!cur && matchMedia('(prefers-color-scheme: dark)').matches);
  const next = dark ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('pf-theme', next);
  renderAll();
});
let rT; addEventListener('resize', () => { clearTimeout(rT); rT = setTimeout(renderAll, 150); });
renderAll();
</script>
</body>
</html>
"""

out = os.path.join(HERE, "index.html")
html = HTML.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
with io.open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("written:", out, len(html), "chars")
