from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .benchmark_engine import build_report, generate_all_assets


class WorkflowEngine:
    """Production workflow for generating benchmark, GEO, and visibility outputs."""

    def __init__(self, output_dir: str = "advanced_seo_ai_visibility/output") -> None:
        self.output_dir = Path(output_dir)

    def run(self) -> Dict[str, Any]:
        report = generate_all_assets(str(self.output_dir))
        return report

    def render_dashboard(self) -> str:
        from .dashboard import render_dashboard

        report = build_report()
        output_path = self.output_dir / "dashboard.html"
        render_dashboard(report, output_path)
        return str(output_path)

    def export_all(self) -> Dict[str, Any]:
        report = self.run()
        self.render_dashboard()
        return report


if __name__ == "__main__":
    engine = WorkflowEngine()
    engine.export_all()
    print("Workflow complete. Outputs generated.")
