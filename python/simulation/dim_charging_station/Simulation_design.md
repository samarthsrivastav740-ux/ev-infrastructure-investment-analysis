# Dim Charging Station Simulation Design

This document describes the design methodology used to generate each column in the `dim_charging_station` table. Every column is generated using either reference datasets or documented engineering assumptions to create a realistic public EV charging infrastructure. :contentReference[oaicite:0]{index=0}

# 1. Station_ID

### Purpose

Uniquely identifies every simulated charging station. It serves as the primary key of the `dim_charging_station` table and is used to link charging stations with charging sessions in downstream fact tables.

### Reference Dataset

- `OperationalPCS.csv`

### Generation Method

- Calculate the total number of operational charging stations from the reference dataset.
- Generate sequential station IDs.
- Prefix each ID with `ST`.
- Pad the numeric portion with leading zeros to maintain a fixed-length format.

Example:

ST000001  
ST000002  
ST000003

### Design Decision

The total number of simulated charging stations matches the total operational charging stations reported in the reference dataset. Sequential IDs provide deterministic and unique identifiers suitable for simulation.

### Validation

- No missing values
- No duplicate Station_IDs
- Total generated Station_IDs equals the total operational charging stations

---

# 2. State

### Purpose

Represents the state in which each charging station is located. This preserves the geographical distribution of India's existing public charging infrastructure.

### Reference Dataset

- `OperationalPCS.csv`

### Data Preparation

- Retain only the `State` and `No. of Operational PCS` columns.

### Generation Method

Assign charging stations to each state by repeating the state name according to its reported number of operational charging stations.

Example:

If Delhi has 120 operational charging stations, then 120 Station_IDs are assigned to Delhi.

### Design Decision

The simulation preserves the existing state-wise charging station distribution instead of generating stations using random probabilities.

### Validation

- No missing values
- Compare generated station count with the reference count for every state

---

# 3. Latitude

### Purpose

Represents the simulated latitude of each charging station.

### Reference Dataset

- `state_coordinates.csv`

### Generation Method

For each charging station:

- Retrieve the reference latitude of its assigned state.
- Generate a random geographic offset within a predefined maximum distance.
- Apply the offset to the reference latitude.

### Design Decision

A small random offset prevents multiple charging stations within the same state from sharing identical coordinates while keeping them close to the state's reference location.

### Validation

- No missing values
- One latitude generated for every charging station

---

# 4. Longitude

### Purpose

Represents the simulated longitude of each charging station.

### Reference Dataset

- `state_coordinates.csv`

### Generation Method

For each charging station:

- Retrieve the reference longitude of its assigned state.
- Generate the same random geographic offset used for latitude.
- Apply the offset to the reference longitude.

### Design Decision

Latitude and longitude are generated together to simulate realistic charging station locations around each state's reference coordinate.

### Validation

- No missing values
- One longitude generated for every charging station

---

# 5. Connector_Count

### Purpose

Represents the number of charging connectors available at a charging station. This determines the station's simultaneous charging capacity.

### Generation Method

Generate connector counts using weighted random sampling from the following options:

| Connector Count | Probability |
|-----------------|------------:|
| 2 | 75% |
| 4 | 18% |
| 6 | 5% |
| 8 | 2% |

### Design Decision

Detailed connector-count distributions for Indian public charging stations were not available. The probabilities were introduced as engineering assumptions based on the observation that smaller charging stations are significantly more common than large charging hubs.

### Validation

- No missing values
- All connector counts belong to the valid set {2, 4, 6, 8}
- Compare simulated distribution with the expected probabilities

---

# 6. Station_Type

### Purpose

Classifies charging stations based on their charging capacity.

### Generation Method

Assign station types according to the connector count:

| Connector Count | Station Type |
|-----------------|--------------|
| 2 or 4 | Standard |
| 6 or 8 | Hub |

### Design Decision

Instead of modeling charger technology (AC/DC), stations are classified by capacity. This provides a simple representation of infrastructure scale while remaining sufficient for downstream charging session simulation.

### Validation

- No missing values
- Only valid station types (`Standard`, `Hub`)
- Verify every station type correctly matches its connector count