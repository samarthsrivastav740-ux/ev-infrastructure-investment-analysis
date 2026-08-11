--grain: state
SELECT

    state,
    operational_pcs,

    total_sessions,

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
        utilization::NUMERIC,
        3
    ) AS utilization,

    charging_demand_rank,

    utilization_category

FROM {{ ref('int_state_performance') }}