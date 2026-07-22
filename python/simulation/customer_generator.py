#==========================================
# Third Party Libraries
#==========================================

import pandas as pd
import numpy as np


#==========================================
# Project Constants
#==========================================

Total_Customers = 500000

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


#==========================================
# Column 1 - Customer_ID
#==========================================

def generate_customer_ids(total_customers):
    """
    Generate customer IDs.

    Example:
        CUS000001
        CUS000002
        CUS000003
    """
    # Create an empty list to store Customer IDs
    customer_ids = []
   
    # Generate one customer ID at a time
    for i in range (1,total_customers+1):

        # Format the customer ID with leading zeros
        customer_id= f"CUS{i:06d}"

        # Add the generated id to the list
        customer_ids.append(customer_id)

    # Return the completed list
    return customer_ids

#==========================================
# Create Customer Dataframe
#==========================================

customer_df=pd.DataFrame()

# Generate Customer_ID column
customer_df["Customer_ID"]=generate_customer_ids(Total_Customers)

#==========================================
# Validation - Customer_ID
#==========================================

print("\nCustomer_ID validation")

# Check total number of rows
print("Total Customers:",len(customer_df))

# Check for duplicate Customer IDs
print("Duplicate Customer IDs:",customer_df["Customer_ID"].duplicated().sum())

# Check for missing Customer IDs
print("Missing Customer IDs:",customer_df["Customer_ID"].isnull().sum())

#==========================================
# Column 2 - Home_State
#==========================================

# Load state wise ev registrations data
from python.utils.file_paths import STATE_EV_REGISTRATIONS
state_ev_df=pd.read_csv(STATE_EV_REGISTRATIONS)

# Keep only required columns
state_ev_df=state_ev_df[
    ["State/ UT","Total EV"]
]

# Remove the summary row
state_ev_df=state_ev_df[
    state_ev_df["State/ UT"]!="Total"
]

# Reset the index
state_ev_df=state_ev_df.reset_index(drop=True)

# Checking missing Total Ev values
print("Rows with missing Total EV")

print(
    state_ev_df[
        state_ev_df["Total EV"].isna()
    ]
)

# Government dataset contains missing Total EV
# for Sikkim (recorded as "NA").
# Remove rows where Total EV is unavailable
# because sampling probabilities cannot be calculated.

state_ev_df = state_ev_df.dropna(
    subset=["Total EV"]
)
state_ev_df = state_ev_df.reset_index(drop=True)


# Calculate total EV registrations
total_ev=state_ev_df["Total EV"].sum()

# Calculate probability of each state
state_ev_df["Probability"]=(
    state_ev_df["Total EV"]/total_ev
)

def generate_home_states(state_dataframe,total_customers):
    """
    Generate Home_State using weighted random sampling
    based on actual EV registrations.
    """
    home_states= np.random.choice(

        # state to choose from
        state_dataframe["State/ UT"],

        # Number of customers to generate
        size= total_customers,

        # Sampling Probabilities
        p=state_dataframe["Probability"] 
    )
    return home_states

# Generate Home state column
customer_df["Home_State"]=generate_home_states(
    state_ev_df,
    Total_Customers
)

print(customer_df.head())

#==========================================
# Validation - Home_State
#==========================================

print("\nHome_State Validation")

# Check for missing values
print(
    "Missing Home_State:",customer_df["Home_State"].isnull().sum()
)

# Display customer distribution by state

print("\nCustomer Distribution")

print(
    customer_df["Home_State"]
    .value_counts()
    .head(10)
)

# Actual distribution from government dataset
actual_distribution = (
    state_ev_df[["State/ UT", "Probability"]]
    .rename(columns={"State/ UT": "Home_State"})
)

# Simulated distribution
simulated_distribution = (
    customer_df["Home_State"]
    .value_counts(normalize=True)
    .reset_index()
)

simulated_distribution.columns = [
    "Home_State",
    "Simulated_Probability"
]

# Compare both
comparison_df = actual_distribution.merge(
    simulated_distribution,
    on="Home_State"
)

