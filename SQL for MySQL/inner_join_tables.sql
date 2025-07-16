SELECT
    p.id,
    p.hotel_name,
    i.brand,
    i.city,
    p.check_in,
    p.check_out,
    p.price
FROM
    hotel_prices p
JOIN
    hotel_info i
ON
    p.hotel_name = i.hotel_name
ORDER BY
    i.brand, p.price DESC;