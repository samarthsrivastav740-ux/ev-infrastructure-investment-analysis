WITH source AS (

    SELECT *
    FROM {{ source('raw', 'ev_vehicle_master') }}

)

SELECT

    "Vehicle_ID"::TEXT AS vehicle_id,

    "Manufacturer"::TEXT AS manufacturer,

    "Vehicle_Model"::TEXT AS vehicle_model,

    "Category"::TEXT AS category,

    "Battery_kWh"::DOUBLE PRECISION AS battery_kwh,

    "Estimated_Range_km"::BIGINT AS estimated_range_km,

    "Max_DC_Charging_kW"::DOUBLE PRECISION AS max_dc_charging_kw

FROM source