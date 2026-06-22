from pathlib import Path

def test_customer_360_exists():
    assert Path("03_gold/marts/customer_360.py").exists()