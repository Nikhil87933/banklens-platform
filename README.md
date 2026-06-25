# 🏦 BankLens – Enterprise Banking Lakehouse Platform

An end-to-end banking analytics platform built on the Databricks Lakehouse, demonstrating enterprise-grade data engineering, machine learning, and natural language business analytics.

---

## 🚀 Overview

BankLens simulates a modern banking data platform using the Medallion Architecture (Bronze, Silver, Gold). It ingests banking data, applies data quality and governance, builds curated business datasets, trains machine learning models, and enables business users to query data using natural language.

---

## 🛠️ Tech Stack

### Data Engineering
- Databricks
- Apache Spark (PySpark)
- Delta Lake
- Unity Catalog
- SQL

### Machine Learning
- Python
- Scikit-learn

### AI Copilot
- Ollama
- Qwen 2.5
- Streamlit
- Databricks SQL Connector

### Development
- VS Code
- Ubuntu (WSL)
- Git
- GitHub
- CI/CD
- GitHub Actions

---

## ✨ Key Features

- Medallion Lakehouse Architecture
- Metadata-Driven ETL Pipelines
- Data Quality & Audit Framework
- Schema Standardization
- Gold Business Data Models
- Customer Churn Prediction
- Fraud Detection Foundation
- Natural Language Analytics using AI Copilot

---

## 🏗️ Architecture

```
Raw Banking Data
        │
        ▼
 Bronze Layer
        │
        ▼
 Silver Layer
        │
        ▼
 Gold Layer
   ┌──────────────┐
   │              │
   ▼              ▼
Machine Learning  AI Copilot
   │              │
   └──────┬───────┘
          ▼
 Business Insights
```

---

## 📂 Project Structure

```
00_setup/
01_bronze/
02_silver/
03_gold/
04_data_quality/
05_workflows/
07_ml/
08_ai/
```

---

## 💬 Sample Questions

- How many customers do we have?
- How many HIGH risk customers do we have?
- How many customers are predicted to churn?
- What is the total outstanding loan balance?
- What is the average NPS score?

---

## 🎥 Demo

*A short project demo video will be added soon.*

---

## 📌 Future Enhancements

- Retrieval-Augmented Generation (RAG)
- Agentic AI Workflows
- Real-Time Data Streaming
- Interactive Executive Dashboard

---

## 👨‍💻 Author

**Nikhil Chamle**
