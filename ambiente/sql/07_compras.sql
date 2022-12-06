-- change database and user
\connect datalake datalakeuser

-- Cria tabela de compras
CREATE TABLE app.compras (
    id_compra serial PRIMARY KEY,
    id_cliente varchar(14),
    tipo_pagamento text,
    valor_total numeric,

    CONSTRAINT FK_compras_clientes FOREIGN KEY(id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO app.compras VALUES (
    1, '999.333.222-92', 'PIX', 81.89
);

INSERT INTO app.compras VALUES (
    2, '777.333.222-92', 'CARTÃO', 223.83
);

INSERT INTO app.compras VALUES (
    3, '888.333.222-92', 'CARTÃO', 14.29
);
