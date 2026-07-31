# Dim Customer Simulation Design

This document describes the design methodology used to generate each column in the `dim_customer` table. Every column is generated using either reference datasets, statistical distributions, or documented engineering assumptions to create a realistic customer population.

---

# 1. Customer_ID

### Purpose

Uniquely identifies every simulated EV customer. It serves as the primary key of the `dim_customer` table and is used to link customers with charging sessions in downstream fact tables.

### Generation Method

- Generate **500,000** customer IDs sequentially.
- Prefix each ID with `CUS`.
- Pad the numeric portion with leading zeros to maintain a fixed-length format.

Example:

```text
CUS000001
CUS000002
CUS000003
```

### Design Decision

Sequential IDs were chosen because they are deterministic, human-readable, and sufficient for a simulated environment where uniqueness is the only requirement.

### Validation

- No missing values
- No duplicate Customer_IDs
- Total generated IDs = 500,000

---

# 2. Home_State

### Purpose

Represents the customer's state of residence. This determines the geographical distribution of the simulated customer base and serves as the primary location attribute for downstream charging demand analysis.

### Reference Dataset

- `state_wise_ev_registrations_2019-2024.csv`

### Data Preparation

- Retain only `State/UT` and `Total EV` columns.
- Remove the summary (`Total`) row.
- Exclude states with missing `Total EV` values.
- Calculate the probability of each state as:

```text
State Probability = State Total EV / Total EV Across All States
```

### Generation Method

Generate the `Home_State` for each customer using weighted random sampling based on the calculated state probabilities. This preserves the state-wise EV registration distribution observed in the reference dataset.

### Design Decision

State-wise EV registrations were used instead of uniform sampling to ensure that the simulated customer population reflects the real geographical distribution of EV adoption across India.

### Validation

- No missing values
- Compare simulated state probabilities with reference probabilities
- Maximum probability difference must remain within the defined validation threshold

---

# 3. Vehicle_ID

### Purpose

Assigns an EV model to each customer. The assigned vehicle influences customer characteristics such as vehicle category, daily travel distance, battery capacity, charging behaviour, and future charging sessions.

### Reference Datasets

- `ev_sales_by_makers_and_cat_15-24.csv`
- `ev_vehicle_master.csv`

### Data Preparation

- Keep only **2W** and **LMV** records from the sales dataset, then rename **LMV** to **4W**.
- Standardize manufacturer names to match the EV Vehicle Master.
- Retain only manufacturers present in the EV Vehicle Master.
- Keep only valid **Category–Manufacturer** combinations available in the EV Vehicle Master.
- Calculate total sales for each manufacturer across all available years.
- Calculate:
  - Vehicle category probabilities (2W and 4W)
  - Manufacturer probabilities within each category

### Generation Method

Vehicle assignment follows a three-step hierarchical process:

1. Select the vehicle category using weighted random sampling.
2. Select a manufacturer within the chosen category using weighted random sampling.
3. Select a vehicle model uniformly from the available models of the selected manufacturer.

### Design Decision

Historical EV sales were used to preserve realistic market share at both the vehicle category and manufacturer levels. Since model-wise sales data was unavailable, all vehicle models within the selected manufacturer were assumed to have an equal probability of being selected.

### Validation

- No missing Vehicle_ID values
- All generated Vehicle_IDs must exist in the EV Vehicle Master
- Compare simulated vehicle category distribution with the reference distribution

---

# 4. Daily_Distance_km

### Purpose

Represents the average distance traveled by a customer in a typical day. This attribute influences battery depletion and determines how frequently a customer is expected to use public charging infrastructure.

### Reference report

- ORF mobility studies (2W average daily distance)

Link:- https://www.orfonline.org/expert-speak/road-emission-control-electrifying-personal-mobility-in-india

### Generation Method

- Assign an average daily distance of **30 km** for 2W customers based on ORF mobility studies.
- Assign an average daily distance of **40 km** for 4W customers by applying a **10 km engineering offset** to reflect higher average travel.
- Generate individual daily distances using a normal distribution.
- Restrict generated values to a realistic range of **5–80 km**.

### Design Decision

Reliable evidence was available only for two-wheelers. Since no comparable public dataset was found for four-wheelers, a higher average daily distance was introduced as an engineering assumption. A normal distribution was selected because daily commuting typically clusters around an average value while allowing natural variation among customers.

### Validation

- No missing values
- Verify minimum and maximum generated distances
- Compare simulated average daily distance with the expected average for each vehicle category

---

# 5. Home_Charging_Available

### Purpose

Indicates whether a customer has access to a private home charging facility. This attribute influences future charging behaviour by distinguishing customers who can charge at home from those who rely primarily on public charging infrastructure.

### Reference Source

- McKinsey Global Automotive Consumer Survey (India)

Link 1:- https://www.mckinsey.com/industries/automotive-and-assembly/our-insights/consumers-are-driving-the-transition-to-electric-cars-in-india

Link 2:-https://bolt.earth/blog/part-1-the-future-of-workplace-ev-charging-in-india


### Generation Method

- Assign a **55%** probability of home charging availability.
- Generate the attribute using a Bernoulli probability distribution, where each customer is independently assigned either **True** or **False**.

### Design Decision

The McKinsey survey reports that approximately 55% of Indian EV owners have access to home charging. Since category-wise (2W/4W) home charging statistics were unavailable, the same probability was applied uniformly across all customers.

### Validation

- No missing values
- Compare simulated home charging probability with the expected probability (55%)