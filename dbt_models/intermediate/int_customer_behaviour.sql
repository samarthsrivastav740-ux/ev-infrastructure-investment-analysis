-- Grain 1 row = 1 customer
WITH customer_profile AS (

    SELECT
        c.customer_id,
        c.home_state,
        c.vehicle_id,
        v.manufacturer,
        v.vehicle_model,
        v.category,
        c.daily_distance_km,
        c.home_charging_available

    FROM {{ ref('stg_customer') }} c

    INNER JOIN {{ ref('stg_ev_vehicle_master') }} v
        ON c.vehicle_id = v.vehicle_id

),

customer_behavior AS (

    SELECT
        customer_id,

        COUNT(session_id) AS total_sessions,

        COUNT(DISTINCT session_date) AS charging_days,

        COUNT(session_id) * 1.0
            / NULLIF(COUNT(DISTINCT session_date), 0)
            AS avg_sessions_per_day,

        SUM(energy_delivered_kwh) AS total_energy_delivered_kwh,

        AVG(energy_delivered_kwh) AS avg_energy_per_session_kwh,

        AVG(charging_duration_min) AS avg_session_duration_min,

        AVG(battery_start_percent) AS avg_battery_start_percent,

        AVG(battery_end_percent) AS avg_battery_end_percent

    FROM {{ ref('int_session_enriched') }}

    GROUP BY
        customer_id

)

SELECT

    cp.customer_id,
    cp.home_state,
    cp.vehicle_id,
    cp.manufacturer,
    cp.vehicle_model,
    cp.category,
    cp.daily_distance_km,
    cp.home_charging_available,

    COALESCE(cb.total_sessions, 0) AS total_sessions,

    COALESCE(cb.charging_days, 0) AS charging_days,

    COALESCE(cb.avg_sessions_per_day, 0) AS avg_sessions_per_day,

    COALESCE(
        cb.total_energy_delivered_kwh,
        0
    ) AS total_energy_delivered_kwh,

    COALESCE(
        cb.avg_energy_per_session_kwh,
        0
    ) AS avg_energy_per_session_kwh,

    COALESCE(
        cb.avg_session_duration_min,
        0
    ) AS avg_session_duration_min,

    COALESCE(
        cb.avg_battery_start_percent,
        0
    ) AS avg_battery_start_percent,

    COALESCE(
        cb.avg_battery_end_percent,
        0
    ) AS avg_battery_end_percent

FROM customer_profile cp

LEFT JOIN customer_behavior cb
    ON cp.customer_id = cb.customer_id 