WITH source AS (

    SELECT *
    FROM {{ source('raw', 'ev_sales_by_makers') }}

)

SELECT

    CASE
        WHEN "Cat" = 'LMV' THEN '4W'
        ELSE "Cat"
    END AS category,

    CASE

        WHEN "Maker" IN (
            'AMPERE VEHICLES PRIVATE LIMITED',
            'AMPERE VEHICLES PVT LTD'
        ) THEN 'Ampere'

        WHEN "Maker" = 'ATHER ENERGY PVT LTD'
            THEN 'Ather'

        WHEN "Maker" = 'AUDI AG'
            THEN 'Audi'

        WHEN "Maker" = 'BAJAJ AUTO LTD'
            THEN 'Bajaj'

        WHEN "Maker" = 'BGAUSS AUTO PRIVATE LIMITED'
            THEN 'BGauss'

        WHEN "Maker" = 'BMW INDIA PVT LTD'
            THEN 'BMW'

        WHEN "Maker" IN (
            'BYD AUTO',
            'BYD INDIA PRIVATE LIMITED'
        ) THEN 'BYD'

        WHEN "Maker" = 'HERO MOTOCORP LTD'
            THEN 'Hero MotoCorp'

        WHEN "Maker" = 'HYUNDAI MOTOR INDIA LTD'
            THEN 'Hyundai'

        WHEN "Maker" = 'JAGUAR LAND ROVER INDIA LIMITED'
            THEN 'Jaguar'

        WHEN "Maker" = 'KIA INDIA PRIVATE LIMITED'
            THEN 'Kia'

        WHEN "Maker" IN (
            'MAHINDRA & MAHINDRA LIMITED',
            'MAHINDRA ELECTRIC MOBILITY LIMITED',
            'MAHINDRA LAST MILE MOBILITY LTD'
        ) THEN 'Mahindra'

        WHEN "Maker" IN (
            'MERCEDES-BENZ AG',
            'MERCEDES-BENZ INDIA PVT LTD'
        ) THEN 'Mercedes-Benz'

        WHEN "Maker" = 'MG MOTOR INDIA PVT LTD'
            THEN 'MG Motor'

        WHEN "Maker" = 'OBEN ELECTRIC VEHICLES PVT LTD'
            THEN 'Oben'

        WHEN "Maker" = 'OKAYA EV PVT LTD'
            THEN 'Okaya'

        WHEN "Maker" = 'OLA ELECTRIC TECHNOLOGIES PVT LTD'
            THEN 'Ola Electric'

        WHEN "Maker" = 'PORSCHE AG GERMANY'
            THEN 'Porsche'

        WHEN "Maker" = 'RIVER MOBILITY PVT LTD'
            THEN 'River'

        WHEN "Maker" IN (
            'TATA MOTORS LTD',
            'TATA MOTORS PASSENGER VEHICLES LTD',
            'TATA PASSENGER ELECTRIC MOBILITY LTD'
        ) THEN 'Tata'

        WHEN "Maker" = 'TORK MOTORS PVT LTD'
            THEN 'Tork Motors'

        WHEN "Maker" = 'TVS MOTOR COMPANY LTD'
            THEN 'TVS'

        WHEN "Maker" = 'ULTRAVIOLETTE AUTOMOTIVE PVT LTD'
            THEN 'Ultraviolette'

        WHEN "Maker" = 'VOLVO AUTO INDIA PVT LTD'
            THEN 'Volvo'

    END AS manufacturer,

    "2015"::BIGINT AS sales_2015,
    "2016"::BIGINT AS sales_2016,
    "2017"::BIGINT AS sales_2017,
    "2018"::BIGINT AS sales_2018,
    "2019"::BIGINT AS sales_2019,
    "2020"::BIGINT AS sales_2020,
    "2021"::BIGINT AS sales_2021,
    "2022"::BIGINT AS sales_2022,
    "2023"::BIGINT AS sales_2023,
    "2024"::BIGINT AS sales_2024

FROM source

WHERE
    "Cat" IN ('2W', 'LMV')
    AND "Maker" IN (

        'AMPERE VEHICLES PRIVATE LIMITED',
        'AMPERE VEHICLES PVT LTD',
        'ATHER ENERGY PVT LTD',
        'AUDI AG',
        'BAJAJ AUTO LTD',
        'BGAUSS AUTO PRIVATE LIMITED',
        'BMW INDIA PVT LTD',
        'BYD AUTO',
        'BYD INDIA PRIVATE LIMITED',
        'HERO MOTOCORP LTD',
        'HYUNDAI MOTOR INDIA LTD',
        'JAGUAR LAND ROVER INDIA LIMITED',
        'KIA INDIA PRIVATE LIMITED',
        'MAHINDRA & MAHINDRA LIMITED',
        'MAHINDRA ELECTRIC MOBILITY LIMITED',
        'MAHINDRA LAST MILE MOBILITY LTD',
        'MERCEDES-BENZ AG',
        'MERCEDES-BENZ INDIA PVT LTD',
        'MG MOTOR INDIA PVT LTD',
        'OBEN ELECTRIC VEHICLES PVT LTD',
        'OKAYA EV PVT LTD',
        'OLA ELECTRIC TECHNOLOGIES PVT LTD',
        'PORSCHE AG GERMANY',
        'RIVER MOBILITY PVT LTD',
        'TATA MOTORS LTD',
        'TATA MOTORS PASSENGER VEHICLES LTD',
        'TATA PASSENGER ELECTRIC MOBILITY LTD',
        'TORK MOTORS PVT LTD',
        'TVS MOTOR COMPANY LTD',
        'ULTRAVIOLETTE AUTOMOTIVE PVT LTD',
        'VOLVO AUTO INDIA PVT LTD'

    )