{{
    config(
        materialized='table'
    )
}}

WITH coins AS (
    SELECT
        coin_id,
        coin_name,
        symbol,
        all_time_high,
        all_time_high_date,
        all_time_low,
        all_time_low_date,
        max_supply,
        MAX(extracted_at) AS last_extracted_at
    FROM {{ ref('stg_market_data') }}
    GROUP BY 
        coin_id,
        coin_name,
        symbol,
        all_time_high,
        all_time_high_date,
        all_time_low,
        all_time_low_date,
        max_supply
)

SELECT 
    coin_id,
    coin_name,
    symbol,
    all_time_high,
    all_time_high_date,
    all_time_low,
    all_time_low_date,
    max_supply,
    last_extracted_at
FROM coins
ORDER BY coin_id


