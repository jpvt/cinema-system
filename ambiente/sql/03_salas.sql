-- change database and user
\connect datalake datalakeuser

-- Cria tabela de filmes
CREATE TABLE app.salas (
    id_sala serial PRIMARY KEY CHECK (id_sala < 46),
    capacidade integer
);

INSERT INTO app.salas VALUES (1, 64);
INSERT INTO app.salas VALUES (2, 96);
INSERT INTO app.salas VALUES (3, 128);
INSERT INTO app.salas VALUES (4, 160);
INSERT INTO app.salas VALUES (5, 192);
