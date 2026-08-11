WITH source AS (

    SELECT *
    FROM {{ source('raw', 'state_coordinates') }}

)

SELECT

    "State/Union Territory"::TEXT AS state,

    "Latitude"::DOUBLE PRECISION AS latitude,

    "Longitude"::DOUBLE PRECISION AS longitude,

    "Type"::TEXT AS state_type

FROM source