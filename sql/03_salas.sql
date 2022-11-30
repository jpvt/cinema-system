-- change database and user
\connect datalake datalakeuser

-- Cria tabela de filmes
CREATE TABLE app.salas (
    id_sala serial PRIMARY KEY,
    capacidade integer
);
