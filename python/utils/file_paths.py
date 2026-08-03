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
OPERATIONAL_PCS_PATH=REFERENCE_FOLDER/"OperationalPC.csv"
STATE_COORDINATES_PATH=REFERENCE_FOLDER/"state_coordinates.csv"
STATE_POPULATION_PATH = REFERENCE_FOLDER/"state_population.csv" 

# Simulated Dataset paths
DIM_CUSTOMER = SIMULATED_FOLDER/"dim_customer.csv"
DIM_CHARGING_STATION = SIMULATED_FOLDER/"dim_charging_station.csv"
FACT_CHARGING_SESSIONS = SIMULATED_FOLDER/"fact_charging_sessions.csv"

# RAW tables dictionary
RAW_TABLES = {
    "state_ev_registrations": STATE_EV_REGISTRATIONS,
    "ev_sales_by_makers": EV_SALES_BY_CAT_AND_MAKERS,
    "ev_vehicle_master": EV_VEHICLE_MASTER,
    "operational_pcs": OPERATIONAL_PCS_PATH,
    "state_coordinates": STATE_COORDINATES_PATH,
    "state_population": STATE_POPULATION_PATH,

    "dim_customer": DIM_CUSTOMER,
    "dim_charging_station": DIM_CHARGING_STATION,
    "fact_charging_sessions": FACT_CHARGING_SESSIONS
}


