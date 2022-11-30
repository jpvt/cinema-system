-- change database and user
\connect datalake datalakeuser

-- Cria tabela de pedidos
CREATE TABLE app.pedidos (
    id_pedido serial PRIMARY KEY,
    id_item serial,
    id_compra serial,

    CONSTRAINT FK_pedidos_itens FOREIGN KEY(id_item)
        REFERENCES itens(id_item),
    CONSTRAINT FK_pedidos_compras FOREIGN KEY(id_compra)
        REFERENCES compras(id_compra)
);