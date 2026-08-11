-- grain 1 row = 1 state
WITH state_performance AS (

    SELECT
        state,

        COUNT(DISTINCT station_id) AS operational_pcs,

        SUM(sessions_count) AS total_sessions,

        SUM(energy_delivered_kwh) AS total_energy_delivered_kwh,

        AVG(sessions_count) AS avg_daily_sessions,

        AVG(energy_delivered_kwh) AS avg_daily_energy_delivered_kwh,

        (
            SUM(total_charging_minutes)
            / SUM(connector_count * 24.0 * 60.0)
        ) * 100 AS utilization

    FROM {{ ref('int_station_daily') }}

    GROUP BY
        state

),

ranked AS (

    SELECT
        *,

        RANK() OVER (
            ORDER BY total_sessions DESC
        ) AS charging_demand_rank,

        NTILE(3) OVER (
            ORDER BY utilization DESC
        ) AS utilization_bucket

    FROM state_performance

)

SELECT

    state,

    operational_pcs,

    total_sessions,

    total_energy_delivered_kwh,

    avg_daily_sessions,

    avg_daily_energy_delivered_kwh,

    utilization,

    CASE
        WHEN utilization_bucket = 1 THEN 'High'
        WHEN utilization_bucket = 2 THEN 'Medium'
        WHEN utilization_bucket = 3 THEN 'Low'
    END AS utilization_category,

    charging_demand_rank

FROM ranked