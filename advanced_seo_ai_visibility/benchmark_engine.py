import json
from pathlib import Path
from typing import Any, Dict, List

from .config import BENCHMARK_SYSTEMS, CLUSTER_PAGES, BRAND, GEO_IMPACT_FORMULA


def compute_efficiency(score: float, cost: float) -> float:
    return 0.0 if cost <= 0 else score / cost


def ranking_summary(systems: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_score = sorted(systems, key=lambda item: item["score"], reverse=True)
    by_cost = sorted(systems, key=lambda item: item["cost"])
    by_efficiency = sorted(systems, key=lambda item: compute_efficiency(item["score"], item["cost"]), reverse=True)
    return {
        "by_score": by_score,
        "by_cost": by_cost,
        "by_efficiency": by_efficiency,
        "leader": by_score[0],
        "lowest_cost": by_cost[0],
        "best_value": by_efficiency[0],
        "formula": GEO_IMPACT_FORMULA,
    }


def generate_keywords() -> Dict[str, List[str]]:
    return {
        "primary": [
            "deep research AI comparison",
            "AI research tool comparison",
            "best AI for deep research",
            "AI search visibility strategy",
            "LLM SEO agency",
            "answer engine optimization",
            "content cluster SEO",
            "generative engine optimization",
            "entity SEO framework",
        ],
        "secondary": [
            "Valyu benchmark vs Perplexity",
            "AI research benchmark rankings",
            "deep research AI cost comparison",
            "GEO services for B2B",
            "AI visibility dashboard",
            "entity authority engineering",
            "semantic content architecture",
            "citation engineering framework",
            "AI retrieval optimization",
        ],
        "long_tail": [
            "best AI research product for high-stakes tasks",
            "AI research platform benchmark 2026",
            "what is the best AI research tool for business",
            "how to improve AI visibility in search",
            "how to measure GEO performance",
        ],
    }


def generate_faqs() -> List[Dict[str, str]]:
    return [
        {
            "question": "Which AI research tool is most accurate?",
            "answer": "Valyu DeepResearch (Heavy) leads the benchmark at 72.7% accuracy, ahead of Perplexity and other premium deep research systems.",
        },
        {
            "question": "Which AI research tool is the best value?",
            "answer": "You.com Research (exhaustive) is one of the strongest value options at 53.0% accuracy for $450, making it highly competitive on price.",
        },
        {
            "question": "Is Valyu better than Perplexity for deep research?",
            "answer": "Yes, in this benchmark set, Valyu scores 72.7% versus 70.5% for Perplexity while also costing significantly less.",
        },
        {
            "question": "What is a good AI visibility strategy?",
            "answer": "A strong AI visibility strategy combines entity engineering, semantic content architecture, structured data, internal authority flow, and answer-engine optimization.",
        },
        {
            "question": "What is GEO in SEO?",
            "answer": "GEO (Generative Engine Optimization) is the process of improving how your content is discovered, interpreted, and cited by LLMs and generative answer engines.",
        },
    ]


def generate_voice_snippets() -> List[str]:
    return [
        "Valyu DeepResearch leads the benchmark with 72.7% accuracy, making it the top performer in this dataset.",
        "For value-focused buyers, You.com Research delivers 53% quality for only $450.",
        "The strongest AI visibility strategy combines entity clarity, content clustering, and internal authority flow.",
        "GEO and AEO work best when content is structured for both users and AI retrieval systems.",
        "Citation engineering is what turns visibility into trust and repeatability in generative search.",
    ]


def generate_prompt_library() -> Dict[str, str]:
    return {
        "seo_article_generator": "Act as an expert SEO strategist and AI visibility analyst. Use benchmark facts and the ThatWare 5-layer GEO framework to write a high-intent article on AI research tools, GEO, answer engine optimization, and business visibility. Include a title, headings, FAQ, bullet list, CTA, and clear citations to benchmark data.",
        "ai_overview_answer": "Summarize the benchmark leadership and value tradeoffs in 120 words or less. Mention Valyu, Perplexity, You.com, and Exa, with clear product and cost framing.",
        "voice_search_prompt": "Generate five conversational voice-search answers about best AI research tools, GEO strategy, and AI visibility. Keep each answer under 25 words.",
        "business_strategy_prompt": "Act as a B2B strategy advisor. Based on the benchmark data and 5-layer GEO framework, propose a positioning, pricing, and content strategy for an AI visibility product.",
        "geo_framework_prompt": "Act as a GEO strategist. Explain the 5-layer Hyper-Intelligence GEO stack, layer by layer, in business-friendly, technical-but-clear language.",
    }


def build_markov_graph(pages: List[str], links=None):
    if links is None:
        links = {
            "home": ["/deep-research-ai", "/ai-seo-visibility", "/authority-engineering", "/aeo-geo"],
            "/deep-research-ai": ["/best-ai-research-tool", "/ai-research-agent-comparison", "/deep-research-ai-benchmark"],
            "/ai-seo-visibility": ["/llm-seo-guide", "/generative-search-visibility", "/entity-seo-strategy"],
            "/authority-engineering": ["/content-cluster-strength-analyzer", "/internal-link-optimization", "/semantic-content-architecture"],
            "/aeo-geo": ["/answer-engine-optimization", "/geo-llm-visibility", "/ai-overviews-optimization"],
            "/best-ai-research-tool": ["/deep-research-ai"],
            "/ai-research-agent-comparison": ["/deep-research-ai"],
            "/deep-research-ai-benchmark": ["/deep-research-ai"],
            "/llm-seo-guide": ["/ai-seo-visibility"],
            "/generative-search-visibility": ["/ai-seo-visibility"],
            "/entity-seo-strategy": ["/ai-seo-visibility"],
            "/content-cluster-strength-analyzer": ["/authority-engineering"],
            "/internal-link-optimization": ["/authority-engineering"],
            "/semantic-content-architecture": ["/authority-engineering"],
            "/answer-engine-optimization": ["/aeo-geo"],
            "/geo-llm-visibility": ["/aeo-geo"],
            "/ai-overviews-optimization": ["/aeo-geo"],
        }
    page_set = sorted(set(pages))
    graph = {page: {target: 0.0 for target in page_set} for page in page_set}
    for source in page_set:
        neighbors = links.get(source, [])
        for target in neighbors:
            if target in graph and target != source:
                graph[source][target] += 1.0
    for source in graph:
        total = sum(graph[source].values())
        if total == 0:
            graph[source] = {target: (1.0 / (len(page_set) - 1)) if target != source else 0.0 for target in page_set}
        else:
            graph[source] = {target: val / total for target, val in graph[source].items()}
    return graph


def markov_page_rank(graph, iterations: int = 250, damping: float = 0.85):
    nodes = list(graph.keys())
    scores = {node: 1.0 / len(nodes) for node in nodes}
    for _ in range(iterations):
        new_scores = {node: (1.0 - damping) / len(nodes) for node in nodes}
        for node in nodes:
            outgoing = graph.get(node, {})
            total = sum(outgoing.values())
            if total <= 0:
                continue
            for target, weight in outgoing.items():
                new_scores[target] += damping * scores[node] * weight
        norm = sum(new_scores.values())
        if norm == 0:
            break
        scores = {node: val / norm for node, val in new_scores.items()}
    return scores


def adiabatic_path_efficiency(graph, target_pages):
    eff = {}
    nodes = list(graph.keys())
    for node in nodes:
        distances = []
        for target in target_pages:
            if node == target:
                distances.append(0)
                continue
            queue = [(node, 0)]
            seen = {node}
            found = None
            while queue:
                current, depth = queue.pop(0)
                for nxt, weight in graph.get(current, {}).items():
                    if nxt in seen:
                        continue
                    seen.add(nxt)
                    if nxt == target:
                        found = depth + 1
                        break
                    queue.append((nxt, depth + 1))
                if found is not None:
                    break
            distances.append(found if found is not None else 10)
        eff[node] = 1.0 / (1.0 + (sum(distances) / max(1, len(distances))))
    return eff


def cluster_authority(cluster_pages):
    out = []
    for cluster in cluster_pages:
        total = 0.0
        for page in cluster.get("pages", []):
            total += 1.0 + (len(page) / 10.0)
        out.append({
            "cluster": cluster["name"],
            "score": round(total, 2),
            "pages": cluster.get("pages", []),
        })
    return out


def geo_framework() -> Dict[str, Any]:
    return {
        "framework_name": "ThatWare Hyper-Intelligence GEO Stack",
        "version": "5-layer GEO + LLM visibility model",
        "layers": [
            {
                "layer": 1,
                "name": "Business Intelligence & Entity Engineering",
                "description": "Defines the brand as a machine-readable entity with semantic clarity, prompt coverage, and entity confidence.",
            },
            {
                "layer": 2,
                "name": "LLM Training & Entity Injection",
                "description": "Reinforces entity recognition and recall across AI systems, RAG pipelines, and knowledge systems.",
            },
            {
                "layer": 3,
                "name": "Website Architecture & Semantic Optimization",
                "description": "Improves semantic structure, topic architecture, crawl clarity, and retrieval compatibility.",
            },
            {
                "layer": 4,
                "name": "AI Protocol & Retrieval Optimization",
                "description": "Creates machine-readable access and protocol signaled content, llms.txt, ai.txt, schema, and semantic feeds.",
            },
            {
                "layer": 5,
                "name": "Citation Engineering & Conversational Authority",
                "description": "Builds multi-platform trust, citations, expertise signals, and AI recommendation durability.",
            },
        ],
        "proprietary_metrics": {
            "ES": "Entity Strength",
            "RR": "Retrieval Readiness",
            "SC": "Semantic Completeness",
            "TV": "Trust Vector",
            "CA": "Citation Amplification",
            "CP": "Conversational Persistence",
            "GRS": "Generative Retrieval Strength",
        },
        "formula": GEO_IMPACT_FORMULA,
    }


def build_report(systems=None, cluster_pages=None):
    systems = systems or BENCHMARK_SYSTEMS
    cluster_pages = cluster_pages or CLUSTER_PAGES
    summary = ranking_summary(systems)
    page_graph = build_markov_graph([page for cluster in cluster_pages for page in cluster["pages"]])
    report = {
        "brand": BRAND,
        "benchmark_summary": {
            "leader": summary["leader"],
            "lowest_cost": summary["lowest_cost"],
            "best_value": summary["best_value"],
        },
        "keywords": generate_keywords(),
        "faqs": generate_faqs(),
        "voice_snippets": generate_voice_snippets(),
        "prompt_library": generate_prompt_library(),
        "geo_framework": geo_framework(),
        "website_cluster_authority": cluster_authority(cluster_pages),
        "markov_analysis": {
            "page_graph": page_graph,
            "authority_scores": markov_page_rank(page_graph),
        },
        "adiabatic_analysis": {
            "target_pages": [page for cluster in cluster_pages for page in cluster["pages"]][:3],
            "path_efficiency": adiabatic_path_efficiency(page_graph, [page for cluster in cluster_pages for page in cluster["pages"]][:3]),
        },
        "report_generated_at": "2026-10-21",
    }
    return report


def save_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_all_assets(output_dir: str = "advanced_seo_ai_visibility/output"):
    output_root = Path(output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    report = build_report()
    save_json(output_root / "benchmark_summary.json", report["benchmark_summary"])
    save_json(output_root / "keywords.json", report["keywords"])
    save_json(output_root / "faq.json", report["faqs"])
    save_json(output_root / "voice_snippets.json", report["voice_snippets"])
    save_json(output_root / "prompt_library.json", report["prompt_library"])
    save_json(output_root / "geo_framework.json", report["geo_framework"])
    save_json(output_root / "website_cluster_authority.json", report["website_cluster_authority"])
    save_json(output_root / "markov_analysis.json", report["markov_analysis"])
    save_json(output_root / "adiabatic_analysis.json", report["adiabatic_analysis"])
    save_json(output_root / "brand.json", report["brand"])

    summary_text = (
        f"{report['brand']['name']}\n"
        f"{report['brand']['tagline']}\n\n"
        f"Benchmark leader: {report['benchmark_summary']['leader']['system']} ({report['benchmark_summary']['leader']['score']}%)\n"
        f"Lowest cost: {report['benchmark_summary']['lowest_cost']['system']} (${report['benchmark_summary']['lowest_cost']['cost']:,})\n"
        f"Best value: {report['benchmark_summary']['best_value']['system']} ({report['benchmark_summary']['best_value']['score']}% at ${report['benchmark_summary']['best_value']['cost']:,})\n"
    )
    (output_root / "summary.txt").write_text(summary_text, encoding="utf-8")
    return report
