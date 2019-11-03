use Jorjan;

-- Util
SELECT * FROM Jorjan.`user`;

-- Cadastrar Usuário
INSERT INTO Jorjan.`user`(email, username, `password`, `name`, state, picture, avaliation, auth)
VALUES ('gustavo@gmail.com','gusta_braga',SHA('espinafre2000'),'Gustavo Braga Mota',0,NULL,NULL,NULL);

INSERT INTO Jorjan.`user` (email, username, `password`, `name`, state, picture, avaliation, auth)
VALUES ('ana@gmail.com','aninha0660',SHA('espinafre2000'),'Ana Beatriz de Souza',0,NULL,NULL,NULL);

-- Realizar Login
SELECT *
FROM Jorjan.`user`
WHERE email = 'gustavo@gmail.com' AND `password` = SHA('espinafre2000');

-- Cadastrar Produto
INSERT INTO Jorjan.product(name, description, price, stock, category, owner_id)
VALUES ('Brigadeiro', 'Bolinhas de chocolate.', 2.00, 20, 'Doces', 1);

-- Realizar Pedido
-- STATUS DO PEDIDO
-- 0 -> CANCELADO
-- 1 -> AGUARDANDO CONFIRMAÇÃO
-- 2 -> AGUARDANDO ENTREGA
-- 3 -> FINALIZADO 

INSERT INTO Jorjan.sales(`date`, quantity, buyer_id, seller_id, observation, delivery, `status`)
VALUES (2019-11-02, 2, 2, 1, NULL, FALSE, 0);

-- Selecionar Categoria
SELECT *
FROM Jorjan.product
WHERE category = 'Doces';

-- Selecionar Vendedor

-- Selecionar Produto

-- Adicionar Item Carrinho

-- Remover Item Carrinho

-- 	Abrir Carrinho

-- Pesquisar

-- Confirmar Pedido

-- Confirmar Pagamento

-- Notificar Vendedor

-- Confirmar Entrega

-- Avaliar Pedido

-- Mostrar Histórico

-- Editar Perfil

-- Cancelar Pedido
