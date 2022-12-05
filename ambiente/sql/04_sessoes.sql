-- change database and user
\connect datalake datalakeuser

-- Cria tabela de sessoes
CREATE TABLE app.sessoes (
    id_sessao serial PRIMARY KEY,
    id_sala serial,
    id_filme serial,
    total_vendido integer,
    data_sessao date,
    dia_da_semana text,
    tempo_inicio time,
    tempo_final time,
    valor_inteira numeric,

    CONSTRAINT FK_sessoes_salas FOREIGN KEY(id_sala)
        REFERENCES salas(id_sala),

    CONSTRAINT FK_sessoes_filmes FOREIGN KEY(id_filme)
        REFERENCES filmes(id_filme)
    
);

INSERT INTO app.sessoes VALUES (
    1, 1, 1, 1, '2022/12/06', 'Terça-feira', '18:00:00', 
    '20:00:00', 34.90
);

INSERT INTO app.sessoes VALUES (
    2, 5, 6, 7, '2022/12/06', 'Terça-feira', '16:00:00', 
    '18:00:00', 34.90
);

INSERT INTO app.sessoes VALUES (
    3, 2, 6, 0, '2022/12/06', 'Terça-feira', '20:00:00', 
    '22:00:00', 34.90
);

INSERT INTO app.sessoes VALUES (
    4, 2, 6, 0, '2022/12/07', 'Quarta-feira', '20:00:00', 
    '22:00:00', 34.90
);

INSERT INTO app.sessoes VALUES (
    5, 3, 3, 0, '2022/12/06', 'Terça-feira', '14:00:00', 
    '16:00:00', 34.90
);

INSERT INTO app.sessoes VALUES (
    6, 1, 4, 0, '2022/12/06', 'Terça-feira', '16:00:00', 
    '18:00:00', 34.90
);
INSERT INTO app.sessoes VALUES (
    7, 5, 5, 0, '2022/12/06', 'Quarta-feira', '16:00:00', 
    '18:00:00', 34.90
);
INSERT INTO app.sessoes VALUES (
    8, 1, 2, 0, '2022/12/06', 'Terça-feira', '16:00:00', 
    '18:00:00', 34.90
);