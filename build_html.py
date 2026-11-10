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
  /* v4：深色为默认主题；仅显式 data-theme="light" 才回浅色 */
  :root {
    color-scheme: dark;
    --surface-1:#1a1a19; --page:#0d0d0d;
    --ink-1:#ffffff; --ink-2:#c3c2b7; --ink-3:#98968f;
    --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.10);
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s5:#d55181;
    --good:#0ca30c;
    --tooltip-bg:#242423; --tooltip-ring:rgba(255,255,255,.16);
  }
  :root[data-theme="light"] {
    color-scheme: light;
    --surface-1:#fcfcfb; --page:#f9f9f7;
    --ink-1:#0b0b0b; --ink-2:#52514e; --ink-3:#898781;
    --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,.10);
    --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s5:#e87ba4;
    --good:#006300;
    --tooltip-bg:#ffffff; --tooltip-ring:rgba(11,11,11,.14);
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
  .kicker::before { content:""; display:inline-block; width:9px; height:9px; border-radius:2px;
    margin-right:9px; vertical-align:-1px; background:linear-gradient(135deg,var(--s1),var(--s3)); }
  h1 { font-size:38px; font-weight:700; letter-spacing:.01em; margin:10px 0 6px; }
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
  section { margin-top:84px; }
  .sec-head { display:flex; align-items:baseline; gap:12px; margin-bottom:6px; }
  .sec-no { font-size:13px; color:var(--ink-3); font-weight:600; letter-spacing:.1em; }
  h2 { font-size:25px; font-weight:700; letter-spacing:.01em; }
  .sec-note { color:var(--ink-2); font-size:14px; margin-bottom:18px; max-width:820px; }
  .card { background:var(--surface-1); border:1px solid var(--ring); border-radius:12px; padding:20px 20px 12px; }
  .card h4 { font-size:16px; font-weight:650; letter-spacing:.01em; }
  .card .sub { font-size:13px; color:var(--ink-3); margin:3px 0 12px; }
  .grid2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  @media (max-width:860px){ .grid2{grid-template-columns:1fr;} .intro{grid-template-columns:1fr;} }

  /* ---------- KPI ---------- */
  .kpis { display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); gap:14px; margin-top:28px; }
  @media (max-width:1020px){ .kpis{grid-template-columns:repeat(2,1fr);} .tile.khero{grid-column:span 2;} }
  @media (max-width:560px){ .kpis{grid-template-columns:1fr;} .tile.khero{grid-column:span 1;} }
  .tile { background:var(--surface-1); border:1px solid var(--ring); border-radius:12px; padding:14px; }
  .tile .lb { font-size:12px; color:var(--ink-3); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .tile .v { font-size:24px; font-weight:650; margin:4px 0 2px; white-space:nowrap; overflow:hidden; font-variant-numeric:tabular-nums; letter-spacing:-.01em; }
  .tile.khero .v { font-size:32px; line-height:1.15; }
  .tile.khero { grid-column:span 2; }
  .tile .d { font-size:12px; color:var(--ink-3); min-height:18px;
    overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .tile .d .up { color:var(--good); font-weight:600; }
  .tile svg { display:block; margin-top:12px; width:100%; height:38px; }

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

  /* ---------- 阅读进度条 ---------- */
  #prog { position:fixed; top:0; left:0; height:2px; width:0; z-index:60;
    background:linear-gradient(90deg,var(--s1),var(--s3)); transition:width .08s linear; }

  /* ---------- 左侧章节导航（宽屏） ---------- */
  .rail { position:fixed; left:max(12px,calc(50% - 632px)); top:50%; transform:translateY(-50%);
    display:flex; flex-direction:column; gap:16px; z-index:25; }
  .rail a { display:flex; align-items:center; gap:9px; color:var(--ink-3); text-decoration:none;
    font-size:12px; height:18px; }
  .rail a::before { content:""; width:6px; height:6px; border-radius:50%; background:var(--axis);
    flex:none; transition:all .25s; }
  .rail a span { opacity:0; transform:translateX(-4px); transition:all .2s; }
  .rail a.active { color:var(--ink-1); font-weight:600; }
  .rail a.active::before { background:var(--s1); transform:scale(1.35); }
  .rail a.active span, .rail:hover a span { opacity:1; transform:none; }
  @media (max-width:1340px){ .rail { display:none; } }

  /* ---------- 滚动渐显 ---------- */
  .rv { opacity:0; transform:translateY(16px);
    transition:opacity .55s ease, transform .55s cubic-bezier(.22,1,.36,1); }
  .rv.on { opacity:1; transform:none; }
  @media (prefers-reduced-motion: reduce) { .rv { opacity:1; transform:none; transition:none; } }

  /* ---------- 数据质量条 ---------- */
  .qstrip { display:flex; gap:3px; margin:10px 0 6px; }
  .qc { flex:1; max-width:26px; aspect-ratio:1; border-radius:3px; cursor:pointer; }
  .qc:hover { transform:scale(1.18); }
  .qc:focus-visible { outline:2px solid var(--s1); outline-offset:1px; }
  .qends { display:flex; justify-content:space-between; font-size:11.5px; color:var(--ink-3); }
  .qnote { font-size:12.5px; color:var(--ink-2); margin-top:12px;
    border-top:1px solid var(--grid); padding-top:12px; }

  /* ---------- 钻取与冲积图 ---------- */
  .dhead { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
  .whint { color:var(--s1); font-weight:600; }
  .sx { overflow-x:auto; margin-top:4px; }
  .sx svg { min-width:760px; display:block; }
  .navbar a.active { color:var(--ink-1); font-weight:600; box-shadow:inset 0 -2px var(--s1); }

  /* ================= v2/v4 科技感层 ================= */
  :root {
    --glass:rgba(26,26,25,.58); --glass-bd:rgba(255,255,255,.10);
    --glow:rgba(57,135,229,.22); --glow2:rgba(25,158,112,.16); --gridline:rgba(255,255,255,.06);
    --lift:rgba(0,0,0,.55); --edge:rgba(255,255,255,.09);
  }
  :root[data-theme="light"] {
    --glass:rgba(252,252,251,.72); --glass-bd:rgba(11,11,11,.12);
    --glow:rgba(42,120,214,.16); --glow2:rgba(27,175,122,.13); --gridline:rgba(11,11,11,.045);
    --lift:rgba(11,11,11,.38); --edge:rgba(255,255,255,.65);
  }

  /* 页面底纹：双色微光 + 渐隐网格（仅装饰，无障碍不可见） */
  body::before { content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
    background-image:
      radial-gradient(720px 420px at 12% -6%, var(--glow), transparent 70%),
      radial-gradient(680px 460px at 96% 2%, var(--glow2), transparent 72%),
      linear-gradient(var(--gridline) 1px, transparent 1px),
      linear-gradient(90deg, var(--gridline) 1px, transparent 1px);
    background-size:auto,auto,44px 44px,44px 44px;
    -webkit-mask-image:radial-gradient(1300px 900px at 50% 0%, #000 0%, transparent 78%);
    mask-image:radial-gradient(1300px 900px at 50% 0%, #000 0%, transparent 78%);
  }

  /* v4 玻璃卡片：去 1px 灰框观感 —— 极淡描边 + 顶缘渐变光线 + 海拔投影 */
  .card, .tile, .intro, .disclaimer, .seg, .iconbtn {
    background:var(--glass);
    -webkit-backdrop-filter:blur(14px) saturate(1.15); backdrop-filter:blur(14px) saturate(1.15);
    border-color:var(--glass-bd);
    box-shadow:0 10px 30px -24px var(--lift), inset 0 1px 0 var(--edge);
  }
  .card, .tile, .intro { position:relative; }
  .card::before, .tile::before, .intro::before { content:""; position:absolute; top:0;
    left:10%; right:10%; height:1px; border-radius:1px; pointer-events:none;
    background:linear-gradient(90deg, transparent, var(--s1) 30%, var(--s3) 70%, transparent);
    opacity:.42; }
  @supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))) {
    .card, .tile, .intro, .disclaimer, .seg, .iconbtn { background:var(--surface-1); }
  }

  /* v4 KPI hero 卡：渐变底 + 加强顶缘光线 + 渐变数值 */
  .tile.khero { background:linear-gradient(135deg, rgba(57,135,229,.17), rgba(25,158,112,.06) 58%, transparent);
    border-color:rgba(57,135,229,.34);
    box-shadow:0 14px 40px -22px var(--glow), inset 0 1px 0 var(--edge); }
  .tile.khero::before { opacity:1; left:5%; right:5%; height:2px; }
  @supports ((-webkit-background-clip:text) or (background-clip:text)) {
    .tile.khero .v { width:fit-content;
      background:linear-gradient(92deg, var(--ink-1) 0%, var(--s1) 58%, var(--s3) 100%);
      -webkit-background-clip:text; background-clip:text; color:transparent; }
  }

  /* 玻璃导航条 */
  .navbar { background:transparent; border-bottom-color:transparent; }
  .navbar .row { background:var(--glass); border:1px solid var(--glass-bd); border-radius:14px;
    padding:9px 14px; margin:0 0 4px;
    -webkit-backdrop-filter:blur(14px) saturate(1.15); backdrop-filter:blur(14px) saturate(1.15);
    box-shadow:0 12px 34px -24px var(--lift), inset 0 1px 0 var(--edge); }

  /* 头部：胶囊徽标 + 渐变大标题 */
  .hero { padding:84px 0 8px; }
  .kicker { display:inline-flex; align-items:center; gap:9px; font-size:12.5px; letter-spacing:.16em;
    color:var(--ink-2); font-weight:600; border:1px solid var(--glass-bd); background:var(--glass);
    padding:7px 15px; border-radius:999px; }
  .kicker::before { content:""; width:8px; height:8px; border-radius:50%; background:var(--s3);
    animation:pulse 2.6s ease-out infinite; }
  @keyframes pulse { 0% { box-shadow:0 0 0 0 var(--glow2); } 70% { box-shadow:0 0 0 10px transparent; } 100% { box-shadow:0 0 0 0 transparent; } }
  h1 { font-size:44px; letter-spacing:.005em; margin:18px 0 10px; line-height:1.2; }
  @supports ((-webkit-background-clip:text) or (background-clip:text)) {
    h1 { width:fit-content; background:linear-gradient(92deg, var(--ink-1) 0%, var(--s1) 55%, var(--s3) 100%);
      -webkit-background-clip:text; background-clip:text; color:transparent; }
  }
  .herosub { letter-spacing:.02em; }
  @media (prefers-reduced-motion: reduce) { .kicker::before { animation:none; } }

  /* 区块标题：编号章 + 渐隐细线 */
  .sec-head { align-items:center; }
  .sec-no { font-size:36px; font-weight:750; line-height:.9; letter-spacing:.03em; width:fit-content;
    color:var(--ink-2); opacity:.30; user-select:none; }
  .sec-head::after { content:""; flex:1; height:1px; margin-left:10px;
    background:linear-gradient(90deg, var(--grid), transparent); }

  /* KPI 卡片悬浮 */
  .tile { transition:transform .25s cubic-bezier(.22,1,.36,1), box-shadow .25s; }
  .tile:hover { transform:translateY(-3px);
    box-shadow:0 14px 32px -16px var(--glow), 0 0 0 1px var(--glass-bd); }
  @media (prefers-reduced-motion: reduce) { .tile { transition:none; } .tile:hover { transform:none; } }

  /* 钻取播放器 */
  .pctrl { display:flex; gap:6px; align-items:center; flex:none; }
  .pbtn { border:1px solid var(--glass-bd); background:var(--surface-1); color:var(--ink-2);
    border-radius:8px; font-size:12.5px; line-height:1; padding:7px 11px; cursor:pointer;
    transition:all .2s; font-variant-numeric:tabular-nums; }
  .pbtn:hover { color:var(--ink-1); border-color:var(--s1); box-shadow:0 0 0 1px var(--glow), 0 6px 16px -8px var(--glow); }
  .pbtn[aria-pressed="true"] { color:var(--ink-1); background:var(--glow); border-color:var(--s1); }
  .pbtn:focus-visible { outline:2px solid var(--s1); outline-offset:1px; }

  /* 图例可点击序列 */
  .legend .li[role="button"] { cursor:pointer; border-radius:6px; padding:2px 4px; margin:-2px -4px; transition:opacity .2s; }
  .legend .li[role="button"]:hover { color:var(--ink-1); background:var(--glow); }
  .legend .li[role="button"]:focus-visible { outline:2px solid var(--s1); outline-offset:1px; }

  /* 回到顶部 */
  #totop { position:fixed; right:22px; bottom:22px; z-index:40; width:42px; height:42px; border-radius:50%;
    border:1px solid var(--glass-bd); background:var(--glass); color:var(--ink-2); font-size:16px; cursor:pointer;
    -webkit-backdrop-filter:blur(14px); backdrop-filter:blur(14px);
    opacity:0; pointer-events:none; transform:translateY(8px); transition:all .3s; }
  #totop.on { opacity:1; pointer-events:auto; transform:none; }
  #totop:hover { color:var(--ink-1); box-shadow:0 10px 26px -10px var(--glow); }

  /* 细滚动条 */
  ::-webkit-scrollbar { width:10px; height:10px; }
  ::-webkit-scrollbar-thumb { background:var(--axis); border-radius:5px; border:2px solid var(--page); }
  ::-webkit-scrollbar-track { background:transparent; }
  ::-webkit-scrollbar-thumb:hover { background:var(--ink-3); }
