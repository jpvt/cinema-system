-- change database and user
\connect datalake datalakeuser

-- Cria tabela de itens
CREATE TABLE app.itens (
    id_item serial PRIMARY KEY,
    descricao text,
    valor_item numeric
);
