USE sales_analytics_db;


-- =========================================================
-- Customers
-- =========================================================

INSERT INTO customers
    (customer_id, name, email, city, country, signup_date)
VALUES
    (1, 'Alice Martin', 'alice@example.com', 'Paris', 'France', '2024-01-15'),
    (2, 'Bob Sharma', 'bob@example.com', 'Mumbai', 'India', '2024-02-10'),
    (3, 'Charlie Brown', 'charlie@example.com', 'New York', 'USA', '2024-03-05'),
    (4, 'Diya Patel', 'diya@example.com', 'Ahmedabad', 'India', '2024-04-18'),
    (5, 'Ethan Wilson', 'ethan@example.com', 'London', 'United Kingdom', '2024-05-22'),
    (6, 'Fatima Khan', 'fatima@example.com', 'Dubai', 'UAE', '2024-06-12'),
    (7, 'George Miller', 'george@example.com', 'Berlin', 'Germany', '2024-07-08'),
    (8, 'Hannah Lee', 'hannah@example.com', 'Singapore', 'Singapore', '2024-08-01');


-- =========================================================
-- Categories
-- =========================================================

INSERT INTO categories
    (category_id, category_name)
VALUES
    (1, 'Laptops'),
    (2, 'Smartphones'),
    (3, 'Tablets'),
    (4, 'Accessories'),
    (5, 'Audio');


-- =========================================================
-- Products
-- =========================================================

INSERT INTO products
    (product_id, product_name, category_id, unit_price, stock_quantity)
VALUES
    (1, 'ProBook Laptop',       1, 1200.00, 25),
    (2, 'UltraSlim Laptop',     1, 1500.00, 18),
    (3, 'SmartPhone X',         2,  800.00, 40),
    (4, 'SmartPhone Mini',      2,  600.00, 35),
    (5, 'Tab Pro',              3,  650.00, 30),
    (6, 'Tab Lite',             3,  450.00, 28),
    (7, 'Wireless Mouse',       4,   40.00, 100),
    (8, 'Mechanical Keyboard',  4,   90.00, 75),
    (9, 'NoiseCancel Headset',  5,  180.00, 50),
    (10, 'Wireless Earbuds',    5,  120.00, 60);

-- =========================================================
-- Orders
-- =========================================================

INSERT INTO orders
    (order_id, customer_id, order_date, status, shipping_country)
VALUES
    (1,  1, '2024-03-12', 'Delivered', 'France'),
    (2,  2, '2024-04-05', 'Delivered', 'India'),
    (3,  3, '2024-05-18', 'Delivered', 'USA'),
    (4,  4, '2024-06-09', 'Delivered', 'India'),
    (5,  5, '2024-07-21', 'Delivered', 'United Kingdom'),
    (6,  6, '2024-08-14', 'Delivered', 'UAE'),
    (7,  7, '2024-09-03', 'Delivered', 'Germany'),
    (8,  8, '2024-10-11', 'Delivered', 'Singapore'),
    (9,  2, '2024-11-24', 'Delivered', 'India'),
    (10, 4, '2025-01-15', 'Delivered', 'India'),
    (11, 1, '2025-02-20', 'Shipped',   'France'),
    (12, 3, '2025-03-05', 'Processing','USA');


-- =========================================================
-- Order Items
-- =========================================================

INSERT INTO order_items
    (order_item_id, order_id, product_id, quantity, unit_price)
VALUES
    (1,  1, 1,  1, 1200.00),
    (2,  1, 7,  1,   40.00),

    (3,  2, 3,  1,  800.00),
    (4,  2, 10, 1,  120.00),

    (5,  3, 2,  1, 1500.00),
    (6,  3, 8,  1,   90.00),

    (7,  4, 5,  1,  650.00),
    (8,  4, 9,  1,  180.00),

    (9,  5, 6,  2,  450.00),
    (10, 5, 7,  1,   40.00),

    (11, 6, 3,  1,  800.00),
    (12, 6, 9,  2,  180.00),

    (13, 7, 1,  1, 1150.00),
    (14, 7, 8,  1,   85.00),

    (15, 8, 4,  1,  600.00),
    (16, 8, 10, 2,  120.00),

    (17, 9, 2,  1, 1450.00),
    (18, 9, 7,  2,   40.00),

    (19, 10, 1, 1, 1180.00),
    (20, 10, 9, 1,  175.00),

    (21, 11, 5, 1,  625.00),
    (22, 11, 10, 1, 115.00),

    (23, 12, 4, 1,  590.00),
    (24, 12, 8, 1,   90.00);