comparison_df["Difference"] = (
    comparison_df["Simulated_Probability"]
    - comparison_df["Probability"]
)

print(comparison_df.head())

# Maximum absolute difference
max_difference = comparison_df["Difference"].abs().max()

print(f"\nMaximum Difference: {max_difference:.6f}")

# Validation
if max_difference < 0.002:
    print("Home_State validation PASSED")
else:
    print("Home_State validation FAILED")

comparison_df.to_csv(
    "data/simulated/home_state_validation.csv",
    index=False
)


#==========================================
# Column 3 - Vehicle_ID
#==========================================

# Load EV sales by manufacturer and category dataset
from python.utils.file_paths import EV_SALES_BY_CAT_AND_MAKERS

ev_sales_df=pd.read_csv(EV_SALES_BY_CAT_AND_MAKERS)

# Keep only required columns
ev_sales_df=ev_sales_df[
    [
        "Cat","Maker","2015","2016","2017","2018","2019","2020",
        "2021","2022","2023","2024"
    ]
]

# keep only 2W and LMV records
ev_sales_df=ev_sales_df[
    ev_sales_df["Cat"].isin(
        ["2W","LMV"]
    )
]

# Reset the index 
ev_sales_df=ev_sales_df.reset_index(drop=True)

# Rename LMV to 4W
ev_sales_df["Cat"]=(
    ev_sales_df["Cat"]
    .replace(
        {
            "LMV":"4W"
        }
    )
)

# Load EV Vehicle Master dataset
from python.utils.file_paths import EV_VEHICLE_MASTER

vehicle_master_df=pd.read_csv(EV_VEHICLE_MASTER)

# Keep only required columns
vehicle_master_df=vehicle_master_df[
    [
        "Vehicle_ID","Manufacturer","Vehicle_Model","Category","Battery_kWh",
        "Estimated_Range_km","Max_DC_Charging_kW"
    ]
]

# Standardize manufacturer names
# The EV sales dataset contains legal company names,
# while the EV vehicle master uses simplified manufacturer names.
# Map all legal names to a common manufacturer name.

manufacturer_mapping = {

    # Ampere
    "AMPERE VEHICLES PRIVATE LIMITED": "Ampere",
    "AMPERE VEHICLES PVT LTD": "Ampere",

    # Ather
    "ATHER ENERGY PVT LTD": "Ather",

    # Audi
    "AUDI AG": "Audi",

    # Bajaj
    "BAJAJ AUTO LTD": "Bajaj",

    # BGauss
    "BGAUSS AUTO PRIVATE LIMITED": "BGauss",

    # BMW
    "BMW INDIA PVT LTD": "BMW",

    # BYD
    "BYD AUTO": "BYD",
    "BYD INDIA PRIVATE LIMITED": "BYD",

    # Hero MotoCorp
    "HERO MOTOCORP LTD": "Hero MotoCorp",

    # Hyundai
    "HYUNDAI MOTOR INDIA LTD": "Hyundai",

    # Jaguar
    "JAGUAR LAND ROVER INDIA LIMITED": "Jaguar",

    # Kia
    "KIA INDIA PRIVATE LIMITED": "Kia",

    # Mahindra
    "MAHINDRA & MAHINDRA LIMITED": "Mahindra",
    "MAHINDRA ELECTRIC MOBILITY LIMITED": "Mahindra",
    "MAHINDRA LAST MILE MOBILITY LTD": "Mahindra",

    # Mercedes-Benz
    "MERCEDES-BENZ AG": "Mercedes-Benz",
    "MERCEDES-BENZ INDIA PVT LTD": "Mercedes-Benz",

    # MG Motor
    "MG MOTOR INDIA PVT LTD": "MG Motor",

    # Oben
    "OBEN ELECTRIC VEHICLES PVT LTD": "Oben",

    # Okaya
    "OKAYA EV PVT LTD": "Okaya",

    # Ola Electric
    "OLA ELECTRIC TECHNOLOGIES PVT LTD": "Ola Electric",

    # Porsche
    "PORSCHE AG GERMANY": "Porsche",

    # River
    "RIVER MOBILITY PVT LTD": "River",

    # Tata
    "TATA MOTORS LTD": "Tata",
    "TATA MOTORS PASSENGER VEHICLES LTD": "Tata",
    "TATA PASSENGER ELECTRIC MOBILITY LTD": "Tata",

    # Tork Motors
    "TORK MOTORS PVT LTD": "Tork Motors",

    # TVS
    "TVS MOTOR COMPANY LTD": "TVS",

    # Ultraviolette
    "ULTRAVIOLETTE AUTOMOTIVE PVT LTD": "Ultraviolette",

    # Volvo
    "VOLVO AUTO INDIA PVT LTD": "Volvo"
}

