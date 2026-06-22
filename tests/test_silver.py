from pathlib import Path

def test_silver_runner_exists():
    assert Path("02_silver/02_run_silver.py").exists()

def test_gold_runner_exists():
    assert Path("03_gold/02_run_gold.py").exists()