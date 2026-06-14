# Advanced Analytics & AI Layer

After establishing the Bronze, Silver, and Gold data platform, the next phase focuses on machine learning and generative AI capabilities.

The Gold marts created in this project serve as the foundation for analytical and AI workloads.

---

## Churn Prediction Model

Source:

banklens.gold.gld_churn_features

Objective:

Predict customers likely to leave the bank.

Potential Algorithms:

- Logistic Regression
- Random Forest
- XGBoost

Business Value:

- Customer retention
- Targeted campaigns
- Reduced customer attrition

---

## Fraud Detection Model

Source:

banklens.gold.gld_fraud_features

Objective:

Identify suspicious customer behaviour and potential fraud.

Potential Algorithms:

- Random Forest
- XGBoost
- Isolation Forest
- Autoencoders

Business Value:

- Fraud prevention
- Reduced financial losses
- Improved risk monitoring

---

## Customer Segmentation

Source:

banklens.gold.gld_customer_360

Objective:

Group customers into behavioural segments.

Potential Algorithms:

- K-Means
- Hierarchical Clustering

Business Value:

- Personalised offers
- Marketing optimisation
- Better customer understanding

---

## Loan Risk Analytics

Source:

banklens.gold.gld_loan_portfolio

Objective:

Assess portfolio concentration and customer risk.

Potential Use Cases:

- Risk scoring
- Exposure analysis
- Portfolio monitoring

Business Value:

- Better lending decisions
- Improved risk management

---

# LLM & Generative AI Layer

The final phase introduces Large Language Models to provide natural language access to banking insights.

---

## Banking Insight Assistant

Source:

Customer 360
Loan Portfolio
Fraud Features
Executive KPI Mart

Objective:

Allow business users to ask questions in plain English.

Examples:

- Which customers have the highest balances?
- Show customers with multiple loans.
- Which states have the largest loan exposure?
- How many customers are at risk of churn?

Business Value:

- Self-service analytics
- Reduced dependency on SQL
- Faster decision making

---

## Executive Copilot

Objective:

Generate management summaries from Gold data.

Examples:

- Daily executive briefing
- Loan portfolio summary
- Customer growth summary
- Digital banking adoption trends

Business Value:

- Faster reporting
- Executive decision support

---

## Retrieval-Augmented Generation (RAG)

Future Integration:

Combine structured banking data with:

- Policies
- Product documentation
- Compliance manuals
- Operational procedures

Potential Capabilities:

- Policy Q&A
- Compliance assistance
- Knowledge retrieval

Business Value:

- Faster information access
- Improved operational efficiency

## Workflow Orchestration

The platform follows a dependency-driven DAG.

Bronze Ingestion
↓
Silver Standardisation
↓
Gold Data Marts
↓
Dashboards

Execution is controlled through Databricks Workflows.