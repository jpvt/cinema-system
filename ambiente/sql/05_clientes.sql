-- change database and user
\connect datalake datalakeuser

-- Cria tabela de clientes
CREATE TABLE app.clientes (
    id_cliente serial PRIMARY KEY,
    nome text,
    cpf varchar(14),
    telefone varchar(11)
);

INSERT INTO app.clientes VALUES (
    1, 'Junior', '999.333.222-92', '83988884444'
);