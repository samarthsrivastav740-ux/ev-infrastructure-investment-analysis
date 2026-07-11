# EV Infrastructure Investment Analysis

An end-to-end Analytics Engineering project that helps identify which Indian states should be prioritized for EV charging infrastructure investment using government datasets, simulated operational data, and a modern ELT pipeline.

---

## Business Problem

The Government of India has allocated a limited budget of **₹1,000 crore** to expand the country's electric vehicle (EV) charging infrastructure.

Since the budget cannot support every state equally, decision-makers need a data-driven approach to determine where new investments will generate the greatest impact.

This project builds an analytics platform that evaluates EV adoption, existing charging infrastructure, and projected charging demand to rank Indian states based on infrastructure investment priority.

---

## Project Objective

Build an automated data platform capable of answering questions such as:

- Which states have the largest EV infrastructure gap?
- Where is charging demand expected to exceed existing capacity?
- Which states should receive priority investment?
- How can charging companies and policymakers allocate resources more effectively?

The final output is a **State Expansion Priority Score** that supports strategic investment decisions.

---

## Why State-Level Analysis?

Initially, this project aimed to recommend investments at the city level.

However, after evaluating publicly available datasets, it became clear that reliable city-level EV registration and charging infrastructure data was not consistently available.

Rather than generating artificial city-level metrics, the project intentionally operates at the **state level** to maintain data integrity and produce reliable recommendations.

---

## Stakeholders

### Government

- Allocate infrastructure funding efficiently
- Identify states requiring immediate investment

### Charging Network Companies

Examples:
- Tata Power EZ Charge
- Statiq
- ChargeZone
- Ather Grid

Use the analysis to identify underserved markets with strong growth potential.

### Investors

- Evaluate expected charging demand
- Prioritize regions with higher infrastructure utilization potential

### EV Manufacturers

- Assess infrastructure readiness before expanding into new markets

---

## Technology Stack

| Category | Tools |
|----------|------|
| Programming Languages | Python, SQL |
| Cloud Platform | Google Cloud Platform (GCS, BigQuery) |
| Transformation | dbt |
| Orchestration | Apache Airflow |
| BI & Visualization | Power BI |
| Version Control | Git & GitHub |

---

## Project Architecture

```
Reference Datasets
        │
        ▼
Python Data Simulation
        │
        ▼
Google Cloud Storage
        │
        ▼
BigQuery (RAW)
        │
        ▼
dbt Transformation
        │
        ▼
Analytics Mart
        │
        ▼
Power BI Dashboard
```

---

## Data Sources

### Government Data

- state wise ev registrations 2019-2024
- state population
- state coordinates

### Publicly available Reference Datasets (kaggle and other websites)

- ev_vehicle_master
- ev_sales_by_makers_and_cat_15-24
- OperationalPC
- ev_cat_01-24

### Simulated Data

Python is used to generate realistic operational charging events, enabling analysis at production-like scale.

---

## Planned Data Model

### Fact Tables

- Fact Charging Events
- Fact Daily Charging Demand

### Dimension Tables

- Dim State
- Dim Vehicle
- Dim Charging Station
- Dim Date
- Dim Customer

---

## Key Business Metrics

The analytics layer will calculate metrics including:

- EV Penetration
- Chargers per 1,000 EVs
- Charging Demand
- Infrastructure Gap
- Charger Utilization
- State Expansion Priority Score

---

## Dashboard

The Power BI dashboard will include:

- Executive Summary
- State-wise EV Adoption
- Charging Infrastructure Overview
- Infrastructure Gap Analysis
- State Priority Ranking
- Investment Recommendation Dashboard

---

## Repository Structure

```
.
├── airflow/
├── data/
├── dbt/
├── docs/
├── images/
├── powerbi/
├── python/
├── sql/
├── README.md
└── requirements.txt
```

---

## Project Status

Current Stage:

- Business Problem Defined
- Architecture Finalized
- Dataset Collection Completed
- Data Simulation (In Progress)
- ELT Pipeline (Upcoming)
- dbt Models (Upcoming)
- Power BI Dashboard (Upcoming)


---

## License

This project is intended for educational and portfolio purposes.