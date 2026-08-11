# ⚡ EV Charging Network Operations Analytics Platform

An end-to-end EV charging analytics platform built using **Python, PostgreSQL, SQL, dbt, and Power BI** to model and analyze charging network operations.

The project converts **state-level EV and charging infrastructure aggregates** into a synthetic operational environment containing **500K customers, ~1,600 charging stations, and ~2.1M charging sessions across 35 days**.

---

## 📌 Project Overview

Public EV datasets are largely available as **aggregated state-level data**, such as total EV registrations and operational charging stations per state, while charging networks operate through customer-level transactions, charging sessions, stations, and timestamps.

This project bridges this **macro-to-micro data gap** by using state-level reference aggregates, industry research, statistical distributions, and business assumptions to generate a synthetic operational charging environment for analytics.

The platform answers questions such as:

- How does charging demand change over time?
- Who uses public charging and how frequently?
- Which stations handle the most charging activity?
- How does station utilization vary across the network?
- How does charging demand and infrastructure utilization differ across states?

---

## 🛠 Tech Stack

| Layer | Technology |
| --- | --- |
| Reference Data | Government Sources, Kaggle, Industry Reports |
| Data Generation | Python, Pandas, NumPy |
| Database | PostgreSQL |
| Transformation | SQL, dbt |
| Semantic & BI Layer | Power BI |
| Version Control | Git & GitHub |

---

# 🔄 Data Generation & Ingestion

Reference datasets were used to establish the distributions and operating conditions for the synthetic environment.

Examples include:

- State-wise EV registrations *(aggregated state-level totals)*
- Operational public charging stations *(aggregated state-level totals)*
- EV sales by category & manufacturer
- EV vehicle specifications

### Macro-to-Micro Data Generation

The state-level reference datasets represent approximately **36 lakh EV registrations** and **12,000 operational public charging stations** across India.

The customer population was downscaled to **5 lakh synthetic customers** while preserving the state-level EV registration distribution for customers and maintain the relative demand-to-infrastructure relationship for stations.. Charging stations were proportionally downscaled to **~1,600 stations** to maintain the relative demand-to-infrastructure relationship. States that would otherwise receive zero stations after scaling were assigned a minimum of one station.

Customer, vehicle, station, and charging-session attributes were then generated using **reference distributions, industry-supported probabilities, statistical distributions, and business assumptions**.

The resulting operational environment contains:

- **500K synthetic customers**
- **~1,600 charging stations**
- **~2.1M charging sessions**
- **35 days of simulated operations**

A Python ingestion script loads the reference tables and generated operational data into PostgreSQL in a single execution.

---

# 🏗 Data Pipeline

```text
Government / Kaggle / Industry Reference Data
                    │
                    ▼
        Macro-to-Micro Data Engineering
                    │
                    ▼
          Synthetic Operational Data
       500K Customers / ~1,600 Stations
             / ~2.1M Sessions
                    │
                    ▼
          Automated Ingestion Script
                    │
                    ▼
                PostgreSQL
                    │
                    ▼
              dbt Transformation
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      Staging            Intermediate
      Models                Models
                                │
                                ▼
                           Mart Models
                                │
                                ▼
                       Power BI Semantic
                             Model
                                │
                                ▼
                           Dashboards
 ```

 
---

# 🧱 dbt Transformation Architecture

### Staging

Source and synthetic operational data are standardized through staging models, including column naming and data type normalization.

### Intermediate

Grain-specific analytical models are created for entities and operating levels such as:

* Customer
* Station
* State
* Station × Day
* Hour
* Charging Session

### Marts

Visualization-ready analytical models are created for Power BI reporting and analysis.

---

# 📊 Dashboard Pages

## 1️⃣ Network Operations Overview

Answers:

* How much charging activity does the network handle over the 35-day operating period?
* When does charging demand peak during the day?
* How is charging demand distributed across states?
* Which stations handle the highest number of charging sessions?
* How does charging activity differ between 2W and 4W vehicles?

<img width="1308" height="736" alt="image" src="https://github.com/user-attachments/assets/7eeb26bd-6399-4c33-8564-bc3e12ff7251" />

---

## 2️⃣ Customer Behavior

Answers:

* How many customers rely on public charging?
* How frequently do customers use public charging?
* Which manufacturers make up the largest share of the customer base?
* How does public charging adoption compare with home charging availability?
* At what battery SOC (State of Charge) do customers typically begin and end charging?
* What does the daily driving-distance distribution look like?

<img width="1303" height="716" alt="image" src="https://github.com/user-attachments/assets/89595769-8d5a-4f9a-a45e-fb427b622fbd" />


---

## 3️⃣ State & Station Performance

Answers:

* Which states have the highest charging infrastructure utilization?
* How does charging demand compare with the number of operational stations across states?
* Does increasing connector capacity correspond to higher average daily charging activity?
* Which charging stations deliver the highest session volume, energy, and utilization?
* How does station-level performance vary across the network?

<img width="1302" height="733" alt="image" src="https://github.com/user-attachments/assets/05858ce0-bcde-44f2-8209-ff407f5c0391" />


---

# 📐 Analytical Data Model

The project uses a layered analytical model to transform session-level operational data into reporting-ready grains.

### Core Entities

* Customer
* Charging Station
* EV Vehicle
* Charging Session

### Analytical Grains

* Charging Session
* Customer
* Station
* Station × Day
* Hour
* State

---

# 📈 Key Analytical Outputs

The platform enables analysis of:

* Charging demand trends and peak charging periods
* Customer charging behavior and frequency
* Battery SOC and daily driving patterns
* Station utilization and operational performance
* Station demand and energy delivery
* Connector capacity vs charging activity
* State-level charging demand and infrastructure utilization
* Demand vs infrastructure relationships across states

---

# ⚠ Limitations

* Operational charging data is **synthetic**, not collected from a live charging network; generation is based on reference data, industry research, statistical distributions, and business assumptions.
* Dashboard results represent the modeled **35-day operating environment**, not observed real-world charging-network performance.
* **Utilization categories are relative, not absolute:** High / Medium / Low are assigned using `NTILE(3)`, so they indicate a station's position relative to other stations in the dataset rather than whether its utilization meets an industry-defined threshold.

---
                          
