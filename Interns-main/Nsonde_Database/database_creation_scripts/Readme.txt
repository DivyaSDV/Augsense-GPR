tblNsDeviceData

CREATE TABLE IF NOT EXISTS public."tblNsDeviceData"
(
    "Deviceid" character varying COLLATE pg_catalog."default" NOT NULL,
    "DeviceName" character varying COLLATE pg_catalog."default" NOT NULL,
    "Timestamp" timestamp with time zone NOT NULL,
    "Latitude" double precision NOT NULL,
    "Longitude" double precision NOT NULL,
    "Altitude" double precision NOT NULL,
    "Location" character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "tblNsDeviceData_pkey" PRIMARY KEY ("Deviceid")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."tblNsDeviceData"
    OWNER to postgres;

tblParameters
CREATE TABLE IF NOT EXISTS public."tblParameters"
(
    "IdParameter" integer NOT NULL DEFAULT nextval('idparameter_seq'::regclass),
    "IdParametertype" integer NOT NULL,
    "Deviceid" character varying COLLATE pg_catalog."default" NOT NULL,
    "Timestamp" timestamp with time zone NOT NULL,
    "Value" double precision NOT NULL,
    CONSTRAINT "tblParameters_pkey" PRIMARY KEY ("IdParameter"),
    CONSTRAINT "Deviceid" FOREIGN KEY ("Deviceid")
        REFERENCES public."tblNsDeviceData" ("Deviceid") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "IdParametertype" FOREIGN KEY ("IdParametertype")
        REFERENCES public."tblParametertype" ("IdParametertype") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."tblParameters"
    OWNER to postgres;

tblParametertype

CREATE TABLE IF NOT EXISTS public."tblParametertype"
(
    "IdParametertype" integer NOT NULL,
    "ParameterName" character varying COLLATE pg_catalog."default" NOT NULL,
    "Unit" character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "tblParametertype_pkey" PRIMARY KEY ("IdParametertype")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."tblParametertype"
    OWNER to postgres;


tblStatus
CREATE TABLE IF NOT EXISTS public."tblStatus"
(
    "IdStatus" integer NOT NULL,
    "IdStatustype" integer NOT NULL,
    "Timestamp" time with time zone NOT NULL,
    "Deviceid" character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "tblStatus_pkey" PRIMARY KEY ("IdStatus"),
    CONSTRAINT "Deviceid" FOREIGN KEY ("Deviceid")
        REFERENCES public."tblNsDeviceData" ("Deviceid") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "IdStatustype" FOREIGN KEY ("IdStatustype")
        REFERENCES public."tblStatustype" ("IdStatustype") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."tblStatus"
    OWNER to postgres;

tblStatustype
CREATE TABLE IF NOT EXISTS public."tblStatustype"
(
    "IdStatustype" integer NOT NULL,
    "Status" character varying(266) COLLATE pg_catalog."default",
    CONSTRAINT "tblStatustype_pkey" PRIMARY KEY ("IdStatustype")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."tblStatustype"
    OWNER to postgres;

