-- Grain = 1 station x 1 day
WITH valid_stations AS (

    SELECT DISTINCT
        s.station_id,
        s.state,
        s.station_type,
        s.connector_count

    FROM {{ ref('stg_charging_station') }} s

    INNER JOIN {{ ref('stg_customer') }} c
        ON s.state = c.home_state

),

simulation_dates AS (

    SELECT
        generate_series(
            MIN(session_date),
            MAX(session_date),
            INTERVAL '1 day'
        )::DATE AS session_date

    FROM {{ ref('int_session_enriched') }}

),

station_days AS (

    SELECT
        s.station_id,
        s.state,
        s.station_type,
        s.connector_count,
        d.session_date

    FROM valid_stations s

    CROSS JOIN simulation_dates d

),

daily_metrics AS (

    SELECT
        sd.station_id,
        sd.state,
        sd.session_date,
        sd.station_type,
        sd.connector_count,

        COUNT(se.session_id) AS sessions_count,

        COUNT(DISTINCT se.customer_id) AS customers_served,

        COALESCE(
            SUM(se.energy_delivered_kwh),
            0
        ) AS energy_delivered_kwh,

        COALESCE(
            AVG(se.charging_duration_min),
            0
        ) AS avg_session_duration_min,

        COALESCE(
            AVG(se.energy_delivered_kwh),
            0
        ) AS avg_energy_per_session_kwh,

        COALESCE(
            SUM(se.charging_duration_min),
            0
        ) AS total_charging_minutes

    FROM station_days sd

    LEFT JOIN {{ ref('int_session_enriched') }} se
        ON sd.station_id = se.station_id
        AND sd.session_date = se.session_date

    GROUP BY
        sd.station_id,
        sd.state,
        sd.session_date,
        sd.station_type,
        sd.connector_count

)

SELECT

    station_id,
    state,
    session_date,

    EXTRACT(ISODOW FROM session_date)::INTEGER AS day_of_week,

    TRIM(
        TO_CHAR(session_date, 'Day')
    ) AS day_name,

    TRIM(
        TO_CHAR(session_date, 'Month')
    ) AS month_name,

    station_type,
    connector_count,

    sessions_count,
    customers_served,
    energy_delivered_kwh,
    avg_session_duration_min,
    avg_energy_per_session_kwh,
    total_charging_minutes,

    (
        total_charging_minutes
        / (connector_count * 24.0 * 60.0)
    ) * 100 AS utilization_rate

FROM daily_metrics