</style>
</head>
<body>
<div id="prog"></div>
<nav class="rail" id="rail" aria-label="章节导航"></nav>
<button id="totop" title="回到顶部" aria-label="回到顶部">↑</button>
<div class="wrap">

  <header class="hero" id="top">
    <p class="kicker">数据产品作品集 · PORTFOLIO</p>
    <h1>订阅业务收入成本监控看板</h1>
    <p class="herosub">某海外 AI 创作平台 · 订阅会员与积分购买双轨商业化 · 数据产品经理独立建设</p>

    <div class="intro rv">
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
    <div class="disclaimer rv"><span>⚠</span><span><b>数据说明：</b>本页为仿真数据。曲线形状参考真实业务趋势，数值已缩放与扰动，不对应任何真实经营数字，仅用于展示分析方法与看板设计。</span></div>
  </header>

  <div class="navbar"><div class="row">
    <a href="#revenue">收入概览</a><a href="#subroi">双轨 ROI 对照</a><a href="#cost">购买成本</a><a href="#alloc">分摊与质量</a>
    <span class="spacer"></span>
    <div class="seg" role="group" aria-label="时间范围">
      <button data-win="all" aria-pressed="true">全部窗口</button>
      <button data-win="30" aria-pressed="false">近 30 天</button>
      <button data-win="launch" aria-pressed="false">订阅上线以来</button>
    </div>
    <button class="iconbtn" id="themeBtn" title="切换深浅色">◐</button>
  </div></div>

  <div class="kpis rv" id="kpis"></div>

  <section id="revenue" class="rv">
    <div class="sec-head"><span class="sec-no">01</span><h2>收入概览</h2></div>
    <p class="sec-note">订阅业务上线首日即有日级收入追踪：每日净收入与每日新增付费会员。竖线标注为订阅上线日。</p>
    <div class="grid2">
      <div class="card"><h4>每日净收入</h4><p class="sub">订单流水核算 · 仿真口径：美元</p><div id="c_rev"></div><details class="tbl" id="t_rev"></details></div>
      <div class="card"><h4>每日新增付费会员</h4><p class="sub">会员系统 · 去重人数</p><div id="c_mem"></div><details class="tbl" id="t_mem"></details></div>
    </div>
  </section>

  <section id="subroi" class="rv">
    <div class="sec-head"><span class="sec-no">02</span><h2>双轨 ROI 对照</h2></div>
    <p class="sec-note">订阅与购买两条业务线并排对照：各画一张「收入指数 vs 分摊成本指数」（各自区间首日 = 100），两图共用同一纵轴刻度与同一组图例。线与线的距离即毛利空间——订阅线收入增长远快于成本，购买线毛利空间较薄，同刻度并置让差距一眼可见。</p>
    <div id="roiLegend" class="legend" style="margin:0 0 14px" aria-label="双轨 ROI 共享图例，点击显示或隐藏序列"></div>
    <div class="grid2">
      <div class="card"><h4>订阅线 · 收入指数 vs 分摊成本指数</h4><p class="sub">同轴双指数线，避免双轴误读</p><div id="c_subroi"></div><details class="tbl" id="t_subroi"></details></div>
      <div class="card"><h4>购买线 · 等效金额指数 vs 分摊成本指数</h4><p class="sub">等效金额按积分面值折算，非现金收入</p><div id="c_proi"></div><details class="tbl" id="t_proi"></details></div>
    </div>
  </section>

  <section id="cost" class="rv">
    <div class="sec-head"><span class="sec-no">03</span><h2>购买成本</h2></div>
    <p class="sec-note">左图：每 100 积分分摊成本的指数走势（区间首日 = 100），用于监控定价与成本的匹配度。右图：购买、订阅、赠送三桶的周度消耗构成——分摊比例的来源。</p>
    <div class="grid2">
      <div class="card"><h4>单位积分成本指数</h4><p class="sub">每 100 积分分摊成本 · 区间首日 = 100</p><div id="c_unit"></div><details class="tbl" id="t_unit"></details></div>
      <div class="card"><h4>三桶积分消耗构成（周度）</h4><p class="sub">成本按各桶消耗占比分摊的依据</p><div id="c_bucket"></div><details class="tbl" id="t_bucket"></details></div>
    </div>
    <div class="card" style="margin-top:16px">
      <div class="dhead"><div><h4>单位成本构成钻取</h4>
        <p class="sub">点击上方「单位积分成本指数」任意日期，或用播放器逐日回放 · <span id="wdate" class="whint"></span></p></div>
        <div class="pctrl" role="group" aria-label="逐日播放器">
          <button class="pbtn" id="pPrev" title="前一日">◀</button>
          <button class="pbtn" id="pNext" title="后一日">▶</button>
          <button class="pbtn" id="pPlay" title="自动播放" aria-pressed="false">⏵ 播放</button>
        </div></div>
      <div id="c_wf"></div><details class="tbl" id="t_wf"></details>
    </div>
  </section>

  <section id="alloc" class="rv">
    <div class="sec-head"><span class="sec-no">04</span><h2>成本分摊与数据质量</h2></div>
    <p class="sec-note">成本从四类来源按各业务桶当日消耗占比分摊的全景流向——赠送积分无直接收入，其分摊成本为平台自担的增长投入。发布质量逐日留痕：校验未通过的日期不发布成本指标，看板上不留灰色地带。</p>
    <div class="card"><h4>成本来源 → 业务桶 · 分摊全景</h4><p class="sub">悬浮查看每条流量的金额与占比 · 金额为仿真口径</p><div id="c_sankey" class="sx"></div><details class="tbl" id="t_sankey"></details></div>
    <div class="card" style="margin-top:16px"><h4>逐日发布质量</h4><p class="sub">每个格子是一天 · 悬浮查看当日校验说明</p><div id="c_qual"></div><p class="qnote">复核与补发全量留痕：进入看板的每一个数字，都能回溯到当日的校验记录与订单核对明细。</p></div>
  </section>

  <footer class="foot rv">
    <h4>方法注记</h4>
    <p>每日已纳入成本（模型网关调用、3D 渲染、创作者分成）乘以各桶消耗占比得到分摊成本；跨日只求和。单位成本 = 区间分摊成本 ÷ 区间消耗，不做日均的简单平均。数据校验未通过的日期不发布成本指标；报表数字与订单流水逐笔核对。</p>
    <p class="fine">本页数据为仿真数据，仅用于作品展示 · 图表与代码可复现 · 生成器与数据形状见仓库<br>
    交互：深浅主题 · 时间窗口筛选 · 悬浮十字线读数 · 共享图例跨图显隐（双轨 ROI 两图联动） · 单位成本按日钻取与逐日播放 · 冲积分摊全景 · 每图数据表孪生 · 键盘 ←/→/Enter</p>
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

