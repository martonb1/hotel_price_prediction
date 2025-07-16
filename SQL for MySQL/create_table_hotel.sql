USE hotel_data;

CREATE TABLE hotel_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_name VARCHAR(255),
    check_in DATE,
    check_out DATE,
    price INT
);