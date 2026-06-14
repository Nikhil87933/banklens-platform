# BankLens Workflow DAG

Bronze Ingestion
        ↓
Silver Standardisation
        ↓
Gold Mart Generation
        ↓
Dashboard Refresh

Dependencies:

1. Bronze must complete successfully
2. Silver starts only after Bronze success
3. Gold starts only after Silver success
4. Dashboards consume Gold tables

Failure Handling:

- Audit log records failure
- Pipeline control table records last successful run
- Re-run starts from failed layer