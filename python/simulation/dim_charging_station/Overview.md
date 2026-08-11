# Dim Charging Station

## Overview

`dim_charging_station` represents the **synthetic public charging network across India**, with one row per charging station.

Stations are generated from **state-level Operational PCS reference data**, with the station count **proportionally descaled relative to the 500K simulated customer population**. State coordinates are used to generate station locations, while connector counts and station types are assigned using documented assumptions.

### Columns

| Column            | Description               |
| ----------------- | ------------------------- |
| `Station_ID`      | Unique station identifier |
| `State`           | Station state             |
| `Latitude`        | Simulated latitude        |
| `Longitude`       | Simulated longitude       |
| `Connector_Count` | Number of connectors      |
| `Station_Type`    | Station classification    |

### Reference Data

* `OperationalPCS.csv` — state-level operational station totals
* `state_coordinates.csv` — state-level geographic coordinates

### Validation

* Station count
* State distribution
* Missing values
* Connector counts
* Station type mapping
