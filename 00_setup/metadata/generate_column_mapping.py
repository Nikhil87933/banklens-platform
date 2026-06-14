"""
generate_column_mapping.py
──────────────────────────
Generates column_mapping.csv from schema_definitions.py.

No datatype inference.
No sample data generation.
No pandas dtype detection.
No imports from generate_data.py.

Run this whenever schema_definitions.py changes:
    python generate_column_mapping.py

Output: column_mapping.csv (same directory as this script)

column_mapping.csv is consumed by:
    06_metadata/01_load_column_mapping.py  →  loads into metadata table in Databricks
"""

import csv
from pathlib import Path
from schema_definitions import SCHEMA_REGISTRY


OUTPUT_FILE = Path(__file__).parent / "column_mapping.csv"
FIELDNAMES  = ["table_name", "column_name", "target_type", "format_string", "is_active"]


def generate():
    rows = []

    for table_name, columns in SCHEMA_REGISTRY.items():
        for col in columns:
            rows.append({
                "table_name":    table_name,
                "column_name":   col["column_name"],
                "target_type":   col["target_type"],
                "format_string": col["format_string"],
                "is_active":     col["is_active"],
            })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    # Summary
    table_counts = {}
    for row in rows:
        table_counts[row["table_name"]] = table_counts.get(row["table_name"], 0) + 1

    print(f"\ncolumn_mapping.csv generated → {OUTPUT_FILE}")
    print(f"{'─' * 50}")
    print(f"{'Table':<35} {'Columns':>7}")
    print(f"{'─' * 50}")
    for table, count in table_counts.items():
        print(f"  {table:<33} {count:>7}")
    print(f"{'─' * 50}")
    print(f"  {'TOTAL':<33} {len(rows):>7}")
    print()


if __name__ == "__main__":
    generate()
