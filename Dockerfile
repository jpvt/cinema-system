FROM postgres:15.1
COPY ./sql/00_config.sql /docker-entrypoint-initdb.d
COPY ./sql/01_ambiente.sql /docker-entrypoint-initdb.d
COPY ./sql/02_filmes.sql /docker-entrypoint-initdb.d
