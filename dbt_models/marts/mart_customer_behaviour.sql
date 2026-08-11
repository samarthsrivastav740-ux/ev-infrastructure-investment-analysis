-- grain: 1 customer
SELECT

    customer_id,
    home_state,
    vehicle_id,
    manufacturer,
    vehicle_model,
    category,

    ROUND(
        daily_distance_km::NUMERIC,
        3
    ) AS daily_distance_km,

    home_charging_available,

    total_sessions,
    charging_days,

    ROUND(
        avg_sessions_per_day::NUMERIC,
        3
    ) AS avg_sessions_per_day,

    ROUND(
        total_energy_delivered_kwh::NUMERIC,
        3
    ) AS total_energy_delivered_kwh,

    ROUND(
        avg_energy_per_session_kwh::NUMERIC,
        3
    ) AS avg_energy_per_session_kwh,

    ROUND(
        avg_session_duration_min::NUMERIC,
        3
    ) AS avg_session_duration_min,

    ROUND(
        avg_battery_start_percent::NUMERIC,
        3
    ) AS avg_battery_start_percent,

    ROUND(
        avg_battery_end_percent::NUMERIC,
        3
    ) AS avg_battery_end_percent

FROM {{ ref('int_customer_behaviour') }}