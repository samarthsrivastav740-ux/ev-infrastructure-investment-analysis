--grain: 1 charging session
SELECT

    session_id,
    customer_id,
    vehicle_id,
    station_id,

    session_date,
    charging_hour,

    home_state,
    category,
    manufacturer,

    station_state,
    station_type,
    connector_count,

    battery_start_percent,
    battery_end_percent,

    ROUND(
        energy_delivered_kwh::NUMERIC,
        3
    ) AS energy_delivered_kwh,

    ROUND(
        charging_duration_min::NUMERIC,
        3
    ) AS charging_duration_min

FROM {{ ref('int_session_enriched') }}