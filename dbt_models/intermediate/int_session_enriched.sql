--Grain:- 1 row= 1 charging session
WITH sessions AS (

    SELECT *
    FROM {{ ref('stg_charging_sessions') }}

),

customers AS (

    SELECT
        customer_id,
        home_state,
        daily_distance_km,
        home_charging_available
    FROM {{ ref('stg_customer') }}

),

vehicles AS (

    SELECT
        vehicle_id,
        manufacturer,
        vehicle_model,
        category
    FROM {{ ref('stg_ev_vehicle_master') }}

),

stations AS (

    SELECT
        station_id,
        state AS station_state,
        station_type,
        connector_count
    FROM {{ ref('stg_charging_station') }}

)

SELECT

    -- Session information
    s.session_id,
    s.customer_id,
    s.vehicle_id,
    s.station_id,
    s.session_start,
    s.session_end,

    -- Charging metrics
    s.battery_start_percent,
    s.battery_end_percent,
    s.energy_delivered_kwh,
    s.charging_duration_min,

    -- Time attributes
    s.session_start::DATE AS session_date,
    EXTRACT(ISODOW FROM s.session_start)::INTEGER AS day_of_week,
    TRIM(TO_CHAR(s.session_start, 'Day')) AS day_name,
    TRIM(TO_CHAR(s.session_start, 'Month')) AS month_name,
    EXTRACT(HOUR FROM s.session_start)::INTEGER AS charging_hour,

    -- Customer attributes
    c.home_state,
    c.daily_distance_km,
    c.home_charging_available,

    -- Vehicle attributes
    v.manufacturer,
    v.vehicle_model,
    v.category,

    -- Station attributes
    st.station_state,
    st.station_type,
    st.connector_count

FROM sessions s

INNER JOIN customers c
    ON s.customer_id = c.customer_id

INNER JOIN vehicles v
    ON s.vehicle_id = v.vehicle_id

INNER JOIN stations st
    ON s.station_id = st.station_id