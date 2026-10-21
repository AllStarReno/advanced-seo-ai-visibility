from __future__ import annotations

import argparse
import json
from pathlib import Path

from .workflow import WorkflowEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced SEO + AI Visibility workflow and dashboard")
    parser.add_argument("--output", default="advanced_seo_ai_visibility/output", help="Output directory")
    parser.add_argument("--dashboard", action="store_true", help="Generate HTML dashboard")
    parser.add_argument("--workflow", action="store_true", help="Run full workflow and export assets")
    args = parser.parse_args()

    engine = WorkflowEngine(output_dir=args.output)
    if args.dashboard:
        dashboard_path = engine.render_dashboard()
        print(json.dumps({"dashboard": dashboard_path}, indent=2))
    else:
        report = engine.export_all()
        print(json.dumps({
            "leader": report["benchmark_summary"]["leader"]["system"],
            "leader_score": report["benchmark_summary"]["leader"]["score"],
            "best_value": report["benchmark_summary"]["best_value"]["system"],
            "dashboard": str(Path(args.output) / "dashboard.html"),
        }, indent=2))


if __name__ == "__main__":
    main()
