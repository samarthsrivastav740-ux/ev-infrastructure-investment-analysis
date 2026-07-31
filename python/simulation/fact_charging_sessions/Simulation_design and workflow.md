# Fact Charging Sessions Simulation Design

This document describes the methodology used to generate charging events in the `fact_charging_sessions` table. Unlike the dimension tables, charging sessions are not generated column by column. Instead, the simulation creates one complete charging event at a time by modeling customer charging behavior over a multi-day simulation period. :contentReference[oaicite:0]{index=0}

# Simulation Workflow

The simulation follows the workflow below for every simulated day.

```text
Initialize Simulation
        │
        ▼
Process One Day
        │
        ▼
Process Each Customer
        │
        ▼
Update Charging Countdown
        │
        ▼
Charging Required?
        │
    ┌───┴────┐
    │        │
   No       Yes
    │        │
 Continue    ▼
      Home Charging Available?
           │
      ┌────┴────┐
      │         │
 Skip Public   Generate Charging Event
 Charging          │
                   ▼
         Select Charging Station
                   │
                   ▼
        Generate Session Timing
                   │
                   ▼
        Generate Battery Levels
                   │
                   ▼
        Calculate Energy Delivered
                   │
                   ▼
       Calculate Charging Duration
                   │
                   ▼
        Generate Session End Time
                   │
                   ▼
      Reset Charging Countdown
                   │
                   ▼
        Save Charging Session
```

---

# Step 1. Initialize Simulation

### Purpose

Prepare the simulation environment before charging events are generated.

### Generation Method

- Load all required reference and simulated tables.
- Configure simulation parameters.
- Calculate the expected charging interval for every customer.
- Initialize each customer's charging countdown with a random starting value.

### Design Decision

Randomizing the initial charging countdown prevents every customer from requiring charging on the same day, resulting in a more realistic distribution of charging demand.

---

# Step 2. Daily Customer Simulation

### Purpose

Simulate charging behavior over multiple days.

### Generation Method

For every simulation day:

- Process every customer once.
- Reduce the customer's remaining days until the next charge.
- Only customers whose countdown reaches zero become eligible for a charging session.

### Design Decision

Using a daily countdown approximates real-world charging frequency without simulating individual vehicle movement throughout the day.

---

# Step 3. Home Charging Decision

### Purpose

Determine whether a customer uses public charging on a given day.

### Generation Method

Customers with home charging availability have a predefined probability of charging at home instead of using a public charging station.

If home charging is selected:

- No public charging session is generated.
- The customer's charging countdown is reset.

### Design Decision

This prevents customers with home charging from unrealistically relying on public charging infrastructure.

---

# Step 4. Generate Charging Event

### Purpose

Create one complete charging session for customers requiring public charging.

### Generation Method

For each charging event, the simulation generates:

- Session identifier
- Customer
- Vehicle
- Charging station
- Session start time
- Battery state of charge
- Energy delivered
- Charging duration
- Session end time

The completed event is stored as one row in the fact table.

---

# Step 5. Reset Charging Cycle

### Purpose

Prepare the customer for the next charging event.

### Generation Method

After completing a charging session, a new charging interval is sampled around the customer's expected charging interval.

### Design Decision

Introducing random variation prevents customers from charging on perfectly fixed schedules while maintaining realistic charging frequency.

---

# Validation

The generated charging sessions are validated to ensure:

- No missing values
- Unique Session_ID values
- Session_End occurs after Session_Start
- Battery_End_Percent is greater than Battery_Start_Percent
- Energy_Delivered_kWh is positive
- Charging_Duration_Min is positive