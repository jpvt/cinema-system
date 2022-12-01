-- change database and user
\connect datalake datalakeuser

-- Cria tabela de filmes
CREATE TABLE app.salas (
    id_sala serial PRIMARY KEY,
    capacidade integer
);

INSERT INTO app.salas VALUES (1, 10);
INSERT INTO app.salas VALUES (2, 20);
INSERT INTO app.salas VALUES (3, 30);
INSERT INTO app.salas VALUES (4, 40);
INSERT INTO app.salas VALUES (5, 50);
