WITH source AS (
    SELECT *
    FROM {{ source('raw','dim_charging_station') }}

)

SELECT 
   "Station_ID"::TEXT AS station_id,
   "State":: TEXT AS state,
   "Latitude":: DOUBLE PRECISION AS latitude,
   "Longitude":: DOUBLE PRECISION AS longitude,
   "Connector_Count"::BIGINT AS connector_count,
   "Station_Type"::TEXT AS station_type
FROM source

