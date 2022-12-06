-- change database and user
\connect datalake datalakeuser

-- Cria tabela de ingressos
CREATE TABLE app.ingressos (
    id_ingresso serial PRIMARY KEY,
    id_compra serial,
    id_sessao serial,
    assento text,
    tipo_ingresso text,

    CONSTRAINT FK_ingressos_compras FOREIGN KEY(id_compra)
        REFERENCES compras(id_compra)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT FK_ingressos_sessoes FOREIGN KEY(id_sessao)
        REFERENCES sessoes(id_sessao)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO app.ingressos VALUES (
    1, 1, 1, 'A7', 'Adulto'
);


INSERT INTO app.ingressos VALUES (
    2, 2, 2, 'E2', 'Adulto'
);


INSERT INTO app.ingressos VALUES (
    3, 2, 2, 'E3', 'Adulto'
);


INSERT INTO app.ingressos VALUES (
    4, 2, 2, 'E4', 'Adulto'
);

INSERT INTO app.ingressos VALUES (
    5, 2, 2, 'E5', 'Adulto'
);

INSERT INTO app.ingressos VALUES (
    6, 2, 2, 'E6', 'Adulto'
);

INSERT INTO app.ingressos VALUES (
    7, 3, 2, 'D7', 'Flamenguista'
);

INSERT INTO app.ingressos VALUES (
    8, 3, 2, 'D8', 'Flamenguista'
);
