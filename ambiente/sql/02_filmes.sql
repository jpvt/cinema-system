
-- change database and user
\connect datalake datalakeuser

-- Cria tabela de filmes
CREATE TABLE app.filmes (
    id_filme serial PRIMARY KEY,
    nome text,
    categoria text,
    censura text,
    atores_principais text,
    duracao time,
    produtora text,
    nacional boolean,
	descricao text NULL
);

-- Mock
INSERT INTO app.filmes VALUES (
    1, 'Eurotrip', 'comedia', '16', 'Michael Cera, etc', '01:50:00',
    'MGM', false, 'Um filme muito alto astral sobre amigos viajando na europa'
);
