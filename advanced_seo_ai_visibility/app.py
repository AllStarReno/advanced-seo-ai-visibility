from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, render_template

from .benchmark_engine import build_report

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    report = build_report()
    return render_template("index.html", report=report)


@app.route("/api/report")
def api_report():
    return jsonify(build_report())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
