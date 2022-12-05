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

INSERT INTO app.compras VALUES (
    1, 1, 'PIX', 81.89
);

INSERT INTO app.compras VALUES (
    2, 3, 'CARTÃO', 223.83
);

INSERT INTO app.compras VALUES (
    3, 2, 'CARTÃO', 14.29
);