# Replace manufacturer names with standardized names
ev_sales_df["Maker"]=(
    ev_sales_df["Maker"].replace(manufacturer_mapping)
)

# Keep only manufacturers present in EV Vehicle Master
ev_sales_df=ev_sales_df[
    ev_sales_df["Maker"].isin(
        vehicle_master_df["Manufacturer"]
    )
]

# Reset the index
ev_sales_df=ev_sales_df.reset_index(drop=True)

# Get all valid Category-Manufacturer combinations
# from EV Vehicle Master.
valid_combinations = (
    vehicle_master_df[
        ["Category", "Manufacturer"]
    ]
    .drop_duplicates()
)

# Keep only Category-Manufacturer combinations
# that exist in EV Vehicle Master.
ev_sales_df = ev_sales_df.merge(
    valid_combinations,
    left_on=["Cat", "Maker"],
    right_on=["Category", "Manufacturer"],
    how="inner"
)

# Remove duplicate columns created by merge
ev_sales_df = ev_sales_df.drop(
    columns=[
        "Category",
        "Manufacturer"
    ]
)

# Reset the index
ev_sales_df = ev_sales_df.reset_index(drop=True)

# Calculate total sales across all years
ev_sales_df["Total_Sales"] = (
    ev_sales_df[
        [
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
            "2024"
        ]
    ]
    .sum(axis=1)
)

# Calculate total sales for each vehicle category
category_sales=(
    ev_sales_df
    .groupby("Cat")["Total_Sales"]
    .sum()
    .reset_index()
)

# Calculate category probabilities
category_sales["Probability"]=(
    category_sales["Total_Sales"]/category_sales["Total_Sales"].sum()
)

# Calculate total sales for each manufacturer
# within each vehicle category.
manufacturer_sales=(
    ev_sales_df
    .groupby(
        ["Cat","Maker"]
    )["Total_Sales"]
    .sum()
    .reset_index()
)

# Calculate manufacturer probability
# within each vehicle category.
manufacturer_sales["Probability"]=(
    manufacturer_sales["Total_Sales"]/
    manufacturer_sales.groupby("Cat")["Total_Sales"]
    .transform("sum")
)

#==========================================
# Generate Vehicle_ID
#==========================================

def generate_vehicle_ids(
        total_customers,
        category_sales,
        manufacturer_sales,
        vehicle_master_df
):
    '''
    Generate Vehicle_ID for every customer.
    Vehicle assignment follows three steps:
    1. Select vehicle category (2W / 4W)
    2. Select manufacturer within the selected category
    3. Select vehicle model uniformly within the selected manufacturer
    '''

    # Create an empty list to store Vehicle IDs
    vehicle_ids=[]

    # Generate one vehicle for each customer
    for i in range(total_customers):
        #========================
        # Step 1 - Select Vehicle category
        #========================

        selected_category=np.random.choice(
            # Vehicle category to choose from
            category_sales["Cat"],

            # Select one category
            size=1,

            # Category probabilities
            p=category_sales["Probability"] 
        )[0]

        #========================
        # Step 2 - Select Manufacturer
        #========================

        # Keep only manufacturer 
        # related to the selected category.
        category_manufacturers=(
            manufacturer_sales[
                manufacturer_sales["Cat"]==selected_category
            ]
        )
    
        # Select manufacturer using weighted
        # random sampling.
        selected_manufacturer=np.random.choice(
    
            # Manufacturer to choose from
            category_manufacturers["Maker"],
    
            # Select one manufacturer
            size=1,

            # Manufacturer probabilities
            p=category_manufacturers["Probability"]

        )[0]
        
        #========================
        # Step 3 - Select Vehicle
        #========================

        # Keep only vehicle belonging to the 
        # selected category and customer.
        available_vehicles=(
            vehicle_master_df[
                (vehicle_master_df["Category"]==selected_category)
                &
                (vehicle_master_df["Manufacturer"]==selected_manufacturer)
            ]
        )

        # Select one vehicle uniformly from
        # the available vehicle models
        selected_vehicle=available_vehicles.sample(
            n=1
        ).iloc[0]

        # Get Vehicle_ID
        vehicle_id=selected_vehicle["Vehicle_ID"]
        
        # Add Vehicle_ID to the list
        vehicle_ids.append(vehicle_id)

    # Return the completed Vehicle_ID list
    return vehicle_ids

