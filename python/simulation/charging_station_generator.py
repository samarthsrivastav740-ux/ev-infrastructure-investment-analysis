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




