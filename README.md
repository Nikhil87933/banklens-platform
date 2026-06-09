# BankLens Platform

End-to-end banking data engineering platform built on Databricks.

Synthetic Australian banking dataset. Medallion architecture.

Bronze → Silver → Gold | Delta Lake | Unity Catalog

## Dataset

12 banking tables.
55,000 customers.
5 days of incremental data.

Includes intentional data quality issues on Days 3, 4, and 5.

## Technology Stack

- Databricks
- Unity Catalog
- Delta Lake
- GitHub
- GitHub Actions
- Python
- SQL

## Architecture

Raw Files → Bronze → Data Quality → Silver → Gold