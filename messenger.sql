--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE messages (
    message character varying(255),
    username character varying(30)
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(30),
    password character varying(30)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY messages (message, username) FROM stdin;
lazy in here	lazy
lazy still in here	lazy
hello everybody	taka
fourth message	tmasuda
fifth message	tmasuda
no message	tmasuda
lazy still up in here, in the building	lazy
lazy is out of the building	lazy
finished?	lazy
yess	tmasuda
yes	lazy
back in here	tmasuda
still	tmasuda
still...	tmasuda
lazy's message	lazy
where is ja	tmasuda
where is ja right now?	tmasuda
Hello there world.	taka
hello there again world	taka
first message	tmasuda
second message	tmasuda
third message	tmasuda
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY users (id, username, password) FROM stdin;
37	tmasuda	matsutaka
38	lazy	qwerty
39	taka	masuda
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('users_id_seq', 41, true);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

