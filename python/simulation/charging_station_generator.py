import pandas as pd
import numpy as np

from python.utils.file_paths import *

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

print(comparison_df)

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





