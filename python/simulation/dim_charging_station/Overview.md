# Dim Charging Station

## Overview

`dim_charging_station` is the charging station dimension table for the EV Charging Operations & Expansion Analytics project.

It represents the simulated public EV charging infrastructure across India. Each row corresponds to one charging station and stores its location, connector capacity, and station classification.

The table is generated using operational charging station data, state coordinates, and documented engineering assumptions to create a realistic charging network for downstream charging session simulation.

---

# Objectives

The primary objectives of this simulation are to:

- Generate a realistic charging station network across Indian states.
- Preserve the existing distribution of operational charging stations.
- Assign realistic geographic locations to each station.
- Simulate charging capacity using connector counts.
- Classify stations based on charging capacity.
- Provide the charging infrastructure required for charging session simulation.


---

# Table Schema

| Column | Description |
|---------|-------------|
| Station_ID | Unique identifier for each charging station |
| State | State where the charging station is located |
| Latitude | Simulated station latitude |
| Longitude | Simulated station longitude |
| Connector_Count | Number of charging connectors available |
| Station_Type | Station classification based on connector capacity |

---

# Reference Datasets

| Dataset | Purpose |
|----------|---------|
| OperationalPCS.csv | Existing charging station distribution across states |
| state_coordinates.csv | Reference geographic coordinates for each state |

---

# Simulation Workflow

```text
Generate Station_ID
        │
        ▼
Assign State
        │
        ▼
Generate Latitude & Longitude
        │
        ▼
Generate Connector_Count
        │
        ▼
Generate Station_Type
```

---

# Data Validation

Validation includes:

- Missing values
- Station count validation
- State distribution validation
- Connector count validation
- Station type validation
- Connector count mapping validation
