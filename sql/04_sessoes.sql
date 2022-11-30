-- change database and user
\connect datalake datalakeuser

-- SESSÕES (1,1): Cada linha representa uma sessão de filme
-- id_sessao PK SERIAL: ID da sessão
-- id_sala FK SERIAL: ID da sala onde ocorre a sessão
-- id_filme FK SERIAL: ID do filme que vai passar na sessão
-- total_vendido INTEGER: total de ingressos vendidos
-- data DATE: data da sessão
-- dia_da_semana TEXT: Dia da semana da sessão
-- tempo_inicio TIMESTAMP: Horário de início da sessão
-- tempo_final TIMESTAMP: Horário final da sessão
-- valor NUMERIC: Valor de uma inteira nessa sessão

-- Cria tabela de filmes
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
