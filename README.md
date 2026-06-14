# BankLens – End-to-End Banking Data & AI Platform

## Overview

BankLens is an end-to-end banking data platform built on Databricks using a Medallion Architecture (Bronze, Silver, Gold) approach. The project simulates how a modern bank ingests, standardizes, governs, analyzes, and predicts customer behavior using Data Engineering and Machine Learning.

The platform processes data from multiple banking domains including customers, accounts, transactions, loans, products, digital activity, and support interactions. It provides a unified Customer 360 view, business-ready data marts, workflow orchestration, and predictive analytics.

---

# Business Problem

Banks generate data across multiple systems including customer onboarding, core banking, transactions, loans, digital banking applications, and support platforms.

This data is often fragmented and difficult to analyze efficiently.

BankLens solves this problem by creating a centralized platform that:

* Ingests data from multiple source systems
* Standardizes and governs data
* Tracks pipeline execution and schema changes
* Produces business-ready analytical datasets
* Generates machine learning predictions

---

# Technology Stack

## Data Engineering

* Databricks
* Delta Lake
* Unity Catalog
* PySpark
* SQL

## DevOps

* Git
* GitHub
* Feature Branch Workflow

## Machine Learning

* Scikit-Learn
* Pandas
* Random Forest

---

# Project Architecture

```text
Source Files
      ↓
Bronze Layer
      ↓
Metadata Framework
      ↓
Silver Layer
      ↓
Governance Controls
      ↓
Gold Layer
      ↓
Machine Learning Layer
```

---

# Dataset

A synthetic banking dataset was generated to simulate real-world banking operations.

## Scale

* 55,000 Customers
* 12 Source Tables
* Multi-day data simulation

## Source Tables

### Customer Domain

* customer_master

### Accounts Domain

* account_master
* account_balance_snapshot

### Transactions Domain

* transaction_fact
* card_transaction_fact

### Lending Domain

* loan_master

### Products Domain

* product_holdings

### Digital Banking Domain

* digital_activity
* device_events

### Customer Service Domain

* support_tickets

### Reference Data

* merchant_reference
* market_rates

Intentional data quality issues were introduced to validate governance controls and schema monitoring.

---

# Bronze Layer

## Purpose

Store source data exactly as received.

## Features

* Metadata-aware ingestion framework
* Raw data preservation
* Replayability
* Source traceability

## Output

Examples:

* brz_customer_master
* brz_account_master
* brz_transaction_fact
* brz_loan_master

---

# Metadata Framework

A centralized metadata registry was implemented to drive downstream processing.

## Metadata Registry

```text
banklens.metadata.column_mapping
```

Stores:

* Table Names
* Column Names
* Expected Data Types
* Date Formats
* Active Flags

## Benefits

* No hardcoded schemas
* Centralized transformation rules
* Easier maintenance and scalability

---

# Silver Layer

## Purpose

Convert raw data into trusted analytical datasets.

## Features

* Metadata-driven processing
* Data type standardization
* Date format standardization
* Reusable transformation framework

## Output

Examples:

* slv_customer_master
* slv_account_master
* slv_transaction_fact
* slv_loan_master

---

# Governance & Monitoring

## Pipeline Audit Framework

Created:

* pipeline_audit_log
* pipeline_control

Tracks:

* Pipeline execution status
* Processing timestamps
* Row counts
* Success and failure information

---

## Schema Drift Detection

Created:

* schema_change_log

Detects:

* Added columns
* Removed columns
* Schema modifications

Benefits:

* Early detection of source system changes
* Protection against downstream failures

---

# Gold Layer

Business-ready analytical data marts were built for reporting and machine learning.

---

## Customer 360 Mart

### Table

```text
banklens.gold.gld_customer_360
```

Combines:

* Customer Information
* Accounts
* Products
* Loans
* Digital Activity
* Support Interactions

Provides:

* One consolidated record per customer

---

## Loan Portfolio Mart

### Table

```text
banklens.gold.gld_loan_portfolio
```

Purpose:

* Portfolio analysis
* Lending insights
* Exposure reporting

---

## Fraud Features Mart

### Table

```text
banklens.gold.gld_fraud_features
```

Purpose:

* Generate machine learning-ready fraud features

---

## Churn Features Mart

### Table

```text
banklens.gold.gld_churn_features
```

Purpose:

* Generate machine learning-ready churn features

Features include:

* Customer tenure
* Product holdings
* Account information
* Customer engagement
* Customer satisfaction indicators

---

## Executive KPI Mart

### Table

```text
banklens.gold.gld_executive_kpis
```

Provides:

* Customer KPIs
* Product KPIs
* Lending KPIs
* Engagement KPIs

---

# Dashboards

## Customer 360 Dashboard

Provides:

* Customer exploration
* Customer segmentation
* Customer insights

---

## Executive KPI Dashboard

Provides:

* Business metrics
* Operational KPIs
* Executive reporting

---

# Workflow Orchestration

Databricks Workflows were implemented to automate pipeline execution.

## Workflow

```text
bronze_load
      ↓
silver_load
      ↓
gold_load
```

## Features

* Dependency management
* Automated execution
* Scheduled processing
* Cloud-based orchestration

---

# Machine Learning Layer

## Churn Prediction Pipeline

Built a machine learning pipeline using the churn feature mart.

### Input

```text
banklens.gold.gld_churn_features
```

### Output

```text
banklens.ml.churn_predictions
```

The prediction table provides:

* Customer churn probability
* Churn classification
* Risk band assignment
* Prediction timestamp

This enables proactive customer retention analysis and customer risk monitoring.

---

# Repository Structure

```text
00_setup/
01_bronze/
02_silver/
03_gold/
04_data_quality/
05_workflows/
06_metadata/
07_ml/
99_utils/
README.md
```

---

# Current Status

## Completed

### Data Engineering

* Synthetic Banking Dataset
* Bronze Layer
* Metadata Framework
* Silver Layer
* Audit Framework
* Pipeline Control Framework
* Schema Drift Detection
* Customer 360 Mart
* Loan Portfolio Mart
* Fraud Features Mart
* Churn Features Mart
* Executive KPI Mart
* Customer Dashboard
* Executive KPI Dashboard
* Workflow Orchestration

### Machine Learning

* Churn Prediction Pipeline
* Churn Prediction Table

---

# Next Steps

## Machine Learning

* Fraud Detection Model
* Fraud Prediction Table

## Generative AI

* Natural Language Querying
* Customer Insights Assistant
* Executive Summary Generation
* AI-Powered Banking Analytics

---

# Outcome

BankLens demonstrates how modern financial institutions can combine Data Engineering, Governance, Workflow Orchestration, Business Analytics, and Machine Learning into a single unified platform.

The platform currently provides:

* End-to-End Data Pipeline
* Metadata-Driven Processing
* Governance Controls
* Business Data Marts
* Automated Workflow Orchestration
* Customer 360 Analytics
* Churn Prediction Capabilities

and serves as the foundation for future Fraud Analytics and Generative AI use cases.
