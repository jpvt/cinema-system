-- change database and user
\connect datalake datalakeuser

-- Cria tabela de itens
CREATE TABLE app.itens (
    id_item serial PRIMARY KEY,
    descricao text,
    valor_item numeric
);

INSERT INTO app.itens VALUES (
    1, 'Bolo Fubica', 45.99
)
