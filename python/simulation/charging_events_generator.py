# ==========================================
# Third Party Libraries
# ==========================================

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# ==========================================
# Project Files
# ==========================================

from python.utils.file_paths import (
    DIM_CUSTOMER,
    DIM_CHARGING_STATION,
    EV_VEHICLE_MASTER,
    FACT_CHARGING_SESSIONS
)

# ==========================================
# Load Reference Tables
# ==========================================

# Load simulated customer dimension
dim_customer = pd.read_csv(DIM_CUSTOMER)

# Load simulated charging station dimension
dim_charging_station = pd.read_csv(DIM_CHARGING_STATION)

# Load EV vehicle specifications
ev_vehicle_master = pd.read_csv(EV_VEHICLE_MASTER)

# ==========================================
# Project Configuration
# ==========================================

# Set development mode
DEV_MODE = False

if DEV_MODE:

    # Small dataset for faster debugging
    TOTAL_CUSTOMERS = 500
    SIMULATION_DAYS = 7

else:

    # Final production dataset
    TOTAL_CUSTOMERS = 500000
    SIMULATION_DAYS = 35

# Average charging rate assumption (kW)
# A constant charging rate is assumed for the simulation.
# This simplifies charging duration calculations by avoiding charger-type
# (AC/DC) specific modeling.
AVERAGE_CHARGING_RATE_KW = 30

# Simulation start date
SIMULATION_START_DATE = datetime(2026, 6, 29)

# Random seed for reproducibility
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ==========================================
# Home Charging Behaviour
# ==========================================

# Customers with home charging do not
# always use public charging stations.

HOME_CHARGING_SKIP_PROBABILITY = 0.75

# ==========================================
# Filter Customers
# ==========================================

# Use only the required number of customers
# This keeps the same code for both development
# and production runs.

dim_customer = dim_customer.head(TOTAL_CUSTOMERS).copy()


# ==========================================
# Calculate Expected Charging Interval
# ==========================================

# Attach vehicle information to each customer.
# This allows us to access vehicle specifications
# directly from the customer table.

dim_customer = dim_customer.merge(
    ev_vehicle_master[["Vehicle_ID","Estimated_Range_km"]],
    on = "Vehicle_ID",
    how = "left"
)

# Estimate how many days a customer can drive
# before requiring a charging session.

dim_customer["Expected_Charging_Interval"] = (
    dim_customer["Estimated_Range_km"]/
    dim_customer["Daily_Distance_km"]
)

# ==========================================
# Initialize Charging Countdown
# ==========================================

# Every customer starts with a different point
# in their charging cycle. This prevents all
# customers from charging on the same day.

dim_customer["Days_Until_Next_Charge"] = (
    dim_customer["Expected_Charging_Interval"]
    .apply(lambda x: random.randint(1, max(1, round(x))))
)


# ==========================================
# Initialize Simulation
# ==========================================

# Session IDs will be generated sequentially
# whenever a charging session occurs.

session_counter = 1


# Store every simulated charging session.

sessions = []

# ==========================================
# Main Simulation Loop
# ==========================================

# Simulate one day at a time.

