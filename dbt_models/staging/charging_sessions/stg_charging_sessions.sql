WITH source AS (
    SELECT *
    FROM {{ source('raw','fact_charging_sessions') }}

)

SELECT 
    "Session_ID"::TEXT AS session_id,
    "Customer_ID"::TEXT AS customer_id,
    "Vehicle_ID"::TEXT AS vehicle_id,
    "Station_ID"::TEXT AS station_id,
    
    "Session_Start"::TIMESTAMP AS session_start,
    "Session_End"::TIMESTAMP AS session_end,

    "Battery_Start_Percent"::BIGINT AS battery_start_percent,
    "Battery_End_Percent"::BIGINT AS battery_end_percent,

    "Energy_Delivered_kWh"::DOUBLE PRECISION AS energy_delivered_kwh,

    "Charging_Duration_Min"::BIGINT AS charging_duration_min

FROM source

