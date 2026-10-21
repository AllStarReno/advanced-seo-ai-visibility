import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from .config import BENCHMARK_SYSTEMS, BRAND
from .benchmark_engine import build_report, generate_all_assets


def init_db(db_path: str = "advanced_seo_ai_visibility/data/benchmark_visibility.db") -> sqlite3.Connection:
    db_path_obj = Path(db_path)
    db_path_obj.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path_obj))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS benchmark_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system TEXT,
            score REAL,
            cost REAL,
            category TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS report_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT
        )
        """
    )
    conn.commit()
    return conn


def insert_benchmarks(conn: sqlite3.Connection, systems: List[Dict[str, Any]]) -> None:
    conn.execute("DELETE FROM benchmark_results")
    conn.executemany(
        "INSERT INTO benchmark_results (system, score, cost, category) VALUES (?, ?, ?, ?)",
        [(item["system"], item["score"], item["cost"], item["category"]) for item in systems],
    )
    conn.commit()


def snapshot_report(conn: sqlite3.Connection, report: Dict[str, Any]) -> None:
    conn.execute("INSERT INTO report_snapshots (payload) VALUES (?)", (str(report),))
    conn.commit()


def main() -> None:
    report = build_report()
    conn = init_db()
    insert_benchmarks(conn, BENCHMARK_SYSTEMS)
    snapshot_report(conn, report)
    conn.close()
    print(f"{BRAND['name']} generated report snapshot and DB archive.")


if __name__ == "__main__":
    main()
