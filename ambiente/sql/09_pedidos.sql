-- change database and user
\connect datalake datalakeuser

-- Cria tabela de pedidos
CREATE TABLE app.pedidos (
    id_pedido serial PRIMARY KEY,
    id_item serial,
    id_compra serial,

    CONSTRAINT FK_pedidos_itens FOREIGN KEY(id_item)
        REFERENCES itens(id_item)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT FK_pedidos_compras FOREIGN KEY(id_compra)
        REFERENCES compras(id_compra)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO app.pedidos VALUES (
    1, 1, 1
);

INSERT INTO app.pedidos VALUES (
    2, 6, 3
);

INSERT INTO app.pedidos VALUES (
    3, 7, 3
);

INSERT INTO app.pedidos VALUES (
    4, 6, 2
);
