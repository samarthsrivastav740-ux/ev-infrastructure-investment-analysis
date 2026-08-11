WITH source AS (
    SELECT *
    FROM {{ source('raw','dim_customer') }}

)

SELECT 
   "Customer_ID"::TEXT AS customer_id,
   "Home_State":: TEXT AS home_state,
   "Vehicle_ID":: TEXT AS vehicle_id,
   "Category":: TEXT AS category,
   "Daily_Distance_km":: NUMERIC AS daily_distance_km,
   "Home_Charging_Available":: BOOLEAN AS home_charging_available
FROM source

