import pandas as pd
import numpy as np

from python.utils.file_paths import *

#==========================================
# Random Seed
#==========================================

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)

# ==========================================================
# Load Reference Datasets
# ==========================================================

operational_pcs = pd.read_csv(OPERATIONAL_PCS_PATH)

state_coordinates = pd.read_csv(STATE_COORDINATES_PATH)

#==========================================
# Column 1 - Station_ID
#==========================================

def generate_station_ids(total_stations):
    """
    Generate Station_ID.

    Example:
        ST000001
        ST000002
        ST000003
    """

    # Create an empty list to store Station IDs
    station_ids=[]

    # Generate one Station_ID at a time
    for i in range(1,total_stations+1):

        # Format Station_ID with leading zeros
        station_id=f"ST{i:06d}"

        # Add generated ID to the list
        station_ids.append(station_id)

    # Return completed list
    return station_ids

#==========================================
# Create Charging Station DataFrame
#==========================================

charging_station_df=pd.DataFrame()

# Total operational charging stations
Total_Stations = operational_pcs[
    "No. of Operational PCS"
].sum()

# Generate Station_ID column
charging_station_df["Station_ID"] = generate_station_ids(
    Total_Stations
)

#==========================================
# Validation - Station_ID
#=========================================

print("\nStation_ID Validation")

# Check total number of stations
print(
    "Total Stations:",
    len(charging_station_df)
)

# Check for duplicate Station_IDs
print(
    "Duplicate Station_IDs:",
    charging_station_df["Station_ID"]
    .isnull()
    .sum()
)

#==========================================
# Validation - Total Station Count
#==========================================\

print("\nTotal Station Count Validation")

print(
    "Operational PCS:",
    Total_Stations
)

print(
    "Generated Station_IDs:",
    len(charging_station_df)
)

if len(charging_station_df) == Total_Stations:
    print("Station count validation PASSED")
else:
    print("Station count validation FAILED")

#==========================================
# Column 2 - State
#==========================================

# Required columns
operational_pcs = operational_pcs[
    [
        "State",
        "No. of Operational PCS"
    ]
]

def generate_states(operational_pcs):
    """
    Generate State for every charging station.

    Each state is repeated according to its
    number of operational charging stations.
    """

    # Create empty list
    states = []

    # Generate stations for every state
    for _, row in operational_pcs.iterrows():

        # Get state name
        state = row["State"]

        # Get number of stations
        station_count = int(
            row["No. of Operational PCS"]
        )

        # Add state once for every station
        for i in range(station_count):

            states.append(state)

    # Return completed list
    return states

# Generate State column
charging_station_df["State"] = generate_states(
    operational_pcs
)

#==========================================
# Validation - State
#==========================================

print("\nState Validation")

# Missing values
print(
    "Missing States:",
    charging_station_df["State"].isnull().sum()
)

# Compare generated counts with reference
generated_distribution = (
    charging_station_df["State"]
    .value_counts()
    .sort_index()
)

reference_distribution = (
    operational_pcs
    .set_index("State")["No. of Operational PCS"]
    .sort_index()
)

comparison_df = pd.DataFrame({
    "Reference_Stations": reference_distribution,
    "Generated_Stations": generated_distribution
})

comparison_df["Difference"] = (
    comparison_df["Generated_Stations"]
    -
    comparison_df["Reference_Stations"]
)

print(comparison_df.head(5))

# Validation
if (comparison_df["Difference"] == 0).all():
    print("\nState validation PASSED")
else:
    print("\nState validation FAILED")

# Save validation report
comparison_df.to_csv(
    "data/simulated/station_state_validation.csv",
    index=True
)

#==========================================
# Column 3 & 4 - Latitude and Longitude
#==========================================

# Keep only required columns
state_coordinates = state_coordinates[
    [
        "State/Union Territory",
        "Latitude",
        "Longitude"
    ]
]

# Rename state column
state_coordinates = state_coordinates.rename(
    columns={
        "State/Union Territory": "State"
    }
)

#==========================================
# Standardize Different State Names
#==========================================

state_mapping = {

    "Andaman and Nicobar Islands":
        "Andaman & Nicobar",

    "Dadra and Nagar Haveli and Daman and Diu":
        "D&D and DNH",

    "Puducherry":
    "Pondicherry"

    
}

# Replace state names with standardized names
state_coordinates["State"] = (
    state_coordinates["State"]
    .replace(state_mapping)
)

# Maximum random geographic offset
# around the state's reference coordinate.
# Engineering assumption.
MAX_DISTANCE_OFFSET = 0.20

def generate_station_locations(
    charging_station_df,
    state_coordinates       
):
    """
    Generate Latitude and Longitude for every
    charging station.

    Each station is placed near the state's
    reference coordinate by applying a small
    random spatial offset.
    """

    # Create empty list
    latitudes = []
    longitudes = []

    # Generate location for every station
    for _, row in charging_station_df.iterrows():

        # Get station state
        state = row["State"]

        # Get reference coordinate
        reference_location = (
            state_coordinates[
                state_coordinates["State"] == state
            ]
            .iloc[0]
        )

        reference_latitude = reference_location["Latitude"]
        reference_longitude = reference_location["Longitude"]

        #==========================================
        # Generate One Geographic Location
        #==========================================

        # Random direction (0° to 360°)
        direction = np.random.uniform(
            0,
            2* np.pi
        )

        # Random distance from the reference point
        distance = np.random.uniform(
            0,
            MAX_DISTANCE_OFFSET
        )

        # Convert polar coordinates to
        # latitude and longitude offsets.
        latitude_offset = (
            distance * np.cos(direction)
        )

        longitude_offset = (
            distance * np.sin(direction)
        )

        # Generate simulated location
        latitude = (
            reference_latitude
            + latitude_offset
        )

        longitude = (
            reference_longitude
            + longitude_offset
        )

        # State cooridnates
        latitudes.append(
            round(latitude,6)
        )

        longitudes.append(
            round(longitude,6)
        )

    # Return both columns
    return latitudes,longitudes

