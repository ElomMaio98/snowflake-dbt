{{
    config(
        materialized='view'
    )
}}

WITH source_data AS (
    SELECT
        id AS coin_id,
        symbol,
        name AS coin_name,
        current_price,
        market_cap,
        market_cap_rank,
        total_volume,
        high_24h,
        low_24h,
        price_change_24h,
        price_change_percentage_24h,
        price_change_percentage_7d,
        price_change_percentage_30d,
        circulating_supply,
        total_supply,
        max_supply,
        ath AS all_time_high,
        ath_date AS all_time_high_date,
        atl AS all_time_low,
        atl_date AS all_time_low_date,
        last_updated,
        extracted_at
    FROM {{ source('raw', 'market_data') }}
    WHERE market_cap_rank IS NOT NULL
)

SELECT * FROM source_data