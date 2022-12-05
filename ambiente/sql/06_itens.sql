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
);

INSERT INTO app.itens VALUES (
    2, 'Caldo de Cana', 5.99
);

INSERT INTO app.itens VALUES (
    3, 'Suco de Fruta', 7.99
);

INSERT INTO app.itens VALUES (
    4, 'Pipoca P', 7.99
);

INSERT INTO app.itens VALUES (
    5, 'Pipoca M', 10.99
);

INSERT INTO app.itens VALUES (
    6, 'Pipoca G', 12.99
);

INSERT INTO app.itens VALUES (
    7, 'Refri 2L', 15.99
);