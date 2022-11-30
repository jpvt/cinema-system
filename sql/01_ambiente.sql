-- user
CREATE USER datalakeuser WITH PASSWORD 'jpitawawa';

-- database
CREATE DATABASE datalake;

-- privileges and permissions
REVOKE ALL ON DATABASE datalake FROM public;
ALTER DATABASE datalake OWNER TO datalakeuser;
GRANT CONNECT ON DATABASE datalake to datalakeuser;
ALTER ROLE datalakeuser SET search_path TO public,app;

-- change database and user
\connect datalake datalakeuser

-- schemas
CREATE SCHEMA app;

-- tables
-- TO DO
