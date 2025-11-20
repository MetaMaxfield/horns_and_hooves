--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg110+2)
-- Dumped by pg_dump version 16.4 (Debian 16.4-1.pgdg110+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO postgres;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO postgres;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activities (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    parent_id integer
);


ALTER TABLE public.activities OWNER TO postgres;

--
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activities_id_seq OWNER TO postgres;

--
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: buildings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.buildings (
    id integer NOT NULL,
    address character varying(200) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    geom public.geometry(Point,4326) NOT NULL,
    CONSTRAINT latitude_range CHECK (((latitude >= ('-90.0'::numeric)::double precision) AND (latitude <= (90.0)::double precision))),
    CONSTRAINT longitude_range CHECK (((longitude >= ('-180.0'::numeric)::double precision) AND (longitude <= (180.0)::double precision)))
);


ALTER TABLE public.buildings OWNER TO postgres;

--
-- Name: buildings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.buildings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.buildings_id_seq OWNER TO postgres;

--
-- Name: buildings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.buildings_id_seq OWNED BY public.buildings.id;


--
-- Name: organization_activities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization_activities (
    organization_id integer NOT NULL,
    activity_id integer NOT NULL
);


ALTER TABLE public.organization_activities OWNER TO postgres;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organizations (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    building_id integer NOT NULL
);


ALTER TABLE public.organizations OWNER TO postgres;

--
-- Name: organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organizations_id_seq OWNER TO postgres;

--
-- Name: organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organizations_id_seq OWNED BY public.organizations.id;


--
-- Name: phone_numbers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phone_numbers (
    id integer NOT NULL,
    num character varying(16) NOT NULL,
    organization_id integer NOT NULL
);


ALTER TABLE public.phone_numbers OWNER TO postgres;

--
-- Name: phone_numbers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.phone_numbers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.phone_numbers_id_seq OWNER TO postgres;

--
-- Name: phone_numbers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.phone_numbers_id_seq OWNED BY public.phone_numbers.id;


--
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- Name: buildings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.buildings ALTER COLUMN id SET DEFAULT nextval('public.buildings_id_seq'::regclass);


--
-- Name: organizations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations ALTER COLUMN id SET DEFAULT nextval('public.organizations_id_seq'::regclass);


--
-- Name: phone_numbers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_numbers ALTER COLUMN id SET DEFAULT nextval('public.phone_numbers_id_seq'::regclass);


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activities (id, name, parent_id) FROM stdin;
1	Еда	\N
2	Автомобили	\N
3	Мясная продукция	1
4	Молочная продукция	1
5	Грузовые	2
6	Легковые	2
7	Запчасти	6
8	Аксессуары	6
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
a4b4f1aee889
\.


--
-- Data for Name: buildings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.buildings (id, address, latitude, longitude, geom) FROM stdin;
1	г. Москва, ул. Блюхера, 32/1	55.751244	37.618423	0101000020E61000000F0C207C28CF42407AA86DC328E04B40
2	г. Санкт-Петербург, Невский проспект, 28	59.93428	30.335099	0101000020E61000001CEC4D0CC9553E4048A7AE7C96F74D40
3	г. Новосибирск, ул. Ленина, 1, офис 3	55.030204	82.92043	0101000020E610000077103B53E8BA5440AC1A84B9DD834B40
4	г. Екатеринбург, ул. Малышева, 15	56.843684	60.645447	0101000020E61000009126DE019E524E4049145AD6FD6B4C40
5	г. Казань, ул. Баумана, 58	55.796127	49.106414	0101000020E610000014EB54F99E8D4840363B527DE7E54B40
\.


--
-- Data for Name: organization_activities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization_activities (organization_id, activity_id) FROM stdin;
1	1
2	4
3	6
3	7
4	5
5	2
6	3
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organizations (id, name, building_id) FROM stdin;
1	ООО "Рога и Копыта"	1
2	ЗАО "Молочный завод №1"	2
3	ИП Петров А.В. "АвтоЗапчасти"	3
4	ООО "ГрузАвто Сервис"	4
5	Автосалон "Премиум Авто"	5
6	ООО "Мясокомбинат Сибирский"	3
\.


--
-- Data for Name: phone_numbers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.phone_numbers (id, num, organization_id) FROM stdin;
37	+79995155020	1
38	+79995155012	1
39	+79236661313	1
40	+78121234567	2
41	+78127654321	2
42	+73835551234	3
43	+73437778899	4
44	+73431112233	4
45	+79001234567	4
46	+78439990011	5
47	+73834445566	6
48	+73837778899	6
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: activities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.activities_id_seq', 1, false);


--
-- Name: buildings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.buildings_id_seq', 6, true);


--
-- Name: organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organizations_id_seq', 18, true);


--
-- Name: phone_numbers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.phone_numbers_id_seq', 48, true);


--
-- Name: topology_id_seq; Type: SEQUENCE SET; Schema: topology; Owner: postgres
--

SELECT pg_catalog.setval('topology.topology_id_seq', 1, false);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: buildings buildings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (id);


--
-- Name: organization_activities organization_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_activities
    ADD CONSTRAINT organization_activities_pkey PRIMARY KEY (organization_id, activity_id);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: phone_numbers phone_numbers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_numbers
    ADD CONSTRAINT phone_numbers_pkey PRIMARY KEY (id);


--
-- Name: idx_buildings_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_buildings_geom ON public.buildings USING gist (geom);


--
-- Name: activities activities_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- Name: organization_activities organization_activities_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_activities
    ADD CONSTRAINT organization_activities_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- Name: organization_activities organization_activities_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_activities
    ADD CONSTRAINT organization_activities_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: organizations organizations_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.buildings(id) ON DELETE CASCADE;


--
-- Name: phone_numbers phone_numbers_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_numbers
    ADD CONSTRAINT phone_numbers_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