/* ---------- 全局状态与动效 ---------- */
let WIN = 'all', PICKD = null, ANIM = true;
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const HID = {};                 /* 图例显隐状态：{ 图表key: [序列是否隐藏] } */
let PLAY = null;                /* 钻取自动播放定时器 */
let CURCOST = null;             /* 当前窗口的成本切片（播放器用） */
let __unitSync = null;          /* 单位成本折线的选中标记同步器 */

function drawIn(p, delay) {
  const L = p.getTotalLength();
  p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
  p.getBoundingClientRect();
  p.style.transition = `stroke-dashoffset .9s ${delay || 0}ms cubic-bezier(.4,0,.2,1)`;
  requestAnimationFrame(() => { p.style.strokeDashoffset = '0'; });
  setTimeout(() => { p.style.strokeDasharray = 'none'; p.style.transition = ''; }, 1150 + (delay || 0));
}
function riseIn(nodes, delay) {
  nodes.forEach((n, i) => {
    n.style.transformBox = 'fill-box'; n.style.transformOrigin = '50% 100%';
    n.style.transform = 'scaleY(0.001)';
    n.style.transition = `transform .55s ${(delay || 0) + i * 14}ms cubic-bezier(.22,1,.36,1)`;
    requestAnimationFrame(() => requestAnimationFrame(() => { n.style.transform = 'scaleY(1)'; }));
  });
}
function cssVar(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
function hex2rgb(h) { h = h.replace('#', ''); if (h.length === 3) h = h.split('').map(c => c + c).join('');
  return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); }
function mixHex(a, b, t) { const A = hex2rgb(a), B = hex2rgb(b);
  return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, '0')).join(''); }
function countUpVal(node) {
  if (RM) return;
  const orig = node.textContent;
  const m = orig.match(/[\d][\d,]*(\.\d+)?/); if (!m) return;
  const target = parseFloat(m[0].replace(/,/g, ''));
  const dec = (m[0].split('.')[1] || '').length;
  const pre = orig.slice(0, m.index), suf = orig.slice(m.index + m[0].length);
  const useComma = /,/.test(m[0]);
  const t0 = performance.now(), D = 900;
  function fr(t) {
    let p = Math.min(1, (t - t0) / D); p = 1 - Math.pow(1 - p, 3);
    const v = target * p;
    let s = dec ? v.toFixed(dec) : String(Math.round(v));
    if (useComma) s = Number(s).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
    node.textContent = pre + s + suf;
    if (p < 1) requestAnimationFrame(fr);
  }
  requestAnimationFrame(fr);
}

