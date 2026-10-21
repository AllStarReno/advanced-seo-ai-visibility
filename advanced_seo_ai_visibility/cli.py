import argparse
import json
from pathlib import Path

from .benchmark_engine import build_report, generate_all_assets


def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced SEO + AI Visibility generator")
    parser.add_argument("--output", default="advanced_seo_ai_visibility/output", help="Directory to write generated assets")
    args = parser.parse_args()

    report = generate_all_assets(output_dir=args.output)
    print(json.dumps({
        "leader": report["benchmark_summary"]["leader"]["system"],
        "leader_score": report["benchmark_summary"]["leader"]["score"],
        "best_value": report["benchmark_summary"]["best_value"]["system"],
    }, indent=2))


if __name__ == "__main__":
    main()