for day in range(SIMULATION_DAYS):

    current_date = SIMULATION_START_DATE + timedelta(days=day)

    # Process every customer for the current day.

    for index, customer in dim_customer.iterrows():

        # Reduce the remaining days until
        # the next charging session.

        remaining_days = customer["Days_Until_Next_Charge"] - 1
        dim_customer.at[index, "Days_Until_Next_Charge"] = remaining_days

        # Skip customers who do not require
        # charging today.

        if remaining_days > 0 :
            continue

        # ==========================================
        # Customer requires charging today
        # Generate charging session here...
        # ==========================================

        # Customers with home charging usually
        # charge at home instead of using a
        # public charging station.

        if customer["Home_Charging_Available"]:

            if random.random() < HOME_CHARGING_SKIP_PROBABILITY:

                # Reset the charging countdown.

                new_interval = max(
                    1,
                    round(
                        np.random.normal(
                            loc=customer["Expected_Charging_Interval"],
                            scale=customer["Expected_Charging_Interval"] * 0.15
                        )
                    )
                )

                dim_customer.at[index, "Days_Until_Next_Charge"] = new_interval

                continue

        # Generate a unique session ID.

        session_id = f"SES{session_counter:08d}"

        # Retrieve customer information required
        # for the charging session.

        customer_id = customer["Customer_ID"]
        home_state = customer["Home_State"]
        vehicle_id = customer["Vehicle_ID"]

        # Retrieve vehicle specifications.

        vehicle = ev_vehicle_master.loc[
            ev_vehicle_master["Vehicle_ID"] == vehicle_id
        ].iloc[0]

        battery_kwh = vehicle["Battery_kWh"]
        estimated_range = vehicle["Estimated_Range_km"]

        # Get all charging stations available
        # in the customer's home state.

        state_stations = dim_charging_station[
            dim_charging_station["State"] == home_state
        ]

        # Stations with more connectors have a
        # higher probability of being selected.

        station_weights = (
            state_stations["Connector_Count"]/
            state_stations["Connector_Count"].sum()
        )

        # Randomly select one charging station
        # using connector count as the weight.

        selected_station = state_stations.sample(
            n=1,
            weights=station_weights
        ).iloc[0]

        station_id = selected_station["Station_ID"]

        # Generate a unique charging session ID.
        session_id = f"SES{session_counter:08d}"

        session_counter += 1

        # ==========================================
        # Charging Time Windows
        # ==========================================

        # Time windows used for generating
        # charging session start times.

        TIME_WINDOWS = [
            (0,6),   # 00:00 - 06:00
            (6,10),  # 06:00 - 10:00
            (10,16), # 10:00 - 16:00
            (16,21), # 16:00 - 21:00
            (21,24)  # 21:00 - 24:00
        ]

        # Relative probabilities for charging
        # during different time windows on weekdays.

        WEEKDAY_WEIGHTS = [
            5,
            25,
            20,
            40,
            10
        ]

        # Relative probabilities for charging
        # during different time windows on weekends.
        WEEKEND_WEIGHTS = [
            5,
            10,
            35,
            35,
            15
        ]

        # Check whether the current simulation
        # date is a weekday or weekend.

        if current_date.weekday() < 5:
            time_weights = WEEKDAY_WEIGHTS

        else:
            time_weights = WEEKEND_WEIGHTS

        # Randomly choose a charging time window.

        selected_window = random.choices(
            TIME_WINDOWS,
            weights = time_weights,
            k = 1
        )[0]

        start_hour, end_hour = selected_window

        # Generate a random charging time
        # within the selected time window.

        hour = random.randint(start_hour, end_hour - 1)

        minute = random.randint(0, 59)

        session_start = current_date.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        # ==========================================
        # Battery Start Percentage
        # ==========================================

        # Relative probabilities for battery
        # state of charge when a customer
        # arrives at a charging station.

        BATTERY_START_RANGES = [
            (5,10),
            (10,20),
            (20,30),
            (30,40),
            (40,50),
            (50,60)
        ]

        BATTERY_START_WEIGHTS = [
            5,
            25,
            40,
            20,
            8,
            2
        ]

        # Randomly select a battery
        # start percentage range.

        selected_battery_start_range = random.choices(
            BATTERY_START_RANGES,
            weights=BATTERY_START_WEIGHTS,
            k=1
        )[0]

        # Generate the battery percentage
        # within the selected range.

        battery_start_percent = random.randint(
            selected_battery_start_range[0],
            selected_battery_start_range[1]
        )

        # ==========================================
        # Battery End Percentage
        # ==========================================

        BATTERY_END_RANGES = [
            (70,80),
            (80,90),
            (90,95),
            (95,100)
        ]

        BATTERY_END_WEIGHTS = [
            15,
            55,
            20,
            10
        ]

        # Randomly select a battery
        # end percentage range.

        selected_battery_end_range = random.choices(
            BATTERY_END_RANGES,
            weights=BATTERY_END_WEIGHTS,
            k=1
        )[0]

        # Generate the battery percentage
        # within the selected range.

        battery_end_percent = random.randint(
            selected_battery_end_range[0],
            selected_battery_end_range[1]
        )

        if battery_end_percent <= battery_start_percent:
            battery_end_percent = min(
                battery_start_percent + random.randint(10,30),
                100
            )

        # ==========================================
        # Energy_Delivered_kWh
        # ==========================================

        battery_capacity = vehicle["Battery_kWh"]

        # Calculate the percentage of the
        # battery charged during the session.

        battery_percent_charged = (
            battery_end_percent - battery_start_percent
        )

        # Calculate the energy delivered.

        energy_delivered_kwh = round(
            battery_capacity * battery_percent_charged / 100
            ,2
        )

        # ==========================================
        # Charging_Duration_Min
        # ==========================================

        # Calculate charging duration in minutes.

        MIN_CHARGING_DURATION_MIN = 1

        charging_duration_min = max(
            MIN_CHARGING_DURATION_MIN, 
            round(
                (energy_delivered_kwh / AVERAGE_CHARGING_RATE_KW) *60
            )
        )

        # ==========================================
        # Session_End
        # ==========================================

        session_end = session_start + timedelta(minutes=charging_duration_min)

        # Reset the charging countdown.
        new_interval = max(
            1,
            round(
                np.random.normal(
                    loc=customer["Expected_Charging_Interval"],
                    scale=customer["Expected_Charging_Interval"] * 0.15
                )
            )
        )

        dim_customer.at[index, "Days_Until_Next_Charge"] = new_interval

        # Append the session to sessions
        sessions.append({
            "Session_ID": session_id,
            "Customer_ID": customer_id,
            "Vehicle_ID": vehicle_id,
            "Station_ID": station_id,
            "Session_Start": session_start,
            "Battery_Start_Percent": battery_start_percent,
            "Battery_End_Percent": battery_end_percent,
            "Energy_Delivered_kWh": energy_delivered_kwh,
            "Charging_Duration_Min": charging_duration_min,
            "Session_End": session_end
        })