/* ---------- 折线图（支持多序列 / 面积 / 竖线标注 / 十字线悬浮） ---------- */
function lineChart(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const W = box.clientWidth || 480, H = cfg.h || 300, m = { t: 14, r: 58, b: 26, l: 46 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const n = cfg.dates.length;
  const vis = cfg.key ? (HID[cfg.key] || cfg.series.map(() => false)).map(Boolean)
                      : cfg.series.map(() => false);
  const all = cfg.series.flatMap((s, i) => vis[i] ? [] : s.values);
  const ticks = niceTicks(cfg.yMax != null ? cfg.yMax : Math.max(1, ...all, 0), 4);
  const yMax = ticks[ticks.length - 1];
  const X = i => m.l + (n === 1 ? iw / 2 : i * iw / (n - 1));
  const Y = v => m.t + ih - v / yMax * ih;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block' });

  ticks.forEach(v => {
    svg.append(el('line', { x1: m.l, x2: m.l + iw, y1: Y(v), y2: Y(v), stroke: v === 0 ? C.axis : C.grid, 'stroke-width': 1 }));
    const t = el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 12, fill: C.ink3 });
    t.textContent = cfg.tickFmt ? cfg.tickFmt(v) : v; svg.append(t);
  });
  const nt = Math.min(6, n);
  for (let k = 0; k < nt; k++) {
    const i = Math.round(k * (n - 1) / (nt - 1 || 1));
    const t = el('text', { x: X(i), y: H - 8, 'text-anchor': 'middle', 'font-size': 12, fill: C.ink3 });
    t.textContent = md(cfg.dates[i]); svg.append(t);
  }

  (cfg.notes || []).forEach(nt2 => {
    const i = cfg.dates.indexOf(nt2.d); if (i < 0) return;
    svg.append(el('line', { x1: X(i), x2: X(i), y1: m.t, y2: m.t + ih, stroke: C.axis, 'stroke-width': 1 }));
    const t = el('text', { x: X(i) + 5, y: m.t + 12, 'font-size': 11, fill: C.ink3 });
    t.textContent = nt2.label; svg.append(t);
  });

  const lps = [];
  const defs = el('defs', {});
  svg.append(defs);
  cfg.series.forEach((s, si) => {
    if (vis[si]) return;  /* 图例隐藏的序列不绘制；颜色跟随实体，不重涂幸存者 */
    const pts = s.values.map((v, i) => [X(i), Y(v)]);
    /* v4：面积用纵向渐变（color@.30 → 透明），线带同色微光 */
    const gid = `lg-${(cfg.key || sel.replace(/[^a-zA-Z0-9]/g, ''))}-${si}`;
    const grad = el('linearGradient', { id: gid, x1: 0, y1: 0, x2: 0, y2: 1 });
    grad.append(el('stop', { offset: '0%', 'stop-color': s.color, 'stop-opacity': .30 }));
    grad.append(el('stop', { offset: '100%', 'stop-color': s.color, 'stop-opacity': 0 }));
    defs.append(grad);
    if (cfg.area && si === 0) {
      const d = [`M ${pts[0][0]} ${Y(0)}`].concat(pts.map(p => `L ${p[0]} ${p[1]}`),
        [`L ${pts[pts.length - 1][0]} ${Y(0)}`, 'Z']).join(' ');
      svg.append(el('path', { d, fill: `url(#${gid})` }));
    }
    const lp = el('path', { d: pts.map((p, i) => (i ? 'L' : 'M') + ` ${p[0]} ${p[1]}`).join(' '),
      fill: 'none', stroke: s.color, 'stroke-width': 2.6, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
    lp.style.filter = `drop-shadow(0 1px 7px ${s.color}55)`;
    svg.append(lp); lps.push(lp);
    const last = pts[pts.length - 1];
    svg.append(el('circle', { cx: last[0], cy: last[1], r: 4.5, fill: s.color, stroke: C.surface, 'stroke-width': 2 }));
    const t = el('text', { x: last[0] + 8, y: last[1] + 4, 'font-size': 12, fill: 'var(--ink-2)', 'font-weight': 600 });
    t.textContent = cfg.endFmt ? cfg.endFmt(s.values[s.values.length - 1]) : Math.round(s.values[s.values.length - 1]);
    svg.append(t);
  });

  /* 选中标记（钻取联动；播放器可通过 __unitSync 平移它，不必整图重绘） */
  if (cfg.pick) {
    const pi = cfg.dates.indexOf(cfg.pick);
    const s0 = cfg.series.find((s, i) => !vis[i]) || cfg.series[0];
    if (pi >= 0) {
      const mg = el('g', {});
      const cx0 = X(pi), cy0 = Y(s0.values[pi]);
      mg.append(el('circle', { cx: 0, cy: 0, r: 7, fill: 'none', stroke: C.s2, 'stroke-width': 2 }));
      mg.append(el('circle', { cx: 0, cy: 0, r: 2.5, fill: C.s2 }));
      mg.setAttribute('transform', `translate(${cx0},${cy0})`);
      svg.append(mg);
      if (cfg.key === 'unit') {
        __unitSync = d => {
          const j = cfg.dates.indexOf(d);
          if (j >= 0) mg.setAttribute('transform', `translate(${X(j)},${Y(s0.values[j])})`);
        };
      }
    }
  }

  const cross = el('line', { y1: m.t, y2: m.t + ih, stroke: C.axis, 'stroke-width': 1, visibility: 'hidden' });
  svg.append(cross);
  const hit = el('rect', { x: m.l, y: m.t, width: iw, height: ih, fill: 'transparent' });
  hit.style.cursor = cfg.onPick ? 'pointer' : 'crosshair'; hit.tabIndex = 0;
  hit.setAttribute('role', 'img'); hit.setAttribute('aria-label', cfg.name || '折线图');
  svg.append(hit);

  if (cfg.series.length >= 2 && !cfg.noLegend) {
    const lg = div('legend');
    cfg.series.forEach((s, si) => {
      const li = div('li'); li.setAttribute('role', 'button'); li.tabIndex = 0;
      li.title = '点击显示 / 隐藏该序列';
      const k = div(); k.className = 'ln'; k.style.background = s.color;
      const sp = document.createElement('span'); sp.textContent = s.name;
      li.append(k, sp);
      if (vis[si]) { li.style.opacity = .38; sp.style.textDecoration = 'line-through'; }
      const tog = () => {
        const arr = HID[cfg.key] || (HID[cfg.key] = cfg.series.map(() => false));
        const nv = arr.map((v, i2) => i2 === si ? !v : v);
        if (nv.every(x => x)) return;  /* 不允许隐藏全部序列 */
        arr[si] = !arr[si];
        (cfg.rerender || (() => renderAll(false)))();
      };
      li.addEventListener('click', tog);
      li.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tog(); } });
      lg.append(li);
    });
    box.append(lg);
  }
  box.append(svg);
  if (ANIM && !RM) lps.forEach((p, i) => drawIn(p, 120 + i * 160));

  let idx = n - 1;
  function show(i, cx, cy) {
    idx = i;
    cross.setAttribute('x1', X(i)); cross.setAttribute('x2', X(i));
    cross.setAttribute('visibility', 'visible');
    const tt = tipDate(cfg.dates[i]);
    cfg.series.forEach((s, si) => {
      if (!vis[si]) return;
      tt.append(tipRow(s.color, (cfg.tipFmt || (v => Math.round(v)))(s.values[i]), s.name));
    });
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
    if (e.key === 'Enter' && cfg.onPick) cfg.onPick(cfg.dates[idx]);
  });
  if (cfg.onPick) hit.addEventListener('click', () => cfg.onPick(cfg.dates[idx]));
  addTable(sel.replace('#c_', '#t_'), cfg.dates, cfg.series, cfg.tipFmt, cfg.head || '');
}

