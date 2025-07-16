SELECT
    hotel_name,
    COUNT(*) AS num_samples,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM
    hotel_prices
GROUP BY
    hotel_name
ORDER BY
    max_price DESC;