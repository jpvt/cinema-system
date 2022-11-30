-- change database and user
\connect datalake datalakeuser

-- Cria tabela de compras
CREATE TABLE app.compras (
    id_compra serial PRIMARY KEY,
    id_cliente serial,
    tipo_pagamento text,
    valor_total numeric,

    CONSTRAINT FK_compras_clientes FOREIGN KEY(id_cliente)
        REFERENCES clientes(id_cliente)
);