/* ---------- 柱状图（单序列，逐柱悬浮） ---------- */
function colChart(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const W = box.clientWidth || 480, H = cfg.h || 300, m = { t: 14, r: 12, b: 26, l: 46 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b, n = cfg.values.length;
  const ticks = niceTicks(Math.max(...cfg.values), 4);
  const yMax = ticks[ticks.length - 1];
  const Y = v => m.t + ih - v / yMax * ih;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block' });
  ticks.forEach(v => {
    svg.append(el('line', { x1: m.l, x2: m.l + iw, y1: Y(v), y2: Y(v), stroke: v === 0 ? C.axis : C.grid, 'stroke-width': 1 }));
    const t = el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 12, fill: C.ink3 });
    t.textContent = cfg.tickFmt ? cfg.tickFmt(v) : v; svg.append(t);
  });
  const slot = iw / n, bw = Math.min(24, slot * 0.62);
  const nt = Math.min(6, n);
  for (let k = 0; k < nt; k++) {
    const i = Math.round(k * (n - 1) / (nt - 1 || 1));
    const t = el('text', { x: m.l + slot * i + slot / 2, y: H - 8, 'text-anchor': 'middle', 'font-size': 12, fill: C.ink3 });
    t.textContent = md(cfg.dates[i]); svg.append(t);
  }
  const bars = [];
  cfg.values.forEach((v, i) => {
    if (v <= 0) return;
    const x = m.l + slot * i + (slot - bw) / 2, h = Math.max(1, Y(0) - Y(v)), r = Math.min(4, h / 2);
    const bar = el('path', { fill: cfg.color, opacity: 1,
      d: `M ${x} ${Y(0)} V ${Y(v) + r} Q ${x} ${Y(v)} ${x + r} ${Y(v)} H ${x + bw - r} Q ${x + bw} ${Y(v)} ${x + bw} ${Y(v) + r} V ${Y(0)} Z` });
    svg.append(bar); bars.push(bar);
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
  if (ANIM && !RM) riseIn(bars, 60);
  addTable(sel.replace('#c_', '#t_'), cfg.dates,
    [{ name: cfg.name, color: cfg.color, values: cfg.values }], cfg.tipFmt, cfg.head || '');
}

/* ---------- 堆叠柱（三桶周度构成） ---------- */
function stackChart(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const W = box.clientWidth || 480, H = cfg.h || 300, m = { t: 14, r: 12, b: 26, l: 46 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b, n = cfg.buckets.length;
  const totals = cfg.buckets.map(b => b.parts.reduce((a, p) => a + p.v, 0));
  const ticks = niceTicks(Math.max(...totals), 4);
  const yMax = ticks[ticks.length - 1];
  const Y = v => m.t + ih - v / yMax * ih;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block' });
  ticks.forEach(v => {
    svg.append(el('line', { x1: m.l, x2: m.l + iw, y1: Y(v), y2: Y(v), stroke: v === 0 ? C.axis : C.grid, 'stroke-width': 1 }));
    const t = el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 12, fill: C.ink3 });
    t.textContent = v; svg.append(t);
  });
  const slot = iw / n, bw = Math.min(24, slot * 0.62);
  const segs = [];
  cfg.buckets.forEach((b, i) => {
    const x = m.l + slot * i + (slot - bw) / 2; let acc = 0;
    b.parts.forEach(p => {
      const y1 = Y(acc), y0 = Y(acc + p.v), h = Math.max(1, y1 - y0 - 2), r = Math.min(4, h / 2);
      const top = acc + p.v === totals[i] ? y0 + r : y0; /* 顶端圆角只在最上段 */
      let seg;
      if (acc + p.v === totals[i]) {
        seg = el('path', { fill: p.color, d: `M ${x} ${y1} V ${top} Q ${x} ${y0} ${x + r} ${y0} H ${x + bw - r} Q ${x + bw} ${y0} ${x + bw} ${top} V ${y1} Z` });
      } else {
        seg = el('rect', { x, y: y0 + 1, width: bw, height: Math.max(1, h), fill: p.color });
      }
      svg.append(seg); segs.push(seg);
      acc += p.v;
    });
  });
  const nt = Math.min(6, n);
  for (let k = 0; k < nt; k++) {
    const i = Math.round(k * (n - 1) / (nt - 1 || 1));
    const t = el('text', { x: m.l + slot * i + slot / 2, y: H - 8, 'text-anchor': 'middle', 'font-size': 12, fill: C.ink3 });
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
  if (ANIM && !RM) riseIn(segs, 60);
  addTableStack(sel.replace('#c_', '#t_'), cfg);
}

/* ---------- 冲积图（成本来源 → 业务桶分摊全景） ---------- */
function kf(v) { return v >= 1000 ? '$' + (v / 1000).toFixed(1) + 'k' : '$' + Math.round(v); }

function sankeyChart(sel, agg) {
  const box = $(sel); box.textContent = '';
  const W = 1000, H = 400, nw = 14, gap = 16, mT = 30, mB = 14, mL = 128, mR = 118;
  const { flows, src } = agg;
  const bktNames = agg.bktNames;
  const total = src.reduce((a, b) => a + b, 0);
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block',
    role: 'img', 'aria-label': '成本来源到业务桶的分摊冲积图' });

  /* 列布局：节点高 ∝ 金额，列内居中 */
  const k = Math.min((H - mT - mB - gap * (src.length - 1)) / total,
                     (H - mT - mB - gap * (bktNames.length - 1)) / total);
  const bktTot = bktNames.map(bn => flows.filter(f => f.b === bn).reduce((a, f) => a + f.v, 0));
  const yStart = nn => mT + (H - mT - mB - (total * k + (nn - 1) * gap)) / 2;
  const Lp = {}; let yy = yStart(src.length);
  DATA.src_names.forEach((s2, i) => { Lp[s2] = { x: mL, y: yy, h: Math.max(2, src[i] * k) }; yy += src[i] * k + gap; });
  const Rp = {}; yy = yStart(bktNames.length);
  bktNames.forEach((b2, i) => { Rp[b2] = { x: W - mR, y: yy, h: Math.max(2, bktTot[i] * k) }; yy += bktTot[i] * k + gap; });

  /* 深色主题下去饱和更少、缎带更实，避免小流量节点融进背景 */
  const dk = (() => { const c = hex2rgb(cssVar('--surface-1')); return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255 < 0.5; })();
  const MUTE = dk ? 0.22 : 0.45, ROP = dk ? 0.44 : 0.34;
  const SRC_COLS = ['--s1', '--s2', '--s3', '--s5'];  /* 调色板无 --s4，第四来源取粉色 */
  const muted = SRC_COLS.map(v => mixHex(cssVar(v), cssVar('--surface-1'), MUTE));
  const bktCol = [cssVar('--s1'), cssVar('--s2'), cssVar('--s3')];

  /* 渐变（来源色 → 桶色） */
  const defs = el('defs', {});
  flows.forEach((f, i) => {
    const g = el('linearGradient', { id: 'sk' + i, x1: 0, x2: 1, y1: 0, y2: 0 });
    g.append(el('stop', { offset: '0%', 'stop-color': muted[DATA.src_names.indexOf(f.s)] }));
    g.append(el('stop', { offset: '100%', 'stop-color': bktCol[bktNames.indexOf(f.b)] }));
    defs.append(g);
  });
  svg.append(defs);

  /* 缎带 */
  const offL = {}, offR = {};
  DATA.src_names.forEach(s2 => offL[s2] = Lp[s2].y);
  bktNames.forEach(b2 => offR[b2] = Rp[b2].y);
  const ribbons = [];
  flows.forEach((f, i) => {
    const h = Math.max(1, f.v * k);
    const y0 = offL[f.s], y1 = offR[f.b];
    offL[f.s] += h; offR[f.b] += h;
    const x0 = Lp[f.s].x + nw, x1 = Rp[f.b].x, mx = (x0 + x1) / 2;
    const p = el('path', { d: `M ${x0} ${y0} C ${mx} ${y0} ${mx} ${y1} ${x1} ${y1} L ${x1} ${y1 + h} C ${mx} ${y1 + h} ${mx} ${y0 + h} ${x0} ${y0 + h} Z`,
      fill: 'url(#sk' + i + ')', opacity: ROP });
    p.style.cursor = 'default';
    p.addEventListener('pointerenter', () => {
      ribbons.forEach(r2 => { if (r2 !== p) r2.style.opacity = .08; });
      p.style.opacity = .78;
    });
    p.addEventListener('pointermove', e => {
      const t = tipDate(f.s + ' → ' + f.b + '消耗');
      t.append(tipRow(bktCol[bktNames.indexOf(f.b)], money(f.v), '分摊金额（仿真）'));
      t.append(tipRow('var(--ink-3)', (f.v / total * 100).toFixed(1) + '%', '占窗口总成本'));
      tipShow(t, e.clientX, e.clientY);
    });
    p.addEventListener('pointerleave', () => {
      ribbons.forEach(r2 => { r2.style.opacity = ''; });
      tipHide();
    });
    svg.append(p); ribbons.push(p);
  });

  /* 节点与直标 */
  function nodeBlock(pos, name, val, color, side) {
    const g = el('g', {});
    const r = el('rect', { x: pos.x, y: pos.y, width: nw, height: pos.h, rx: 3, fill: color });
    r.addEventListener('pointerenter', () => ribbons.forEach(p2 => {
      const keep = flows.some(f => (f.s === name || f.b === name) && p2 === ribbons[flows.indexOf(f)]);
      if (!keep) p2.style.opacity = .08;
    }));
    r.addEventListener('pointerleave', () => ribbons.forEach(p2 => { p2.style.opacity = ''; }));
    const nm = el('text', { x: side === 'l' ? pos.x - 10 : pos.x + nw + 10, y: pos.y + pos.h / 2 - 3,
      'text-anchor': side === 'l' ? 'end' : 'start', 'font-size': 13, fill: 'var(--ink-1)', 'font-weight': 600 });
    nm.textContent = name;
    const vl = el('text', { x: side === 'l' ? pos.x - 10 : pos.x + nw + 10, y: pos.y + pos.h / 2 + 15,
      'text-anchor': side === 'l' ? 'end' : 'start', 'font-size': 11.5, fill: 'var(--ink-3)' });
    vl.textContent = kf(val) + ' · ' + (val / total * 100).toFixed(0) + '%';
    g.append(r, nm, vl); svg.append(g);
  }
  DATA.src_names.forEach((s2, i) => nodeBlock(Lp[s2], s2, src[i], muted[i], 'l'));
  bktNames.forEach((b2, i) => nodeBlock(Rp[b2], b2 + '消耗', bktTot[i], bktCol[i], 'r'));

  box.append(svg);
  if (ANIM && !RM) {
    svg.style.opacity = 0; svg.style.transition = 'opacity .8s ease';
    requestAnimationFrame(() => requestAnimationFrame(() => { svg.style.opacity = 1; }));
  }
  flowTable(sel.replace('#c_', '#t_'), flows, bktNames, total);
}

