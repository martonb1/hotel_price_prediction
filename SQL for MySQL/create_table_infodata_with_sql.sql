CREATE TABLE hotel_info (
    hotel_id INT PRIMARY KEY,
    hotel_name VARCHAR(255),
    brand VARCHAR(100),
    city VARCHAR(100)
);

INSERT INTO hotel_info (hotel_id, hotel_name, brand, city) VALUES
(1, 'Taipei Marriott', 'Marriott', 'Taipei'),
(2, 'Holiday Inn Express Taoyuan', 'IHG', 'Taoyuan'),
(3, 'Four Points by Sheraton Linkou', 'Marriott', 'Linkou'),
(4, 'Humble House Taipei', 'Hilton', 'Taipei');