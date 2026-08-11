--grain: station
SELECT

    station_id,
    state,
    station_type,
    connector_count,

    total_sessions,
    customers_served,

    ROUND(
        total_energy_delivered_kwh::NUMERIC,
        3
    ) AS total_energy_delivered_kwh,

    ROUND(
        avg_daily_sessions::NUMERIC,
        3
    ) AS avg_daily_sessions,

    ROUND(
        avg_daily_energy_delivered_kwh::NUMERIC,
        3
    ) AS avg_daily_energy_delivered_kwh,

    ROUND(
        avg_session_duration_min::NUMERIC,
        3
    ) AS avg_session_duration_min,

    ROUND(
        avg_energy_per_session_kwh::NUMERIC,
        3
    ) AS avg_energy_per_session_kwh,

    ROUND(
        utilization_rate::NUMERIC,
        3
    ) AS utilization_rate,

    utilization_category,

    session_rank,
    energy_rank,
    utilization_rank

FROM {{ ref('int_station_performance') }}