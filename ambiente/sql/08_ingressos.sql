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
        REFERENCES compras(id_compra),
    CONSTRAINT FK_ingressos_sessoes FOREIGN KEY(id_sessao)
        REFERENCES sessoes(id_sessao)
);

INSERT INTO app.ingressos VALUES (
    1, 1, 1, 'K7', 'Inteira'
);
