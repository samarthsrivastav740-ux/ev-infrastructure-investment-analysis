WITH source AS (

    SELECT *
    FROM {{ source('raw', 'state_ev_registrations') }}
)

SELECT 
    "Sl. No."::INTEGER AS serial_no,

    "State/ UT"::TEXT AS state,

    "Total EV"::BIGINT AS total_ev,

    "Total Vehicles Sold"::BIGINT AS total_vehicles_sold,

    "% of Share of EV in Total Vehicles Sold"::NUMERIC AS ev_market_share_pct

FROM source
WHERE "State/ UT" <> 'Total'