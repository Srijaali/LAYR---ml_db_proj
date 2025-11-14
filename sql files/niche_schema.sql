CREATE SCHEMA niche_data;

SET search_path TO niche_data;

CREATE TABLE niche_data.articles AS
SELECT * FROM public.articles
WHERE product_type_name IN ('Jacket', 'Hoodie', 'Beanie')
   OR (product_type_name = 'Trousers' AND section_name IN ('Ladies Denim', 'Denim Men'));

CREATE TABLE niche_data.transactions AS
SELECT * FROM public.transactions
WHERE article_id IN (SELECT article_id FROM niche_data.articles);

CREATE TABLE niche_data.customers AS
SELECT DISTINCT c.*
FROM public.customers c
JOIN niche_data.transactions t USING(customer_id);




SELECT COUNT(*) FROM niche_data.articles;
SELECT COUNT(*) FROM niche_data.transactions;
SELECT COUNT(DISTINCT customer_id) FROM niche_data.customers;



SELECT 
    a.product_type_name,
    COUNT(*) AS transactions,
    COUNT(DISTINCT a.article_id) AS num_articles,
    COUNT(DISTINCT t.customer_id) AS unique_customers,
    ROUND(AVG(t.price), 2) AS avg_price
FROM niche_data.transactions t
JOIN niche_data.articles a ON t.article_id = a.article_id
GROUP BY a.product_type_name
ORDER BY transactions DESC;


UPDATE niche_data.articles SET stock = floor(random() * 300 + 50); 


CREATE TABLE categories AS
SELECT DISTINCT 
  CASE
    WHEN a.product_type_name IN ('Jacket', 'Hoodie') THEN 'Upper Body'
    WHEN a.product_type_name = 'Trousers' THEN 'Lower Body'
    WHEN a.product_type_name = 'Beanie' THEN 'Accessories'
  END AS name;


SELECT * FROM niche_data.articles;
SELECT * FROM niche_data.transactions;
SELECT * FROM niche_data.customers;
select * from niche_data.categories


CREATE TABLE niche_data.orders (LIKE public.orders INCLUDING ALL);
CREATE TABLE niche_data.order_items (LIKE public.order_items INCLUDING ALL);
CREATE TABLE niche_data.reviews (LIKE public.reviews INCLUDING ALL);
CREATE TABLE niche_data.categories (LIKE public.categories INCLUDING ALL);
CREATE TABLE niche_data.events (LIKE public.events INCLUDING ALL);


-- categories

INSERT INTO niche_data.categories (name)
SELECT DISTINCT product_type_name
FROM niche_data.articles
WHERE product_type_name IS NOT NULL;

select * from niche_data.categories

UPDATE niche_data.articles a
SET category_id = c.category_id
FROM niche_data.categories c
WHERE a.product_type_name = c.name;

SELECT COUNT(*) AS total, COUNT(category_id) AS with_category
FROM niche_data.articles;

SELECT a.product_type_name, c.name
FROM niche_data.articles a
JOIN niche_data.categories c USING(category_id);



-- orders
select * from niche_data.orders

select COUNT(*) from niche_data.orders
where payment_status = 'Pending';

INSERT INTO niche_data.orders (customer_id, order_date, total_amount)
SELECT 
    customer_id,
    DATE(t_dat) AS order_date,
    ROUND(SUM(price), 2) AS total_amount
FROM niche_data.transactions
GROUP BY customer_id, DATE(t_dat);

SELECT COUNT(*) FROM niche_data.orders
where payment_status = 'pending';

UPDATE niche_data.orders
SET shipping_address = 
    CONCAT('Street ', (RANDOM() * 100)::INT, ', Karachi, Pakistan');

SELECT o.customer_id, SUM(o.total_amount) AS total_spent
FROM niche_data.orders o
GROUP BY o.customer_id
ORDER BY total_spent DESC
LIMIT 5;


UPDATE niche_data.orders
SET payment_status = CASE
    WHEN order_date >= ((SELECT MAX(order_date) FROM niche_data.orders) - INTERVAL '7 days')
         AND RANDOM() < 0.5 THEN 'Pending'
    WHEN order_date >= ((SELECT MAX(order_date) FROM niche_data.orders) - INTERVAL '30 days')
         AND RANDOM() < 0.15 THEN 'Pending'
    ELSE 'Paid'
END;

SELECT 
    payment_status,
    COUNT(*) AS num_orders,
    MIN(order_date) AS oldest_date,
    MAX(order_date) AS newest_date
FROM niche_data.orders
GROUP BY payment_status
ORDER BY oldest_date;


select 
	MIN(order_date) AS oldest_date,
    MAX(order_date) AS newest_date
from niche_data.orders
where payment_status = 'Pending';


-- order items

select * from niche_data.order_items;

INSERT INTO niche_data.order_items (order_id, article_id, quantity, unit_price)
SELECT 
    o.order_id,
    t.article_id,
    1 AS quantity,
    ROUND(t.price, 2) AS unit_price
FROM niche_data.transactions t
JOIN niche_data.orders o
  ON t.customer_id = o.customer_id
 AND DATE(t.t_dat) = o.order_date;

SELECT COUNT(*) FROM niche_data.order_items;

SELECT o.order_id, COUNT(*) AS num_items, SUM(oi.line_total) AS total
FROM niche_data.order_items oi
JOIN niche_data.orders o USING(order_id)
GROUP BY o.order_id
ORDER BY total DESC
LIMIT 10;


UPDATE niche_data.order_items
SET quantity = CASE
    WHEN RANDOM() < 0.7 THEN 1
    WHEN RANDOM() < 0.9 THEN 2
    ELSE 3
END;

--UPDATE niche_data.order_items
--SET line_total = quantity * unit_price;

--line_total NUMERIC(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED

/*
UPDATE niche_data.orders o
SET total_amount = (
    SELECT ROUND(SUM(line_total), 2)
    FROM niche_data.order_items oi
    WHERE oi.order_id = o.order_id
);
*/


SELECT o.order_id, c.first_name, a.prod_name, oi.quantity, oi.unit_price
FROM niche_data.orders o
JOIN niche_data.order_items oi USING(order_id)
JOIN niche_data.articles a USING(article_id)
JOIN niche_data.customers c USING(customer_id)
LIMIT 10;


CREATE INDEX idx_order_items_order_id ON niche_data.order_items(order_id);

UPDATE niche_data.orders o
SET total_amount = rounded.total_amount
FROM (
    SELECT order_id, ROUND(SUM(line_total), 2) AS total_amount
    FROM niche_data.order_items
    GROUP BY order_id
) AS rounded
WHERE o.order_id = rounded.order_id;



-- reviews

select * from articles;
select*from customers;
select*from transactions fetch first 3 rows only;
select*from categories;
select*from events; --empty
select*from orders; --empty
select*from order_items;
select*from reviews; --empty

SELECT * FROM articles WHERE article_id = '108775015';