function flowTable(sel, flows, bktNames, total) {
  const box = $(sel); if (!box) return; box.textContent = '';
  const d = document.createElement('details'), s = document.createElement('summary');
  s.textContent = '查看分摊明细表'; d.append(s);
  const w = div('tblwrap'), t = document.createElement('table');
  const thead = document.createElement('thead'), trh = document.createElement('tr');
  ['成本来源', '业务桶', '分摊金额（仿真）', '占比'].forEach(hh => {
    const th = document.createElement('th'); th.textContent = hh; trh.append(th); });
  thead.append(trh); t.append(thead);
  const tb = document.createElement('tbody');
  flows.forEach(f => {
    const tr = document.createElement('tr');
    [[f.s], [f.b], [money(f.v)], [(f.v / total * 100).toFixed(1) + '%']].forEach(([v]) => {
      const td = document.createElement('td'); td.textContent = v; tr.append(td); });
    tb.append(tr);
  });
  t.append(tb); w.append(t); d.append(w); box.append(d);
}

/* ---------- 数据质量条（逐日发布状态） ---------- */
function qualityStrip(sel, arr) {
  const box = $(sel); box.textContent = '';
  const stC = { ok: 'var(--good)', review: 'var(--s2)', delay: 'var(--s5)' };
  const stN = { ok: '校验通过', review: '复核后补发', delay: '暂缓发布 · 次日补发' };
  const cnt = { ok: 0, review: 0, delay: 0 };
  const strip = div('qstrip');
  arr.forEach(q => {
    cnt[q.st]++;
    const c = div('qc'); c.style.background = stC[q.st]; c.tabIndex = 0;
    c.setAttribute('role', 'img');
    c.setAttribute('aria-label', q.d + ' ' + stN[q.st] + '：' + q.note);
    c.addEventListener('pointermove', e => {
      const t = tipDate(q.d);
      t.append(tipRow(stC[q.st], stN[q.st], q.note));
      tipShow(t, e.clientX, e.clientY);
    });
    c.addEventListener('pointerleave', tipHide);
    strip.append(c);
  });
  const lg = legendRow([
    { name: '校验通过 · 正常发布 ' + cnt.ok + ' 天', color: stC.ok, rect: true },
    { name: '复核后补发 ' + cnt.review + ' 天', color: stC.review, rect: true },
    { name: '暂缓发布 ' + cnt.delay + ' 天', color: stC.delay, rect: true }]);
  const ends = div('qends');
  const e1 = document.createElement('span'); e1.textContent = arr[0].d.slice(5).replace('-', '/');
  const e2 = document.createElement('span'); e2.textContent = '共 ' + arr.length + ' 天';
  const e3 = document.createElement('span'); e3.textContent = arr[arr.length - 1].d.slice(5).replace('-', '/');
  ends.append(e1, e2, e3);
  box.append(lg, strip, ends);
}

