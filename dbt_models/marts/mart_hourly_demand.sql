--grain: 1 charging hour
SELECT

    charging_hour,
    total_sessions,
    customers_served,

    ROUND(
        total_energy_delivered_kwh::NUMERIC,
        3
    ) AS total_energy_delivered_kwh

FROM {{ ref('int_hourly_demand') }}