# Generate Vehicle_ID column
customer_df["Vehicle_ID"] = generate_vehicle_ids(
    Total_Customers,
    category_sales,
    manufacturer_sales,
    vehicle_master_df
)

print(customer_df.head())

#==========================================
# Validation - Vehicle_ID
#==========================================

# Missing values
print(
    "Missing Vehicle_ID:",
    customer_df["Vehicle_ID"].isnull().sum()
)

# Invalid Vehicle_ID
# Every generated Vehicle_ID should exist in ev_vehicle_master.
invalid_vehicle_ids = (
    ~customer_df["Vehicle_ID"].isin(
        vehicle_master_df["Vehicle_ID"]
    )
).sum()

print(
    "Invalid Vehicle_ID:",
    invalid_vehicle_ids
)

# Simulated Category Distribution
vehicle_validation = (
    customer_df[
        ["Vehicle_ID"]
    ]
    .merge(
        vehicle_master_df[
            ["Vehicle_ID", "Category"]
        ],
        on="Vehicle_ID"
    )
)

# Calculate simulated distribution
simulated_category = (
    vehicle_validation["Category"]
    .value_counts(normalize=True)
    .reset_index()
)

simulated_category.columns = [
    "Category",
    "Simulated_Probability"
]

# Compare with reference
actual_category = (
    category_sales[
        ["Cat", "Probability"]
    ]
    .rename(
        columns={
            "Cat":"Category"
        }
    )
)

# Merge
category_comparison = (
    actual_category.merge(
        simulated_category,
        on="Category"
    )
)

category_comparison["Difference"] = (
    category_comparison["Simulated_Probability"]
    -
    category_comparison["Probability"]
)

print(category_comparison.head())

# Maximum Difference
max_difference = (
    category_comparison["Difference"]
    .abs()
    .max()
)

print(
    f"\nMaximum Difference: {max_difference:.6f}"
)

if max_difference < 0.002:
    print("Vehicle Category validation PASSED")
else:
    print("Vehicle Category validation FAILED")

category_comparison.to_csv(
    "data/simulated/vehicle_category_validation.csv",
    index=False
)

#==========================================
# Column 4 - Daily_Distance_km
#==========================================

#==========================================
# Simulation Parameters
#==========================================

# Average daily distance for 2W customers.
# Based on ORF mobility studies reporting
# urban two-wheelers typically travel
# around 27–33 km/day
AVERAGE_2W_DISTANCE=30

# Additional distance assigned to 4W customers.
# Engineering assumption to reflect longer
# average travel compared to 2W customers.
FOUR_WHEELER_DISTANCE_OFFSET = 10

# Average daily distance for 4W customers
AVERAGE_4W_DISTANCE=(
    AVERAGE_2W_DISTANCE+FOUR_WHEELER_DISTANCE_OFFSET
)

# Standard deviation for daily distance.
# Engineering assumption.
DISTANCE_STANDARD_DEVIATION=8

# Minimum allowed average daily distance.
# Engineering assumption.
MIN_DAILY_DISTANCE = 5

# Maximum allowed average daily distance.
# Engineering assumption.
MAX_DAILY_DISTANCE = 80

