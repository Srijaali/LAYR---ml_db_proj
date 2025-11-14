ALTER TABLE public.customers
ALTER COLUMN postal_code TYPE character varying(100);

ALTER TABLE public.customers
ALTER COLUMN club_member_status TYPE character varying(100);

ALTER TABLE public.customers
ALTER COLUMN fashion_news_frequency TYPE character varying(100);

select*from customers;