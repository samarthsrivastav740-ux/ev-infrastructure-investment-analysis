-- grain 1 charging hour
WITH hourly_demand AS (

    SELECT
        charging_hour,

        COUNT(session_id) AS total_sessions,

        COUNT(DISTINCT customer_id) AS customers_served,

        SUM(energy_delivered_kwh) AS total_energy_delivered_kwh

    FROM {{ ref('int_session_enriched') }}

    GROUP BY
        charging_hour

)

SELECT
    charging_hour,
    total_sessions,
    customers_served,
    total_energy_delivered_kwh

FROM hourly_demand

ORDER BY
    charging_hour