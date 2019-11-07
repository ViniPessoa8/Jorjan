use Jorjan;

-- Util
	SELECT * FROM Jorjan.`user`;
    SELECT * FROM Jorjan.sales;
    SELECT * FROM Jorjan.sales_has_product;

-- Cadastrar Usuário
	INSERT INTO Jorjan.`user`(email, username, `password`, `name`, state, picture, avaliation, auth)
	VALUES ('gustavo@gmail.com','gusta_braga',SHA('123'),'Grustavo Braga Mota',0,NULL,NULL,NULL);

	INSERT INTO Jorjan.`user` (email, username, `password`, `name`, state, picture, avaliation, auth)
	VALUES ('ana@gmail.com','aninha0660',SHA('123'),'Ana Beatriz de Souza',0,NULL,NULL,NULL);
    
    INSERT INTO Jorjan.`user` (email, username, `password`, `name`, state, picture, avaliation, auth)
	VALUES ('vcbp.snf18@uea.edu.br','ViniPessoa8',SHA('123'),'Vinícius Cavalcante de Brito Pessoa',0,NULL,NULL,NULL);

-- Realizar Login
	SELECT *
	FROM Jorjan.`user`
	WHERE email = 'gustavo@gmail.com' AND `password` = SHA('espinafre2000');

-- Cadastrar Produto
	INSERT INTO Jorjan.product(name, description, price, stock, category, owner_id)
	VALUES ('Brigadeiro', 'Bolinhas de chocolate.', 2.00, 20, 1, 1);

-- STATUS DO PEDIDO
	-- 0 -> CANCELADO
	-- 1 -> CARRINHO
	-- 2 -> AGUARDANDO CONFIRMAÇÃO
	-- 3 -> AGUARDANDO ENTREGA
    -- 4 -> FINALIZADO 

-- Adicionar Item Carrinho
	INSERT INTO Jorjan.sales(`date`, buyer_id, seller_id, observation, `status`)
	VALUES (DATE '2019-11-02', 2, 1, NULL, 1);
    
    -- Registra os produtos e suas respectivas quantidades
        INSERT INTO Jorjan.sales_has_product(sales_id, product_id, quantity)
        VALUES(1, 1, 2);

-- Realizar Pedido
	-- Busca o ultimo ID
		SELECT id
		FROM Jorjan.sales
		WHERE `status` = 1;

	-- Verifica se o vendedor está disponível
		SELECT `state`
		FROM Jorjan.`user`
		WHERE id = 1;
        
	-- Realiza o pedido
		UPDATE Jorjan.sales
        SET `status` = 2
        WHERE id = 1;

-- Selecionar Categoria
	SELECT *
	FROM Jorjan.product
	WHERE category = 'Doces';

-- Selecionar Vendedor
	SELECT *
	FROM Jorjan.product as p, Jorjan.`user` as u
	WHERE u.id = 1;

-- Selecionar Produto
	SELECT *
    FROM Jorjan.product
    WHERE id = 1;

-- Remover Item Carrinho
	DELETE FROM Jorjan.sales_has_product
    WHERE sales_id = 1
		AND product_id = 1;

-- 	Abrir Carrinho
	SELECT *
    FROM Jorjan.sales as s, Jorjan.sales_has_product h
    WHERE s.id = 1;

-- Pesquisar
	SELECT *
    FROM Jorjan.product as p
    WHERE p.category = 'Doces' 
		OR p.`name` LIKE '%Doces%';
    
-- Confirmar Pedido
	UPDATE Jorjan.sales
        SET `status` = 3
        WHERE id = 1;

-- Confirmar Pagamento

-- Notificar Vendedor

-- Confirmar Entrega
	UPDATE Jorjan.sales
        SET `status` = 4
        WHERE id = 1;
        
-- Avaliar Usuário
	-- Se for nulo
	UPDATE Jorjan.`user`
	SET avaliation = 4.5
    WHERE id = 1;

    -- Se já existir avaliação
	UPDATE Jorjan.`user`
	SET avaliation = (4 + avaliation)/2
    WHERE id = 1;
	

-- Mostrar Histórico
	-- Vendas
		SELECT *
		FROM Jorjan.`user` as u, Jorjan.sales as s, Jorjan.sales_has_product as h
		WHERE u.id = 1
			AND s.seller_id = u.id
            AND h.sales_id = s.id;
	
    -- Compras
		SELECT *
		FROM Jorjan.`user` as u, Jorjan.sales as s, Jorjan.sales_has_product as h
		WHERE u.id = 2
			AND s.buyer_id = u.id
            AND h.sales_id = s.id;

-- Editar Perfil
	UPDATE Jorjan.`user`
    SET username = 'gusta_braga',
		`name` = 'Gustavo',
        email = 'gustavo@gmail.com',
        `password` = SHA('espinafre3000')
	WHERE id = 1;

-- Cancelar Pedido
	UPDATE Jorjan.sales
        SET `status` = 0
        WHERE id = 1;
        
-- Criar Categoria
	INSERT INTO Jorjan.category(`name`)
    VALUES ("Doces");
    
-- Remover Categoria
	DELETE FROM Jorjan.category
    WHERE id = 1;
    
-- Selecionar Categoria
	SELECT `name`
    FROM Jorjan.category;