from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Dict


def _card(label: str, value: str, tone: str = "primary") -> str:
    return f"""
    <div class=\"card {tone}\">
      <div class=\"label\">{escape(label)}</div>
      <div class=\"value\">{escape(value)}</div>
    </div>
    """


def render_dashboard(report: Dict[str, Any], output_path: str | Path) -> str:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    leader = report["benchmark_summary"]["leader"]
    lowest_cost = report["benchmark_summary"]["lowest_cost"]
    best_value = report["benchmark_summary"]["best_value"]
    brand = report["brand"]
    geo_layers = report["geo_framework"]["layers"]
    cluster_auth = report["website_cluster_authority"]
    faqs = report["faqs"]
    snippets = report["voice_snippets"]
    prompt_library = report["prompt_library"]
    authority_scores = report["markov_analysis"]["authority_scores"]

    rows = []
    for item in report["benchmark_summary"]["leader"].get("by_score", []):
        pass

    leaderboard = sorted(report["benchmark_summary"]["leader"].get("by_score", []), key=lambda x: x["score"], reverse=True)
    if not leaderboard:
        leaderboard = [leader, lowest_cost, best_value]

    leaderboard_rows = "".join(
        f"<tr><td>{i + 1}</td><td>{escape(item['system'])}</td><td>{item['score']}</td><td>${item['cost']:,}</td><td>{escape(item.get('category',''))}</td></tr>"
        for i, item in enumerate(sorted(leaderboard, key=lambda x: x["score"], reverse=True))
    )

    cluster_rows = "".join(
        f"<tr><td>{escape(item['cluster'])}</td><td>{item['score']}</td><td>{len(item.get('pages', []))}</td></tr>"
        for item in cluster_auth
    )

    geo_rows = "".join(
        f"<tr><td>{item['layer']}</td><td>{escape(item['name'])}</td><td>{escape(item['description'])}</td></tr>"
        for item in geo_layers
    )

    faq_rows = "".join(
        f"<li><strong>{escape(item['question'])}</strong><br>{escape(item['answer'])}</li>" for item in faqs
    )

    snippet_rows = "".join(f"<li>{escape(item)}</li>" for item in snippets)

    prompt_rows = "".join(
        f"<li><strong>{escape(name)}</strong>: {escape(value)}</li>" for name, value in prompt_library.items()
    )

    authority_rows = "".join(
        f"<tr><td>{escape(path)}</td><td>{value:.4f}</td></tr>" for path, value in sorted(authority_scores.items(), key=lambda kv: kv[1], reverse=True)[:10]
    )

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(brand['name'])}</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #111b2d;
      --panel-alt: #16233d;
      --text: #edf4ff;
      --muted: #a4b6d6;
      --primary: #6ea8fe;
      --accent: #8ce99a;
      --warn: #ffd43b;
      --shadow: rgba(0,0,0,.25);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; font-family: Arial, sans-serif; background: linear-gradient(180deg, var(--bg), #101b2c);
      color: var(--text);
    }}
    header {{
      background: rgba(15, 22, 38, 0.95); border-bottom: 1px solid rgba(255,255,255,0.08); padding: 32px 24px;
    }}
    .container {{ max-width: 1280px; margin: 0 auto; }}
    .hero {{ display: flex; justify-content: space-between; align-items: end; gap: 24px; flex-wrap: wrap; }}
    h1 {{ font-size: 2.4rem; margin: 0 0 8px; }}
    .subtitle {{ color: var(--muted); max-width: 720px; line-height: 1.6; }}
    .pill {{ display: inline-block; background: rgba(110, 168, 254, .15); border: 1px solid rgba(110,168,254,.3); color: #dfeeff; padding: 8px 14px; border-radius: 999px; font-size: 12px; margin-top: 12px; }}
    main {{ padding: 32px 24px 80px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; margin: 24px 0 32px; }}
    .card {{ background: rgba(17,27,45,0.9); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 18px; box-shadow: 0 14px 35px var(--shadow); }}
    .card.primary {{ border-color: rgba(110,168,254,.4); }}
    .card.success {{ border-color: rgba(140,233,154,.4); }}
    .label {{ color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; font-size: 11px; margin-bottom: 10px; }}
    .value {{ font-size: 1.8rem; font-weight: 700; }}
    section {{ margin-top: 34px; }}
    h2 {{ font-size: 1.4rem; margin: 0 0 16px; }}
    table {{ width: 100%; background: rgba(17,27,45,.9); border-collapse: collapse; border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,.08); }}
    th, td {{ padding: 12px 14px; border-bottom: 1px solid rgba(255,255,255,.06); text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; }}
    tr:last-child td {{ border-bottom: none; }}
    ul {{ padding-left: 18px; line-height: 1.8; color: var(--text); }}
    .two-col {{ display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 20px; }}
    @media (max-width: 900px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <div class="container hero">
      <div>
        <div class="pill">GEO / AEO / AI Visibility</div>
        <h1>{escape(brand['name'])}</h1>
        <div class="subtitle">{escape(brand['tagline'])}</div>
      </div>
      <div class="card success">
        <div class="label">Brand Positioning</div>
        <div class="value" style="font-size: 1rem; line-height:1.5;">{escape(brand['positioning'])}</div>
      </div>
    </div>
  </header>
  <main class="container">
    <div class="grid">
      {_card('Benchmark Leader', f"{leader['system']} • {leader['score']}%", 'primary')}
      {_card('Lowest Cost', f"{lowest_cost['system']} • ${lowest_cost['cost']:,}", 'success')}
      {_card('Best Value', f"{best_value['system']} • {best_value['score']}%", 'primary')}
      {_card('GRS Formula', 'ES × RR × SC × TV × CA × CP', 'success')}
    </div>

    <section>
      <h2>Leaderboard</h2>
      <table>
        <thead>
          <tr><th>#</th><th>System</th><th>Score</th><th>Cost</th><th>Category</th></tr>
        </thead>
        <tbody>
          {leaderboard_rows}
        </tbody>
      </table>
    </section>

    <section class="two-col">
      <div>
        <h2>Content Cluster Authority</h2>
        <table>
          <thead><tr><th>Cluster</th><th>Authority</th><th>Pages</th></tr></thead>
          <tbody>{cluster_rows}</tbody>
        </table>
      </div>
      <div>
        <h2>Authority Scores</h2>
        <table>
          <thead><tr><th>Path</th><th>Score</th></tr></thead>
          <tbody>{authority_rows}</tbody>
        </table>
      </div>
    </section>

    <section>
      <h2>5-Layer GEO Framework</h2>
      <table>
        <thead><tr><th>Layer</th><th>Name</th><th>Description</th></tr></thead>
        <tbody>{geo_rows}</tbody>
      </table>
    </section>

    <section class="two-col">
      <div>
        <h2>FAQ</h2>
        <ul>{faq_rows}</ul>
      </div>
      <div>
        <h2>Voice Snippets</h2>
        <ul>{snippet_rows}</ul>
      </div>
    </section>

    <section>
      <h2>Prompt Library</h2>
      <ul>{prompt_rows}</ul>
    </section>
  </main>
</body>
</html>
"""
    output_path.write_text(html, encoding="utf-8")
    return str(output_path)
