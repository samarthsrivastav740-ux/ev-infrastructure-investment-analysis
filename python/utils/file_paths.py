from pathlib import Path

# Project Root
PROJECT_ROOT=Path(__file__).resolve().parents[2]

# Data folder
DATA_FOLDER=PROJECT_ROOT/"data"

# Reference Data Folder
REFERENCE_FOLDER=DATA_FOLDER/"reference"

# Simulated Data Folder
SIMULATED_FOLDER=DATA_FOLDER/"simulated"

# Reference Dataset paths
STATE_EV_REGISTRATIONS=REFERENCE_FOLDER/"state_wise_ev_registrations_2019-2024.csv"
EV_SALES_BY_CAT_AND_MAKERS=REFERENCE_FOLDER/"ev_sales_by_makers_and_cat_15-24.csv"
EV_VEHICLE_MASTER=REFERENCE_FOLDER/"ev_vehicle_master.csv"


