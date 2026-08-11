--grain: Station x Day
SELECT

    station_id,
    state,
    session_date,
    day_of_week,
    day_name,
    month_name,
    station_type,
    connector_count,

    sessions_count,
    customers_served,

    ROUND(
        energy_delivered_kwh::NUMERIC,
        3
    ) AS energy_delivered_kwh,

    ROUND(
        avg_session_duration_min::NUMERIC,
        3
    ) AS avg_session_duration_min,

    ROUND(
        avg_energy_per_session_kwh::NUMERIC,
        3
    ) AS avg_energy_per_session_kwh,

    ROUND(
        total_charging_minutes::NUMERIC,
        3
    ) AS total_charging_minutes,

    ROUND(
        utilization_rate::NUMERIC,
        3
    ) AS utilization_rate

FROM {{ ref('int_station_daily') }}