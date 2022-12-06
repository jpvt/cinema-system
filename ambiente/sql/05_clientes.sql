-- change database and user
\connect datalake datalakeuser

-- Cria tabela de clientes
CREATE TABLE app.clientes (
    id_cliente varchar(14) PRIMARY KEY,
    nome text,
    telefone varchar(11)
);

INSERT INTO app.clientes VALUES (
    '999.333.222-92', 'Junior', '83988884444'
);

INSERT INTO app.clientes VALUES (
    '888.333.222-92', 'Aldemar', '83988884454'
);

INSERT INTO app.clientes VALUES (
    '777.333.222-92', 'Vladimir', '83988884455'
);