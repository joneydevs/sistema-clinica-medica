--
-- PostgreSQL database dump
--

\restrict 0mPhRjZ35KabcXnmHBCLv1Osb669h34bZFrH3NYnJSYPn6ofLwEYeRhSUl1Sdnv

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg13+1)
-- Dumped by pg_dump version 18.3 (Debian 18.3-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: paciente_email_minusculo(); Type: FUNCTION; Schema: public; Owner: joney
--

CREATE FUNCTION public.paciente_email_minusculo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.email := LOWER(NEW.email);
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.paciente_email_minusculo() OWNER TO joney;

--
-- Name: profissional_email_minusculo(); Type: FUNCTION; Schema: public; Owner: joney
--

CREATE FUNCTION public.profissional_email_minusculo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.email := LOWER(NEW.email);
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.profissional_email_minusculo() OWNER TO joney;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: consulta; Type: TABLE; Schema: public; Owner: joney
--

CREATE TABLE public.consulta (
    id integer NOT NULL,
    paciente_id integer NOT NULL,
    profissional_id integer NOT NULL,
    data_hora timestamp without time zone NOT NULL,
    status character varying(20) NOT NULL,
    obs text,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT consulta_status_check CHECK (((status)::text = ANY ((ARRAY['MARCADA'::character varying, 'CANCELADA'::character varying, 'REALIZADA'::character varying])::text[])))
);


ALTER TABLE public.consulta OWNER TO joney;

--
-- Name: consulta_id_seq; Type: SEQUENCE; Schema: public; Owner: joney
--

ALTER TABLE public.consulta ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.consulta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: paciente; Type: TABLE; Schema: public; Owner: joney
--

CREATE TABLE public.paciente (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    celular text NOT NULL,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT paciente_email_check CHECK (((email)::text ~ '^[^@]+@[^@]+\.[^@]+$'::text))
);


ALTER TABLE public.paciente OWNER TO joney;

--
-- Name: paciente_id_seq; Type: SEQUENCE; Schema: public; Owner: joney
--

ALTER TABLE public.paciente ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.paciente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: profissional; Type: TABLE; Schema: public; Owner: joney
--

CREATE TABLE public.profissional (
    id integer NOT NULL,
    nome character varying(100) NOT NULL,
    especialidade character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    celular text NOT NULL,
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT profissional_email_check CHECK (((email)::text ~ '^[^@]+@[^@]+\.[^@]+$'::text))
);


ALTER TABLE public.profissional OWNER TO joney;

--
-- Name: profissional_id_seq; Type: SEQUENCE; Schema: public; Owner: joney
--

ALTER TABLE public.profissional ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.profissional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: consulta consulta_paciente_id_data_hora_key; Type: CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.consulta
    ADD CONSTRAINT consulta_paciente_id_data_hora_key UNIQUE (paciente_id, data_hora);


--
-- Name: consulta consulta_pkey; Type: CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.consulta
    ADD CONSTRAINT consulta_pkey PRIMARY KEY (id);


--
-- Name: consulta consulta_profissional_id_data_hora_key; Type: CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.consulta
    ADD CONSTRAINT consulta_profissional_id_data_hora_key UNIQUE (profissional_id, data_hora);


--
-- Name: paciente paciente_email_key; Type: CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_email_key UNIQUE (email);


--
-- Name: paciente paciente_pkey; Type: CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_pkey PRIMARY KEY (id);


--
-- Name: profissional profissional_email_key; Type: CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.profissional
    ADD CONSTRAINT profissional_email_key UNIQUE (email);


--
-- Name: profissional profissional_pkey; Type: CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.profissional
    ADD CONSTRAINT profissional_pkey PRIMARY KEY (id);


--
-- Name: idx_paciente_id; Type: INDEX; Schema: public; Owner: joney
--

CREATE INDEX idx_paciente_id ON public.consulta USING btree (paciente_id, data_hora);


--
-- Name: idx_profissional_id; Type: INDEX; Schema: public; Owner: joney
--

CREATE INDEX idx_profissional_id ON public.consulta USING btree (profissional_id, data_hora);


--
-- Name: paciente trg_email_minusculo; Type: TRIGGER; Schema: public; Owner: joney
--

CREATE TRIGGER trg_email_minusculo BEFORE INSERT OR UPDATE ON public.paciente FOR EACH ROW EXECUTE FUNCTION public.paciente_email_minusculo();


--
-- Name: profissional trg_email_minusculo2; Type: TRIGGER; Schema: public; Owner: joney
--

CREATE TRIGGER trg_email_minusculo2 BEFORE INSERT OR UPDATE ON public.profissional FOR EACH ROW EXECUTE FUNCTION public.profissional_email_minusculo();


--
-- Name: consulta consulta_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.consulta
    ADD CONSTRAINT consulta_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.paciente(id) ON DELETE RESTRICT;


--
-- Name: consulta consulta_profissional_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: joney
--

ALTER TABLE ONLY public.consulta
    ADD CONSTRAINT consulta_profissional_id_fkey FOREIGN KEY (profissional_id) REFERENCES public.profissional(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict 0mPhRjZ35KabcXnmHBCLv1Osb669h34bZFrH3NYnJSYPn6ofLwEYeRhSUl1Sdnv