# Generate Latitude and Longitude
latitudes, longitudes = generate_station_locations(
    charging_station_df,
    state_coordinates
)

charging_station_df["Latitude"] = latitudes
charging_station_df["Longitude"] = longitudes

print(charging_station_df.head(5))

#==========================================
# Column 5 - Connector_Count
#==========================================

#==========================================
# Simulation Parameters
#==========================================

# Possible connector capacities per station
CONNECTOR_OPTIONS = [
    2,
    4,
    6,
    8
]

# Engineering assumptions informed by
# Indian public charging infrastructure.

CONNECTOR_CAPACITY_PROBABILITIES = [
    0.75,
    0.18,
    0.05,
    0.02
]

def generate_connector_count(total_stations):
    """
    Generate Connector_Count for every charging station.

    Connector_Count represents the maximum number
    of vehicles that can charge simultaneously.
    """
    connector_counts = []

    # Generate one connector capacity
    # for every charging station
    for i in range(total_stations):

        connector_count = np.random.choice(
            CONNECTOR_OPTIONS,
            p=CONNECTOR_CAPACITY_PROBABILITIES
        )

        connector_counts.append(
            connector_count
        )

    return connector_counts

# Generate Connector_Count column
charging_station_df["Connector_Count"] = generate_connector_count(
    Total_Stations
)

#==========================================
# Validation - Connector_Count
#==========================================

print("\nConnector_Count Validation")

# Missing values
print(
    "Missing Connector_Count:",
    charging_station_df["Connector_Count"]
    .isnull()
    .sum()
)

# Connector distribution
connector_distribution = (
    charging_station_df["Connector_Count"]
    .value_counts(normalize = True)
    .sort_index()
    *100
)

print("\nGenerated Distribution (%)")
print(
    connector_distribution.round(2)
)

# Validate connector categories
invalid_connectors = (
    ~charging_station_df["Connector_Count"]
    .isin(CONNECTOR_OPTIONS)
).sum()

print(
    "\nInvalid Connector_Count Values:",
    invalid_connectors
)

# Comparing expected and generated distribution
expected_distribution = pd.Series(
    {
        2: 75.0,
        4: 18.0,
        6: 5.0,
        8: 2.0
    },
    name = "Expected (%)"
)

generated_distribution = (
    charging_station_df["Connector_Count"]
    .value_counts(normalize = True)
    .sort_index()
    *100
).rename("Generated (%)")

comparison_df = pd.concat(
    [
        expected_distribution,
        generated_distribution
    ],
    axis = 1
)

comparison_df["Difference"] = (
    comparison_df["Generated (%)"]
    - comparison_df["Expected (%)"]
)

print("\nConnector Count Distribution")
print(comparison_df.round(2))

# Save validation report
comparison_df.to_csv(
    "data/simulated/connector_count_validation.csv",
    index=True
)

#==========================================
# Column 6 - Station_Type
#==========================================

def generate_station_type(charging_station_df):
    """
    Generate Station_Type based on Connector_Count.

    Standard : 2 or 4 connectors
    Hub      : 6 or 8 connectors
    """

    # Create empty list
    station_types = []

    # Generate Station_Type
    for _, row in charging_station_df.iterrows():

        connector_count = row["Connector_Count"]

        if connector_count <= 4:
            station_type = "Standard"
        else:
            station_type = "Hub"

        station_types.append(station_type)

    # Return completed list
    return station_types

# Generate Station_Type column
charging_station_df["Station_Type"] =  generate_station_type(
    charging_station_df
)

#==========================================
# Validation - Station_Type
#==========================================

print("\nStation_Type Validation")

# Missing values
print(
    "Missing Station_Type:",
    charging_station_df["Station_Type"]
    .isnull()
    .sum()
)

# Distribution
station_type_distribution = (
    charging_station_df["Station_Type"]
    .value_counts()
)

print("\nStation Type Distribution")
print(station_type_distribution)

# Check valid categories
invalid_station_types = (
    ~charging_station_df["Station_Type"]
    .isin(["Standard", "Hub"])
).sum()

print(
    "\nInvalid Station_Type Values:",
    invalid_station_types
)

#==========================================
# Validation - Connector Count Mapping
#==========================================

invalid_mapping = charging_station_df[
    (
        (charging_station_df["Connector_Count"] <= 4)
        &
        (charging_station_df["Station_Type"] != "Standard")
    )
    |
    (
        (charging_station_df["Connector_Count"] >= 6)
        &
        (charging_station_df["Station_Type"] != "Hub")
    )
]

print(
    "\nInvalid Connector Count Mapping:",
    len(invalid_mapping)
)

if len(invalid_mapping) == 0:
    print("Station_Type validation PASSED")
else:
    print("Station_Type validation FAILED")

#==========================================
# Save dim_charging_station
#==========================================

# Export dim_customer
charging_station_df.to_csv(
    "data/simulated/dim_charging_station.csv",
    index=False
)

print("\ndim_charging_station.csv generated successfully.")