#==========================================
# Get Vehicle Category
#==========================================

# Add vehicle category to customer dataframe
# using Vehicle_ID.
customer_df=customer_df.merge(
    
    # Keep only required columns
    vehicle_master_df[
        ["Vehicle_ID", "Category"]
    ],

    # Merge using Vehicle_ID
    on="Vehicle_ID",

    # keep all customers
    how="left" 
)

#==========================================
# Validation - Vehicle Category
#==========================================

# Check for missing categories
print(
    "Missing Categories:",
    customer_df["Category"].isnull().sum()
)

# Display category distribution
print(
    customer_df["Category"]
    .value_counts()
)

def generate_daily_distance(customer_dataframe):
    """
    Generate Daily_Distance_km for every customer.

    Daily distance is generated using a normal
    distribution based on the customer's
    vehicle category.

    2W customers use the evidence-based
    average daily distance.

    4W customers use a higher average daily
    distance based on an engineering
    assumption.
    """

    # Create empty list to store 
    # daily travel distance.
    daily_distances=[]

    # Generate distance for every customer
    for i in range(len(customer_dataframe)):

        # Get vehicle category
        category=(
            customer_dataframe
            .iloc[i]["Category"]
        )

        #================================
        # Select average daily distance
        #================================

        # 2W customers
        if category == "2W":
            average_distance=(
                AVERAGE_2W_DISTANCE
            )
        
        # 4W customers
        elif category=="4W":
            average_distance=(
                AVERAGE_4W_DISTANCE
            )
        
        else:
            raise ValueError(
                f"Invalid vehicle category: {category}"
            )
        #==================================
        # Generate Daily Distance
        #==================================

        daily_distance=np.random.normal(

            # Average daily distance
            loc=average_distance,

            # Standard deviation
            scale=DISTANCE_STANDARD_DEVIATION
        )

        # Restrict distance within
        # minimum and maximum limits.
        daily_distance=np.clip(

            daily_distance,

            MIN_DAILY_DISTANCE,

            MAX_DAILY_DISTANCE
        )

        # Round to nearest kilometer
        daily_distance=int(
            round(daily_distance)
        )

        # Add distance to the list
        daily_distances.append(
            daily_distance
        )
    
    # Return complete list
    return daily_distances

# Generate Daily_Distance_km column
customer_df["Daily_Distance_km"] = (
    generate_daily_distance(
        customer_df
    )
)

print(customer_df.head())

#==========================================
# Validation - Daily_Distance_km
#==========================================

print("\nDaily_Distance_km Validation")

# Check for missing values
print(
    "Missing Daily_Distance_km:",
    customer_df["Daily_Distance_km"].isnull().sum()
)

# Check minimum distance
print(
    "Minimum Daily_Distance_km:",
    customer_df["Daily_Distance_km"].min()
)

# Check maximum distance
print(
    "Maximum Daily_Distance_km:",
    customer_df["Daily_Distance_km"].max()
)

# Display summary statistics
print("\nSummary Statistics")

print(
    customer_df["Daily_Distance_km"]
    .describe()
)

# Average daily distance by vehicle category
print("\nAverage Daily Distance by Category")

print(
    customer_df
    .groupby("Category")["Daily_Distance_km"]
    .mean()
)

# Compare with expected averages
actual_mean=pd.DataFrame(
    {
        "Category":["2W","4W"],
        "Expected_Mean":[AVERAGE_2W_DISTANCE,AVERAGE_4W_DISTANCE]
    }
)

# Calculate simulated averages
simulated_mean=(
    customer_df
    .groupby("Category")["Daily_Distance_km"]
    .mean()
    .reset_index()
)

simulated_mean.columns=[
    "Category","Simulated_Mean"
]

# Merge expected and simulated averages
comparison_df=(
    actual_mean.merge(
        simulated_mean,
        on="Category"
    )
)

# Calculate difference
comparison_df["Difference"]=(
    comparison_df["Simulated_Mean"]
    -
    comparison_df["Expected_Mean"]
)

print("\nExpected vs Simulated Average Daily Distance")

