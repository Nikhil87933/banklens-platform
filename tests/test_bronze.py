from pathlib import Path

def test_bronze_runner_exists():
    assert Path("01_bronze/02_run_bronze.py").exists()