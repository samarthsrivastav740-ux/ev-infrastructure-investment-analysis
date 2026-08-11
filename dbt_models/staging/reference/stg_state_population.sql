WITH source AS (

    SELECT *
    FROM {{ source('raw', 'state_population') }}

)

SELECT

    "Rank"::INTEGER AS population_rank,

    (
        CASE
            WHEN "State/Union Territory" = 'Jammu & Kashmir'
                THEN 'Jammu and Kashmir'
            WHEN "State/Union Territory" = 'Andaman & Nicobar Islands'
                THEN 'Andaman and Nicobar Islands'
            WHEN "State/Union Territory" = 'Dadra & Nagar Haveli & Daman & Diu'
                THEN 'Dadra and Nagar Haveli and Daman and Diu'
            ELSE "State/Union Territory"
        END
    )::TEXT AS state,

    "Population_2024"::BIGINT AS population_2024,

    "Type"::TEXT AS state_type

FROM source