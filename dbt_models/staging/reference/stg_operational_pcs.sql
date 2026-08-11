WITH source AS (

    SELECT *
    FROM {{ source('raw', 'operational_pcs') }}

)

SELECT

    "State"::TEXT AS state,

    "No. of Operational PCS"::BIGINT AS operational_pcs

FROM source