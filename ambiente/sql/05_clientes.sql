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

INSERT INTO app.clientes VALUES (
    2, 'Aldemar', '888.333.222-92', '83988884454'
);

INSERT INTO app.clientes VALUES (
    3, 'Vladimir', '777.333.222-92', '83988884455'
);