
-- change database and user
\connect datalake datalakeuser

-- Cria tabela de filmes
CREATE TABLE app.label (
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
