-- Table: public.articles

-- DROP TABLE IF EXISTS public.articles;

CREATE TABLE IF NOT EXISTS public.articles
(
    article_id character varying COLLATE pg_catalog."default" NOT NULL,
    product_code integer,
    prod_name text COLLATE pg_catalog."default",
    product_type_name text COLLATE pg_catalog."default",
    product_group_name text COLLATE pg_catalog."default",
    graphical_appearance_name text COLLATE pg_catalog."default",
    colour_group_name text COLLATE pg_catalog."default",
    department_no text COLLATE pg_catalog."default",
    department_name text COLLATE pg_catalog."default",
    index_name text COLLATE pg_catalog."default",
    index_group_name text COLLATE pg_catalog."default",
    section_name text COLLATE pg_catalog."default",
    garment_group_name text COLLATE pg_catalog."default",
    detail_desc text COLLATE pg_catalog."default",
    price numeric(10,2),
    stock integer DEFAULT 0,
    category_id integer,
    CONSTRAINT articles_pkey PRIMARY KEY (article_id),
    CONSTRAINT fk_articles_category FOREIGN KEY (category_id)
        REFERENCES public.categories (category_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.articles
    OWNER to postgres;
-- Index: idx_articles_price

-- DROP INDEX IF EXISTS public.idx_articles_price;

CREATE INDEX IF NOT EXISTS idx_articles_price
    ON public.articles USING btree
    (price ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;

