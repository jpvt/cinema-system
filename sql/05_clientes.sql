-- change database and user
\connect datalake datalakeuser

-- Cria tabela de clientes
CREATE TABLE app.clientes (
    id_cliente serial PRIMARY KEY,
    nome text,
    cpf varchar(14),
    telefone varchar(11)
);
