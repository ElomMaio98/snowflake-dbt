{{
    config(
        materialized='table'
    )
}}

SELECT
    coin_id,
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
    last_updated,
    extracted_at
FROM {{ ref('stg_market_data') }}
ORDER BY market_cap_rank