/* ---------- 瀑布图（单位成本按模型拆解） ---------- */
function waterfall(sel, cfg) {
  const box = $(sel); box.textContent = '';
  const W = box.clientWidth || 900, H = 240, m = { t: 26, r: 12, b: 40, l: 52 };
  const iw = W - m.l - m.r, ih = H - m.t - m.b;
  const items = cfg.parts.map(p => ({ name: p.name, v: p.v, total: false }))
    .concat([{ name: '当日合计', v: cfg.total, total: true }]);
  const n = items.length;
  const ticks = niceTicks(cfg.total, 4);
  const yMax = ticks[ticks.length - 1];
  const Y = v => m.t + ih - v / yMax * ih;
  const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'display:block',
    role: 'img', 'aria-label': '当日单位成本按模型拆解瀑布图' });
  ticks.forEach(v => {
    svg.append(el('line', { x1: m.l, x2: m.l + iw, y1: Y(v), y2: Y(v), stroke: C.grid, 'stroke-width': 1 }));
    const t = el('text', { x: m.l - 8, y: Y(v) + 4, 'text-anchor': 'end', 'font-size': 12, fill: C.ink3 });
    t.textContent = '$' + v.toFixed(1); svg.append(t);
  });
  const gapT = 26; /* 合计柱额外间距 */
  const slot = (iw - gapT) / n, bw = Math.min(64, slot * 0.58);
  const surf = cssVar('--surface-1'), c1 = cssVar('--s1');
  const ramp = t => mixHex(surf, c1, t);
  const bars = [];
  let cum = 0, prevRight = null, prevY = null;
  items.forEach((it, i) => {
    const x = m.l + slot * i + (slot - bw) / 2 + (it.total ? gapT : 0);
    const yTop = it.total ? Y(it.v) : Y(cum + it.v);
    const yBot = it.total ? Y(0) : Y(cum);
    const bar = el('rect', { x, y: yTop, width: bw, height: Math.max(2, yBot - yTop), rx: 3 });
    bar.style.fill = it.total ? 'var(--ink-1)' : ramp(0.42 + 0.58 * i / Math.max(1, cfg.parts.length - 1));
    svg.append(bar); bars.push(bar);
    if (prevRight !== null && !it.total) {
      svg.append(el('line', { x1: prevRight, x2: x, y1: prevY, y2: prevY,
        stroke: C.axis, 'stroke-width': 1, 'stroke-dasharray': '2 3' }));
    }
    if (!it.total) { cum += it.v; prevRight = x + bw; prevY = Y(cum); }
    const lbl = el('text', { x: x + bw / 2, y: yTop - 7, 'text-anchor': 'middle',
      'font-size': 11, fill: it.total ? 'var(--ink-1)' : 'var(--ink-2)',
      'font-weight': it.total ? 700 : 400 });
    lbl.textContent = '$' + it.v.toFixed(2); svg.append(lbl);
    const xt = el('text', { x: x + bw / 2, y: H - 10, 'text-anchor': 'middle', 'font-size': 11.5,
      fill: it.total ? 'var(--ink-1)' : 'var(--ink-3)', 'font-weight': it.total ? 600 : 400 });
    xt.textContent = it.name; svg.append(xt);
    const hit = el('rect', { x: m.l + slot * i + (it.total ? gapT : 0), y: m.t, width: slot, height: ih, fill: 'transparent' });
    hit.addEventListener('pointermove', e => {
      const t = tipDate(cfg.date + (it.total ? ' · 合计' : ''));
      t.append(tipRow(it.total ? 'var(--ink-1)' : bar.style.fill,
        '$' + it.v.toFixed(2) + ' / 万积分', it.total ? '当日单位成本' : it.name));
      if (!it.total) t.append(tipRow('var(--ink-3)', (it.v / cfg.total * 100).toFixed(1) + '%', '占当日'));
      tipShow(t, e.clientX, e.clientY);
    });
    hit.addEventListener('pointerleave', tipHide);
    svg.append(hit);
  });
  box.append(svg);
  if (ANIM && !RM) riseIn(bars, 40);
}
function wfTable(sel, parts, total) {
  const box = $(sel); if (!box) return; box.textContent = '';
  const d = document.createElement('details'), s = document.createElement('summary');
  s.textContent = '查看拆解数据表'; d.append(s);
  const w = div('tblwrap'), t = document.createElement('table');
  const thead = document.createElement('thead'), trh = document.createElement('tr');
  ['模型 / 成本项', '贡献（$/万积分）', '占当日'].forEach(hh => {
    const th = document.createElement('th'); th.textContent = hh; trh.append(th); });
  thead.append(trh); t.append(thead);
  const tb = document.createElement('tbody');
  parts.forEach(p => {
    const tr = document.createElement('tr');
    [p.name, '$' + p.v.toFixed(2), (p.v / total * 100).toFixed(1) + '%'].forEach(v => {
      const td = document.createElement('td'); td.textContent = v; tr.append(td); });
    tb.append(tr);
  });
  const tr = document.createElement('tr');
  ['当日合计', '$' + total.toFixed(2), '100%'].forEach(v => {
    const td = document.createElement('td'); td.textContent = v;
    td.style.fontWeight = 600; tr.append(td); });
  tb.append(tr);
  t.append(tb); w.append(t); d.append(w); box.append(d);
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

/* ---------- 迷你走势（12 点重采样 · 实体弱色描线 + 当期强调点，宽度自适应卡片） ---------- */
function spark(vals, color, w) {
  const M = 12;
  const vs = vals.length > M
    ? Array.from({ length: M }, (_, i) => vals[Math.round(i * (vals.length - 1) / (M - 1))]) : vals;
  const W = Math.max(80, Math.round(w || 120)), H = 38;
  const mn = Math.min(...vs), mx = Math.max(...vs);
  const X = i => 2 + i * (W - 8) / (vs.length - 1);
  const Y = v => 5 + (H - 10) * (1 - (v - mn) / ((mx - mn) || 1));
  const s = el('svg', { viewBox: `0 0 ${W} ${H}`, 'aria-hidden': 'true', preserveAspectRatio: 'xMidYMid meet' });
  s.append(el('path', { d: [`M ${X(0)} ${H - 3}`].concat(vs.map((v, i) => `L ${X(i)} ${Y(v)}`),
    [`L ${X(vs.length - 1)} ${H - 3}`, 'Z']).join(' '), fill: color, opacity: .16 }));
  s.append(el('path', { d: vs.map((v, i) => (i ? 'L' : 'M') + ` ${X(i)} ${Y(v)}`).join(' '),
    fill: 'none', stroke: color, 'stroke-opacity': .88, 'stroke-width': 2.2,
    'stroke-linecap': 'round', 'stroke-linejoin': 'round' }));
  s.append(el('circle', { cx: X(vs.length - 1), cy: Y(vs[vs.length - 1]), r: 4, fill: color, stroke: C.surface, 'stroke-width': 2 }));
  return s;
}

/* ---------- 窗口与渲染 ---------- */
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

function renderKpis(cost, mem, costAll) {
  const box = $('#kpis'); box.textContent = '';
  const totRev = mem.reduce((a, m) => a + m.net_rev, 0);
  const totMem = mem.reduce((a, m) => a + m.members, 0);
  const totCr = cost.reduce((a, c) => a + c.p_cr + c.s_cr + c.g_cr, 0);
  const subCost = cost.reduce((a, c) => a + c.s_cost, 0);
  const pEq = cost.reduce((a, c) => a + c.p_cr * 100, 0);
  const pCost = cost.reduce((a, c) => a + c.p_cost, 0);
  /* 逐日比率序列：比率卡与其他卡同构，也带迷你走势 */
  const subRatio = cost.filter(c => c.d >= LAUNCH && c.s_cost > 0)
    .map(c => c2rev(costAll, c.d) / c.s_cost);
  const pRatio = cost.filter(c => c.p_cost > 0).map(c => c.p_cr * 100 / c.p_cost);
  const tiles = [
    { lb: '累计净收入（仿真）', v: money(totRev), hero: true, color: C.s1,
      d: `订阅 + 购买 · ${mem.length} 天窗口`, spark: mem.map(m => m.net_rev) },
    { lb: '新增付费会员', v: intc(totMem) + ' 名', color: C.s1,
      d: prevDelta(mem.map(m => m.members)) || '会员系统 · 去重人数',
      spark: mem.map(m => m.members) },
    { lb: '期末 MRR', v: money(mem[mem.length - 1].mrr), color: C.s1,
      d: '截至窗口末日', spark: mem.map(m => m.mrr) },
    { lb: '累计核算积分消耗', v: wan(totCr) + ' 万', color: C.s2,
      d: '购买·订阅·赠送', spark: cost.map(c => c.p_cr + c.s_cr + c.g_cr) },
    { lb: '订阅收入成本比', v: subCost ? (totRev / subCost).toFixed(1) + ' 倍' : '—', color: C.s1,
      d: '分摊 ' + money(subCost), spark: subRatio },
    { lb: '购买收入成本比', v: pCost ? (pEq / pCost).toFixed(2) + ' 倍' : '—', color: C.s3,
      d: '分摊 ' + money(pCost), spark: pRatio },
  ];
  tiles.forEach(t => {
    const c = div('tile' + (t.hero ? ' khero' : ''));
    const lb = document.createElement('div'); lb.className = 'lb'; lb.textContent = t.lb; c.append(lb);
    const v = document.createElement('div'); v.className = 'v'; v.textContent = t.v; c.append(v);
    const dd = document.createElement('div'); dd.className = 'd';
    if (t.d && typeof t.d === 'object') {
      const u = document.createElement('span'); u.className = 'up'; u.textContent = t.d.txt; dd.append(u);
    } else dd.textContent = t.d || '';
    c.append(dd);
    box.append(c);
    /* 先入 DOM 量得卡内容宽，再按真实宽度画走势线（1:1 不变形） */
    if (t.spark && t.spark.some(x => isFinite(x) && x > 0))
      c.append(spark(t.spark, t.color, c.clientWidth - 32));
  });
  if (ANIM && !RM) box.querySelectorAll('.v').forEach(countUpVal);
  function prevDelta(a) {
    if (a.length < 8) return undefined;
    const prev = a.slice(-8, -1).reduce((x, y) => x + y, 0) / 7;
    const last = a[a.length - 1];
    const pct = Math.round((last / prev - 1) * 100);
    return { txt: `7日环比${pct >= 0 ? '+' : ''}${pct}%` };
  }
}

function renderAll(animate) {
  ANIM = animate !== false;
  __unitSync = null;   /* 旧闭包引用旧几何，先清掉；有选中标记时折线图会重新注册 */
  tipHide();
  const costAll = DATA.cost, memAll = DATA.mem;
  const cost = sliceDays(costAll, WIN);
  const mem = sliceDays(memAll, WIN);
  renderKpis(cost, mem, costAll);

  lineChart('#c_rev', { h: 250, dates: mem.map(m => m.d), name: '净收入',
    area: true, color: C.s1, tickFmt: v => v >= 1000 ? (v / 1000) + 'k' : v,
    tipFmt: v => money(v), endFmt: v => money(v), head: '日期',
    notes: WIN !== '30' ? [{ d: LAUNCH, label: '订阅上线' }] : [],
    series: [{ name: '净收入（仿真）', color: C.s1, values: mem.map(m => m.net_rev) }] });
  colChart('#c_mem', { h: 250, dates: mem.map(m => m.d), name: '新增会员',
    color: C.s1, tipFmt: v => intc(v) + ' 名', head: '日期',
    values: mem.map(m => m.members) });

  /* 02 双轨 ROI 对照：订阅/购买各一张指数图，两图共用同一 y 刻度与共享图例 */
  const subDays = cost.filter(c => c.d >= LAUNCH);
  const subRev = subDays.map(c => c.s_cost ? c2rev(costAll, c.d) : 0);
  const subCst = subDays.map(c => c.s_cost);
  const bi = subCst.findIndex(v => v > 0);
  const bR = (subRev[bi] || 1), bC = (subCst[bi] || 1);
  const subS = [
    { name: '订阅收入指数', color: C.s1, values: subRev.map(v => +(v / bR * 100).toFixed(1)) },
    { name: '订阅分摊成本指数', color: C.s2, values: subCst.map(v => +(v / bC * 100).toFixed(1)) } ];
  const proS = [
    { name: '购买等效指数', color: C.s3, values: idx(cost.map(c => c.p_cr * 100)) },
    { name: '购买分摊成本指数', color: C.s2, values: idx(cost.map(c => c.p_cost)) } ];
  const visOf = (key, len) => (HID[key] || Array(len).fill(false)).map(Boolean);
  const sv = visOf('subroi', 2), pv = visOf('proi', 2);
  /* 同刻度：只统计当前可见序列；隐藏后两图刻度同步重算，对照关系不破坏 */
  const roiVals = [...(sv[0] ? [] : subS[0].values), ...(sv[1] ? [] : subS[1].values),
    ...(pv[0] ? [] : proS[0].values), ...(pv[1] ? [] : proS[1].values)];
  const roiMax = Math.max(1, ...roiVals);
  const roiBase = { h: 300, tickFmt: v => v, tipFmt: v => v.toFixed(1), head: '日期',
    noLegend: true, yMax: roiMax, rerender: () => renderAll(false) };
  lineChart('#c_subroi', Object.assign({}, roiBase, {
    dates: subDays.map(c => c.d), name: '订阅ROI指数', key: 'subroi', series: subS }));
  lineChart('#c_proi', Object.assign({}, roiBase, {
    dates: cost.map(c => c.d), name: '购买ROI指数', key: 'proi', series: proS }));

  /* 共享图例：4 项跨两图联动显隐（每张图至少保留一条序列） */
  const rl = $('#roiLegend');
  if (rl) {
    rl.textContent = '';
    [ { key: 'subroi', i: 0, s: subS[0] }, { key: 'subroi', i: 1, s: subS[1] },
      { key: 'proi', i: 0, s: proS[0] }, { key: 'proi', i: 1, s: proS[1] } ].forEach(it => {
      const li = div('li'); li.setAttribute('role', 'button'); li.tabIndex = 0;
      li.title = '点击显示 / 隐藏该序列';
      const k = div(); k.className = 'ln'; k.style.background = it.s.color;
      const sp = document.createElement('span'); sp.textContent = it.s.name;
      li.append(k, sp);
      if (visOf(it.key, 2)[it.i]) { li.style.opacity = .38; sp.style.textDecoration = 'line-through'; }
      const tog = () => {
        const arr = HID[it.key] || (HID[it.key] = [false, false]);
        const nv = arr.map((v, j) => j === it.i ? !v : v);
        if (nv.every(x => x)) return;  /* 每张图至少保留一条序列 */
        arr[it.i] = !arr[it.i];
        renderAll(false);
      };
      li.addEventListener('click', tog);
      li.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tog(); } });
      rl.append(li);
    });
  }

  lineChart('#c_unit', { h: 250, dates: cost.map(c => c.d), name: '单位成本指数', key: 'unit',
    area: true, color: C.s1, tickFmt: v => v, tipFmt: v => v.toFixed(1), head: '日期',
    pick: PICKD, onPick: d => { stopPlay(); PICKD = (PICKD === d ? null : d); renderAll(false); },
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

  /* 05 分摊全景 + 质量条 + 单位成本钻取 */
  const sdS = sliceDays(DATA.src_daily, WIN);
  sankeyChart('#c_sankey', aggFlows(cost, sdS));
  qualityStrip('#c_qual', sliceDays(DATA.quality, WIN));
  CURCOST = cost;
  renderDrill(cost);
}
function aggFlows(cost, sd) {
  const bkt = ['购买', '订阅', '赠送'];
  const st = DATA.src_names.map(() => 0);
  const fm = DATA.src_names.map(() => [0, 0, 0]);
  cost.forEach((c, i) => {
    const row = sd[i]; const s = c.p_cr + c.s_cr + c.g_cr;
    const bs = [c.p_cr / s, c.s_cr / s, c.g_cr / s];
    row.s.forEach((v, si) => bs.forEach((sh, bi) => {
      const x = v * sh; st[si] += x; fm[si][bi] += x;
    }));
  });
  const flows = [];
  DATA.src_names.forEach((sn, si) => bkt.forEach((bn, bi) => flows.push({ s: sn, b: bn, v: fm[si][bi] })));
  return { flows, src: st, bktNames: bkt };
}
function renderDrill(cost) {
  const d = PICKD || cost[cost.length - 1].d;
  const up = DATA.unit_parts.find(u => u.d === d) || DATA.unit_parts[DATA.unit_parts.length - 1];
  const total = up.parts.reduce((a, p) => a + p.v, 0);
  $('#wdate').textContent = '当前：' + d + ' · 合计 $' + total.toFixed(2) + ' / 万积分';
  waterfall('#c_wf', { parts: up.parts, total, date: d });
  wfTable('#t_wf', up.parts, total);
}

/* ---------- 钻取逐日播放器 ---------- */
function stopPlay() {
  if (!PLAY) return;
  clearInterval(PLAY); PLAY = null;
  const b = $('#pPlay'); b.setAttribute('aria-pressed', 'false'); b.textContent = '⏵ 播放';
}
function stepDrill(dir) {
  const ds = CURCOST.map(c => c.d);
  const i = ds.indexOf(PICKD || ds[ds.length - 1]);
  const j = Math.max(0, Math.min(ds.length - 1, i + dir));
  if (j === i) return;
  PICKD = ds[j];
  ANIM = true;                    /* 单步小动画；RM 用户自动被 &&RM 关闭 */
  renderDrill(CURCOST);
  if (__unitSync) __unitSync(PICKD);
}
$('#pPrev').addEventListener('click', () => { stopPlay(); stepDrill(-1); });
$('#pNext').addEventListener('click', () => { stopPlay(); stepDrill(1); });
$('#pPlay').addEventListener('click', () => {
  if (PLAY) { stopPlay(); return; }
  const ds = CURCOST.map(c => c.d);
  if ((PICKD || ds[ds.length - 1]) === ds[ds.length - 1]) {  /* 已在末日则从头播 */
    PICKD = ds[0]; renderDrill(CURCOST); if (__unitSync) __unitSync(PICKD);
  }
  const b = $('#pPlay'); b.setAttribute('aria-pressed', 'true'); b.textContent = '⏸ 暂停';
  PLAY = setInterval(() => {
    const cur = PICKD || ds[ds.length - 1];
    if (cur === ds[ds.length - 1]) { stopPlay(); return; }
    stepDrill(1);
  }, 700);
});
function c2rev(costAll, d) {
  return DATA.mem.find(m => m.d === d)?.net_rev || 0;
}

/* ---------- 筛选与主题 ---------- */
document.querySelectorAll('.seg button').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('.seg button').forEach(x => x.setAttribute('aria-pressed', 'false'));
    b.setAttribute('aria-pressed', 'true');
    WIN = b.dataset.win; PICKD = null; renderAll(true);
  });
});
const themeBtn = $('#themeBtn');
const saved = localStorage.getItem('pf-theme');
if (saved === 'light') document.documentElement.setAttribute('data-theme', 'light');
themeBtn.addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'light' ? 'dark' : 'light';  /* v4：默认深色，切换即 light↔dark */
  if (next === 'dark') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', 'light');
  localStorage.setItem('pf-theme', next);
  renderAll(false);
});
let rT; addEventListener('resize', () => { clearTimeout(rT); rT = setTimeout(() => renderAll(false), 150); });

