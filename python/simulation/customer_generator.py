#==========================================
# Third Party Libraries
#==========================================

import pandas as pd
import numpy as np

#==========================================
# Project Constants
#==========================================

Total_Customers = 500000

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