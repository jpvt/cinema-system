FROM postgres:15.1
COPY ./sql/00_config.sql /docker-entrypoint-initdb.d
COPY ./sql/01_ambiente.sql /docker-entrypoint-initdb.d
COPY ./sql/02_filmes.sql /docker-entrypoint-initdb.d
COPY ./sql/03_salas.sql /docker-entrypoint-initdb.d
COPY ./sql/04_sessoes.sql /docker-entrypoint-initdb.d
COPY ./sql/05_clientes.sql /docker-entrypoint-initdb.d
COPY ./sql/06_itens.sql /docker-entrypoint-initdb.d
COPY ./sql/07_compras.sql /docker-entrypoint-initdb.d
COPY ./sql/08_ingressos.sql /docker-entrypoint-initdb.d
