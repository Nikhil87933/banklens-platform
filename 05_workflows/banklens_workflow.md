# BankLens Orchestration

Workflow Name:
banklens_daily_pipeline

Schedule:
Daily

Tasks:

Task 1:
Bronze Ingestion
File:
01_bronze/02_run_bronze.py

Task 2:
Silver Standardisation
File:
02_silver/02_run_silver.py

Task 3:
Gold Layer
File:
03_gold/02_run_gold.py

Dependencies:

Bronze → Silver → Gold