# Save to dataframe
fact_charging_sessions = pd.DataFrame(sessions)


# ==========================================
# Validate fact_charging_session
# ==========================================

print("\n========== FACT CHARGING SESSION VALIDATION ==========")

print(f"Total Sessions          : {len(fact_charging_sessions):,}")
print(f"Unique Session IDs      : {fact_charging_sessions["Session_ID"].nunique():,}")
print(f"Unique Customers        : {fact_charging_sessions["Customer_ID"].nunique():,}")

print("\nMissing Values")
print(fact_charging_sessions.isnull().sum())

print("\nDuplicate Session IDs")
print(fact_charging_sessions.duplicated().sum())

print("\nBusiness Rule Checks")

print(
    "Session_End >= Session_Start :",
    (
        fact_charging_sessions["Session_End"]
        >=
        fact_charging_sessions["Session_Start"]
    ).all()
)

print(
    "Battery_End > Battery_Start :",
    (
        fact_charging_sessions["Battery_End_Percent"]
        >
        fact_charging_sessions["Battery_Start_Percent"]
    ).all()
)

print(
    "Energy_Delivered_kWh > 0 :",
    (
        fact_charging_sessions["Energy_Delivered_kWh"] > 0
    ).all()
)

print(
    "Charging_Duration_Min > 0 :",
    (
        fact_charging_sessions["Charging_Duration_Min"] > 0
    ).all()
)

assert fact_charging_sessions["Session_ID"].is_unique,\
       "Duplicate Session_ID found."

assert fact_charging_sessions.isnull().sum().sum() == 0,\
       "Missing values found."

assert (
    fact_charging_sessions["Session_End"]
    >=
    fact_charging_sessions["Session_Start"]
).all(), \
    "Invalid Session_End."

assert (
    fact_charging_sessions["Battery_End_Percent"]
    >
    fact_charging_sessions["Battery_Start_Percent"]
).all(), \
    "Battery percentages are invalid."

assert (
    fact_charging_sessions["Energy_Delivered_kWh"] > 0
).all(), \
    "Invalid Energy_Delivered_kWh."

assert (
    fact_charging_sessions["Charging_Duration_Min"] > 0
).all(), \
    "Invalid Charging_Duration_Min."

print("\nValidation Passed Successfully.")
print("=====================================================\n")

# Extract csv
fact_charging_sessions.to_csv(
    FACT_CHARGING_SESSIONS,
    index=False
)









        



















