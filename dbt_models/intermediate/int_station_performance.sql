--Grain:- 1 row = 1 charging station
WITH station_performance AS (

    SELECT
        station_id,
        state,
        station_type,
        connector_count,

        SUM(sessions_count) AS total_sessions,

        SUM(customers_served) AS customers_served,

        SUM(energy_delivered_kwh) AS total_energy_delivered_kwh,

        AVG(sessions_count) AS avg_daily_sessions,

        AVG(energy_delivered_kwh) AS avg_daily_energy_delivered_kwh,

        AVG(avg_session_duration_min) AS avg_session_duration_min,

        AVG(avg_energy_per_session_kwh) AS avg_energy_per_session_kwh,

        SUM(total_charging_minutes) AS total_charging_minutes,

        SUM(
            connector_count * 24.0 * 60.0
        ) AS total_available_connector_minutes

    FROM {{ ref('int_station_daily') }}

    GROUP BY
        station_id,
        state,
        station_type,
        connector_count

),

utilization AS (

    SELECT
        station_id,
        state,
        station_type,
        connector_count,

        total_sessions,
        customers_served,
        total_energy_delivered_kwh,
        avg_daily_sessions,
        avg_daily_energy_delivered_kwh,
        avg_session_duration_min,
        avg_energy_per_session_kwh,

        (
            total_charging_minutes
            / total_available_connector_minutes
        ) * 100 AS utilization_rate

    FROM station_performance

),

ranked AS (

    SELECT
        *,

        RANK() OVER (
            ORDER BY total_sessions DESC
        ) AS session_rank,

        RANK() OVER (
            ORDER BY total_energy_delivered_kwh DESC
        ) AS energy_rank,

        RANK() OVER (
            ORDER BY utilization_rate DESC
        ) AS utilization_rank

    FROM utilization

),

categorized AS (

    SELECT
        *,

        NTILE(3) OVER (
            ORDER BY utilization_rate DESC
        ) AS utilization_bucket

    FROM ranked

)

SELECT

    station_id,
    state,
    station_type,
    connector_count,

    total_sessions,
    customers_served,
    total_energy_delivered_kwh,

    avg_daily_sessions,
    avg_daily_energy_delivered_kwh,

    avg_session_duration_min,
    avg_energy_per_session_kwh,

    utilization_rate,

    CASE
        WHEN utilization_bucket = 1 THEN 'High'
        WHEN utilization_bucket = 2 THEN 'Medium'
        WHEN utilization_bucket = 3 THEN 'Low'
    END AS utilization_category,

    session_rank,
    energy_rank,
    utilization_rank

FROM categorized