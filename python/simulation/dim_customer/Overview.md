# Dim Customer Simulation

## Overview

`dim_customer` is the customer dimension table for the EV Charging Operations & Expansion Analytics project.

It represents the simulated EV owners that form the foundation of the operational charging ecosystem. Each row corresponds to one unique customer and stores customer attributes that influence charging behaviour, infrastructure demand, and future charging sessions.

This table is generated using a combination of government datasets, public EV datasets, and documented simulation assumptions to produce a realistic customer population for downstream analytics.

---

# Objectives

The primary objectives of this simulation are to:

- Generate a realistic population of EV owners across Indian states.
- Preserve the geographical distribution of EV adoption using government registration data.
- Assign vehicles according to historical manufacturer sales patterns.
- Simulate customer mobility characteristics.
- Simulate home charging availability.
- Provide a customer dimension for generating charging sessions and business KPIs.

---

# Table Schema

| Column | Description |
|---------|-------------|
| Customer_ID | Unique identifier for each customer |
| Home_State | Customer's residential state |
| Vehicle_ID | Assigned EV owned by the customer |
| Category | Vehicle category (2W or 4W) |
| Daily_Distance_km | Simulated average daily travel distance |
| Home_Charging_Available | Indicates whether home charging is available |

---

# Reference Datasets

The simulation uses the following reference datasets.

| Dataset | Purpose |
|----------|---------|
| State-wise EV Registrations (2019–2024) | Customer distribution across states |
| EV Sales by Makers and Category (2015–2024) | Vehicle category and manufacturer probabilities |
| EV Vehicle Master | Vehicle specifications and model selection |

---

# Simulation Workflow

The customer simulation follows a sequential dependency chain.

```text
Generate Customer_ID
        │
        ▼
Assign Home_State
        │
        ▼
Assign Vehicle_ID
        │
        ▼
Derive Vehicle Category
        │
        ▼
Generate Daily_Distance_km
        │
        ▼
Generate Home_Charging_Available
```

Each step depends on information generated in previous steps, ensuring that customer attributes remain internally consistent.

---

# Data Validation

After generation, the dataset is validated to ensure data quality.

Validation includes:

- Missing values
- Duplicate customer IDs
- Duplicate rows
- State distribution validation
- Vehicle category distribution validation
- Daily distance validation
- Home charging probability validation


---