/* ---------- 叙事层：渐显 / 进度条 / 章节联动 ---------- */
const io = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); }
}), { threshold: .08 });
document.querySelectorAll('.rv').forEach(n => io.observe(n));

const SECS = [['top', '总览'], ['revenue', '收入概览'], ['subroi', '双轨 ROI 对照'],
  ['cost', '购买成本'], ['alloc', '分摊与质量']];
const rail = $('#rail');
SECS.forEach(([id, t]) => {
  const a = document.createElement('a'); a.href = '#' + id; a.title = t;
  const s = document.createElement('span'); s.textContent = t;
  a.append(s); rail.append(a);
});
const prog = $('#prog');
function spy() {
  const h = document.documentElement;
  const p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
  prog.style.width = (p * 100).toFixed(2) + '%';
  let cur = SECS[0][0];
  SECS.forEach(([id]) => {
    const n = document.getElementById(id);
    if (n && n.getBoundingClientRect().top <= 170) cur = id;
  });
  rail.querySelectorAll('a').forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + cur));
  document.querySelectorAll('.navbar a').forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + cur));
}
addEventListener('scroll', spy, { passive: true });

/* ---------- 回到顶部 ---------- */
const totop = $('#totop');
addEventListener('scroll', () => totop.classList.toggle('on', scrollY > 600), { passive: true });
totop.addEventListener('click', () => scrollTo({ top: 0, behavior: RM ? 'auto' : 'smooth' }));

renderAll(true);
spy();
</script>
</body>
</html>
"""

out = os.path.join(HERE, "index.html")
html = HTML.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
with io.open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("written:", out, len(html), "chars")
