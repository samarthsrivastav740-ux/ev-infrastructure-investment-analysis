# Project Reference Tables

This folder contains the reference data tables used throughout the project.

The tables were collected from public government sources, Kaggle, and manufacturer websites. They provide the foundational data required to simulate an EV charging ecosystem and support the downstream analytics pipeline.

Minor preprocessing (such as removing empty columns, standardizing column names, and formatting) was performed before the tables were used in the project.

---

# Data Sources

| Source | Purpose |
|---------|---------|
| data.gov.in | Official government statistics |
| Kaggle (Vahan-based datasets) | EV registrations, manufacturers, charging infrastructure |
| Manufacturer Websites | EV vehicle specifications |

---

# Reference Tables

## Government Reference Tables

| Table | Description | Purpose in Project |
|----------|-------------|------|
| state_wise_ev_registrations_2019_2024.csv | State-wise EV registrations and EV share | Customer distribution & state-level metrics |
| state_population.csv | Population estimates for Indian states | Population-normalized KPIs |
| state_coordinates.csv | Latitude and longitude of Indian states | Charging station location generation & maps |

---

## Public Reference Tables

| Table | Description | Purpose in Project |
|----------|-------------|------|
| ev_vehicle_master.csv | EV specifications including battery capacity, range and charging power | Vehicle simulation |
| ev_sales_by_makers_and_cat_15_24.csv | Manufacturer-wise EV sales by year | Manufacturer selection probabilities |
| OperationalPC.csv | Operational public charging stations by state | Charging station generation |
| ev_cat_01_24.csv | Historical EV registrations by vehicle category | Optional registration year distribution |

---

# Notes

- Government reference tables are treated as the primary source for state-level analysis.
- Public reference tables (Kaggle and other sources) are used as reference data where official operational data is unavailable.
- The `ev_vehicle_master` table was created by consolidating publicly available EV specifications from manufacturer websites because the reference datasets did not include detailed vehicle specifications required for simulation.
- The reference tables have undergone minimal preprocessing (e.g., removal of empty columns, standardization of column names, and minor formatting fixes) to improve consistency before being used in the simulation pipeline.
- All business transformations, feature engineering, and simulation logic are implemented programmatically in the subsequent stages of the project.