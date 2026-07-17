# EV Infrastructure Investment Analysis

An end-to-end **Analytics Engineering** project that helps identify
which Indian states should be prioritized for EV charging infrastructure
investment using government datasets, simulated operational data,
PostgreSQL, dbt, and Power BI.

------------------------------------------------------------------------

# Business Problem

The Government of India has allocated a **₹1,000 crore** budget to
expand EV charging infrastructure.

Since the budget cannot fund every state equally, stakeholders need a
data-driven approach to identify where investment will have the greatest
impact.

Rather than fabricating city-level data, this project intentionally
performs **state-level analysis** because publicly available datasets
are consistently available at the state granularity.

The final deliverable is a **State Expansion Priority Score** that
supports infrastructure investment decisions.

------------------------------------------------------------------------

# Project Objective

Build an end-to-end analytics platform capable of:

-   Simulating a realistic EV charging ecosystem
-   Engineering an analytical database
-   Transforming raw operational data into business-ready models
-   Calculating infrastructure KPIs
-   Recommending investment priorities for Indian states

------------------------------------------------------------------------

# Technology Stack

| Category | Tools |
|----------|----------|
|   Programming       |     Python, SQL     |
|    Database      |      PostgreSQL    |
|       Transformation   |    dbt      |
| Visualization   | Power BI   |
| Version Control |  Git, GitHub |

------------------------------------------------------------------------

# Project Architecture

``` text
Reference Datasets
        │
        ├── Government Data
        │
        ├── Public Reference Data
                │
                ▼
      Python Simulation Engine
                │
      ┌─────────┼──────────┐
      ▼         ▼          ▼
dim_customer  dim_charging_station  fact_charging_events
                │
                ▼
      Python Data Validation
                │
                ▼
          PostgreSQL (Raw)
                │
                ▼
              dbt Models
      (staging → intermediate → marts)
                │
                ▼
        Business KPI Calculation
                │
                ▼
          Power BI Dashboard
                │
                ▼
 State Expansion Priority Score
```

------------------------------------------------------------------------

# Data Sources

## Government Data

-   State-wise EV Registrations (2019--2024)
-   State Population
-   State Coordinates

## Reference Data

-   Operational Public Charging Stations
-   EV Sales by Manufacturer
-   EV Vehicle Master

## Simulated Data

Python generates:

-   Dim Customer
-   Dim Charging Station
-   Fact Charging Events

------------------------------------------------------------------------

# Planned Data Model

## Dimension Tables

-   Dim Customer
-   Dim Charging Station
-   Dim Vehicle
-   Dim Date
-   Dim State

## Fact Tables

-   Fact Charging Events
-   Fact Daily Charging Demand (Derived)

------------------------------------------------------------------------

# Execution Flow

``` text
python main.py
      │
      ▼
Load Reference Data
      ▼
Generate Simulation
      ▼
Validate Data
      ▼
Load into PostgreSQL
      ▼
dbt run
      ▼
dbt test
      ▼
Power BI
```

------------------------------------------------------------------------

# Key Business Metrics

-   EV Penetration
-   Chargers per 1,000 EVs
-   Charging Demand
-   Charger Utilization
-   Infrastructure Gap
-   State Readiness Score
-   State Expansion Priority Score

------------------------------------------------------------------------

# Dashboard

The Power BI dashboard will include:

-   Executive Summary
-   State EV Adoption
-   Charging Infrastructure
-   Infrastructure Gap Analysis
-   Charging Demand Analysis
-   State Priority Ranking
-   ₹1,000 Crore Investment Recommendation

------------------------------------------------------------------------

# Repository Structure

``` text
.
├── data/
│   ├── reference/
│   └── simulated/
├── python/
│   ├── simulation/
│   ├── validation/
│   └── loaders/
├── postgres/
├── dbt/
├── powerbi/
├── docs/
├── images/
├── main.py
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# Project Status

-   ✅ Business Problem Finalized
-   ✅ Architecture Finalized
-   ✅ Dataset Collection Completed
-   🚧 Simulation Design In Progress
-   ⏳ Python Simulation
-   ⏳ PostgreSQL Integration
-   ⏳ dbt Models
-   ⏳ Power BI Dashboard

------------------------------------------------------------------------

# License

This project is intended for educational and portfolio purposes.
