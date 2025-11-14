SELECT a.product_group_name,
       a.product_type_name,
       COUNT(t.transaction_id) AS num_sales,
       SUM(t.price) AS total_sales
FROM articles a
JOIN transactions t ON a.article_id = t.article_id
GROUP BY a.product_group_name, a.product_type_name
ORDER BY total_sales DESC;

SELECT
    a.product_group_name,
    a.product_type_name,
    COUNT(DISTINCT t.customer_id) AS unique_customers,
    COUNT(*) AS total_sales,
	COUNT(DISTINCT a.article_id) AS num_articles
FROM
    Transactions t
JOIN
    Articles a ON t.article_id = a.article_id
WHERE
    a.product_type_name IN (
        'Coat', 'Jacket', 'Blazer', 'Hoodie',
        'Trousers', 'Sweater', 'Hat/beanie', 'Beanie',
        'Gloves', 'Boots', 'Blanket', 'Cardigan', 'Leg warmers'
    )
GROUP BY
    a.product_group_name,
    a.product_type_name
ORDER BY
    total_sales DESC;

select article_id, prod_name
from articles
where product_type_name = 'Trousers';

select DISTINCT prod_name
from articles
where product_type_name = 'Trousers';

-- filtering denim,jeans,pants from trousers
SELECT DISTINCT prod_name
FROM articles
WHERE product_type_name = 'Trousers'
AND (
    LOWER(prod_name) LIKE '%jean%' OR
    LOWER(prod_name) LIKE '%pant%' OR
    LOWER(prod_name) LIKE '%denim%'
)
ORDER BY prod_name;

-- checking tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'transactions';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'articles';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'customers';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'articles';


SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'categories';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'orders';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'order_items';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'reviews';

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'events';



SELECT COUNT(*) FROM articles;
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM transactions;


select * from customers;

select * from articles;

select * from transactions;



-- NULL CHECK
SELECT
    COUNT(*) FILTER (WHERE stock = 0) AS null_count,
    COUNT(*) AS total
FROM articles;


SELECT * FROM customers LIMIT 5;


-- CHeking BCNF

-- customers (satisfied)
select DISTINCT(COUNT(customer_id)) - COUNT(*) AS total
from customers


-- articles
select product_code
from articles
group by product_code 
having count(article_id) > 1;

