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
