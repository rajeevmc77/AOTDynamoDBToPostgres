-- Table: public.tempcompletedorders

-- DROP TABLE public.tempcompletedorders;

CREATE TABLE public.tempcompletedorders
(
    "organizationId" character varying COLLATE pg_catalog."default" NOT NULL,
    "orderNumber" character varying COLLATE pg_catalog."default" NOT NULL,
    "locationId" character varying COLLATE pg_catalog."default",
    "totalPrice" numeric(7,2),
    "orderVia" character varying COLLATE pg_catalog."default",
    "subTotal" numeric(7,2),
    "orderedDate" timestamp without time zone ,
    data json
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tempcompletedorders
	ADD COLUMN id SERIAL PRIMARY KEY;

ALTER TABLE public.tempcompletedorders
    OWNER to postgres;
	

GRANT INSERT, SELECT ON TABLE public.tempcompletedorders TO appuser;

GRANT ALL ON TABLE public.tempcompletedorders TO postgres;