print(comparison_df)

# Maximum absolute difference
max_difference = (
    comparison_df["Difference"]
    .abs()
    .max()
)

print(
    f"\nMaximum Difference: {max_difference:.6f}"
)

# Validation
if max_difference < 0.5:
    print("Daily_Distance_km validation PASSED")
else:
    print("Daily_Distance_km validation FAILED")

# Save validation report
comparison_df.to_csv(
    "data/simulated/daily_distance_validation.csv",
    index=False
)

#==========================================
# Column 5 - Home_Charging_Available
#==========================================

# McKinsey Global Automotive Consumer Survey (India)
# Approximately 55% of EV owners have access to home charging

HOME_CHARGING_PROBABILITY = 0.55

def generate_home_charging():
    home_charging=[]

    for _ in range(Total_Customers):

        if np.random.random() < HOME_CHARGING_PROBABILITY:
            home_charging.append(True)

        else:
            home_charging.append(False)
    
    return home_charging

customer_df["Home_Charging_Available"]=generate_home_charging()

print(customer_df.head())

#==========================================
# Validation - Home_Charging_Available
#==========================================

print("\nHome_Charging_Available Validation")

# Check missing values
missing_home_charging=customer_df["Home_Charging_Available"].isna().sum()

print(f"Missing Home_Charging_Available:{missing_home_charging}")

# Expected probability 
expected_probability=HOME_CHARGING_PROBABILITY

# Simulated probability
simulated_probability= (
    customer_df["Home_Charging_Available"].mean()
)

# Comparison table
comparison_df=pd.DataFrame(
    {
        "Expected_probability":[expected_probability],
        "Simulated_probability":[simulated_probability]

    }
)

comparison_df["Difference"]=(
    comparison_df["Simulated_probability"]
    -
    comparison_df["Expected_probability"]
)

print("\nExpected vs Simulated Home Charging Probability")

print(comparison_df)

# Maximum absolute difference
max_difference = (
    comparison_df["Difference"]
    .abs()
    .max()
)

print(f"\nMaximum Difference: {max_difference:.6f}")

# Validation
if max_difference < 0.02:
    print("Home_Charging_Available validation PASSED")
else:
    print("Home_Charging_Available validation FAILED")

# Save validation report
comparison_df.to_csv(
    "data/simulated/home_charging_validation.csv",
    index=False
)

# =============================================================================
# Final Dataset Validation
# =============================================================================

print("\n" + "=" * 70)
print("FINAL DATASET VALIDATION")
print("=" * 70)

# -------------------------------------------------------------------------
# Dataset Shape
# -------------------------------------------------------------------------

print(f"\nTotal Rows    : {customer_df.shape[0]:,}")
print(f"Total Columns : {customer_df.shape[1]}")

# -------------------------------------------------------------------------
# Data Types
# -------------------------------------------------------------------------

print("\nData Types")

print(customer_df.info())

# -------------------------------------------------------------------------
# Missing Values
# -------------------------------------------------------------------------

print("\nMissing Values")

missing_values = customer_df.isnull().sum()

print(missing_values)

# -------------------------------------------------------------------------
# Duplicate Customer_ID Check
# -------------------------------------------------------------------------

duplicate_customer_ids = customer_df["Customer_ID"].duplicated().sum()

print(f"\nDuplicate Customer_IDs : {duplicate_customer_ids}")

# -------------------------------------------------------------------------
# Duplicate Rows Check
# -------------------------------------------------------------------------

duplicate_rows = customer_df.duplicated().sum()

print(f"Duplicate Rows : {duplicate_rows}")

# -------------------------------------------------------------------------
# Final Validation Status
# -------------------------------------------------------------------------

if (
    missing_values.sum() == 0
    and duplicate_customer_ids == 0
    and duplicate_rows == 0
):
    print("\nFINAL DATASET VALIDATION PASSED")

else:
    print("\nFINAL DATASET VALIDATION FAILED")

print("=" * 70)


# Export dim_customer
customer_df.to_csv(
    "data/simulated/dim_customer.csv",
    index=False
)