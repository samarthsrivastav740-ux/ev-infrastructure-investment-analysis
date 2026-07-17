#==========================================
# Third Party Libraries
#==========================================

import pandas as pd

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
    for i in range (1,Total_Customers+1):

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
