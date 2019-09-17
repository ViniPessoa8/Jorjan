class Usuario:

    def __init__(self, nome, nickName, senha, email):
        self.nome     = nome
        self.nickName = nickName
        self.senha    = senha
        self.email    = email
        self.estado   = 0
        self.produtos = []

    def adicionarProduto(self, produto):
        self.produtos.append(produto)

    def solicitarServico(self, serv):
        if (serv == "vendedor"):
            self.estado = 1
        elif (serv == "comprador"):
            self.estado = 0

    ## Comprador ##
    def comprar(self):
        print("Comprar")

    def pagar(self):
        print("Pagar")

    def receberPedido(self):
        print("Receber Pedido")

    def avaliarVendedor(self):
        print("AvaliarVendedor")

    ## Vendedor ##
    def atualizarEstoque(self, produto, estoque):
        produto.estoque = estoque

    def entregarPedido(self):
        print("Entregar Pedido")

    def avaliarComprador(self):
        print("Avaliar Comprador")

    def solicitarEstatisticas(self):
        print("Solicitar Estatisticas")

class Pedido:

    def __init__(self, nickComprador, nickVendedor, formaRetirada, formaPagamento, carrinho, observacao):
        self.nickVendedor   = nickVendedor
        self.nickComprador  = nickComprador
        self.formaRetirada  = formaRetirada
        self.formaPagamento = formaPagamento
        self.carrinho       = carrinho
        self.observacao     = observacao

    def calcularTotal(self):
        total = 0.0
        for item in self.carrinho:
            total += item.produto.preco * item.quantidade
        self.total = total

    def enviarNotificacao(self):
        print("Vendedor notificado.")

class Notificacao:
    mensagem   = None
    valorTroco = None
    observacao = None

class Item:
   
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def verificarProduto(self):
        print("Verifica Produto")

class Produto:

    def __init__(self, nome, descricao, estoque, nickVendedor, preco, categorias):
        self.nome = nome
        self.descricao = descricao
        self.estoque = estoque
        self.nickVendedor = nickVendedor
        self.preco = preco
        self.categorias = categorias.copy()

class Sistema:


    def __init__(self):
        self.usuarioAtual = None
        self.carrinho = []
        self.usuarios = []
        
    def listarFormasEntrega(self):
        txt = """
        Forma de retirada:\n
        1) Delivery\n
        2) Retirar no local\n
        0) Sair
        """
        print(txt)
        
        escolha2 = int(input("\nEscolha: "))
        if (escolha == -2):
            self.finalizarCompra()
        else :
            return escolha2

    def listarCategorias(self):
        txt = "\nCategorias:\n1) Doces\n2) Salgados\n0) Sair"
        print (txt)

        escolha = int(input("\nEscolha: "))
        if (escolha == -2):
            self.finalizarCompra()
        else:
            retorno = ""
            if (escolha == 1):
                retorno = "Doce"
            elif(escolha == 2):
                retorno = "Salgado"
            
            return retorno

    def listarVendedores(self, categoria):
        # vendedores = self.listarVendedores(categoria)
        vendedores = []
        vendedor = None

        for usuario in self.usuarios:
            if (len(usuario.produtos) != 0):
                for produto in usuario.produtos:
                    if (categoria in produto.categorias):
                        vendedores.append(usuario)

        if (len(vendedores) > 0):
            print("\nVendedores:")
            i = 1;
            for vendedor in vendedores:
                print("" + str(i) + ") " + vendedor.nome + " (" + vendedor.nickName + ")")
                i += 1
            print("-2) Finalizar Compra\n0) Sair")

            escolha = int(input("\nEscolha: "))

            if (escolha == -2):
                self.finalizarCompra()
            else :

                i = 1
                for v in vendedores:
                    if (i == escolha):
                        vendedor = v
                        break
                    i += 1
        
        return vendedor

    def listarProdutos(self, vendedor):
        listaProdutos = []
        produto = None
        listaProdutos = vendedor.produtos.copy()

        print("\nProdutos:")
        j = 1   
        for produto in vendedor.produtos:
            print(str(j) + ") " + produto.nome)
            j += 1
        print("-2)Finalizar Compra\n0) Sair")

        escolha = int(input("\nEscolha: "))

        if (escolha == -2):
            self.finalizarCompra()
        else :
            i = 1
            for p in listaProdutos:
                if(i == escolha ):
                    produto = p
                    break
                i += 1

            return produto

    def adicionarAoCarrinho(self, produto):
        qt = int(input("\nQuantidade: "))
        item = Item(produto, qt)
        self.carrinho.append(item)
        
    # def removerDoCarrinho(produto):


    def finalizarCompra(self):
        if (len(self.carrinho) == 0):
            print("\nCarrinho vazio.")
        else :
            print("\nCarrinho:")
            for item in self.carrinho:
                print(item.produto.nome + "   " + str(item.quantidade) + " unid.   " + item.produto.nickVendedor)
            
            total = 0.0
            for item in self.carrinho:
                total += item.produto.preco * item.quantidade

            print("TOTAL: R$" + str(total))

            escolha = input("Comprar?(S/N)\n")

            if (escolha == "S"):
                print("Seu pedido está esperando por você.")
                self.carrinho = []
            else :
                escolha2 = input("Limpar carrinho?(S/N)\n")
                if (escolha2 == "S"):
                    self.carrinho = []


    def logar(self):
        email = input("\nE-mail:")
        senha = input("Senha:")
        for usuario in self.usuarios:
            if (usuario.email == email and usuario.senha == senha):
                print("Login bem-sucedido.")
                self.logado = True
                self.usuarioAtual = usuario
        return self.usuarioAtual

    def cadastrar(self):
        nome = input("Nome: ")
        nickName = input("NickName: ")
        email = input("E-mail:")
        senha = input("Senha:")

        usuario = Usuario(nome, nickName, senha, email)
        self.usuarios.append(usuario)

    def menuPrincipal(self):
        logado = False
        continuar = False
        txt = "1) Cadastrar\n2) Logar\n0) Sair"
        print(txt)

        escolha = int(input("\nEscolha: "))
        while (escolha > 0 and self.usuarioAtual == None):
    
            ## Cadastro ##
            if escolha == 1:
                self.cadastrar()

            ## Login ##
            elif escolha == 2:
                self.logar()

            if(self.usuarioAtual):
                continuar = True
            else :
                print("\n" + txt)
                escolha = int(input("\nEscolha: "))

        while(continuar):
            entrega = self.listarFormasEntrega()
            if (entrega == 0):
                continuar = False
                break

            categoria = self.listarCategorias()
            if(categoria == ""):
                continuar = False
                break
            
            print(1)
            vendedor = self.listarVendedores(categoria)
            if(vendedor == None):
                continuar = False
                break
            print(2)

            produto = self.listarProdutos(vendedor)
            while (produto != None):
                self.adicionarAoCarrinho(produto)
                produto = self.listarProdutos(vendedor)
            


        
### MENU ###
escolha = 0
usuarioLocal = None

sistema = Sistema()

u1 = Usuario("João", "joaomvp", "123", "joaozinho@hotmail.com")
u2 = Usuario("Luiz", "luizmvp", "123", "luizinho@hotmail.com")
u3 = Usuario("Beatriz", "biamvp", "321", "biazinha@hotmail.com")
u4 = Usuario("Vinicius", "ViniPessoa8", "123", "vini")

p1 = Produto("Brigadeiro", "Bolas de chocolate", 30, "joaomvp", 1.0, ["Doce", "Chocolate"])
p2 = Produto("Empada", "Frango e Camarão", 15, "luizinhomvp", 3.0, ["Salgado", "Frango", "Camarão"])
p3 = Produto("Brigadeirão", "Bolas de chocolate", 20, "luizmvp", 2.0, ["Doce", "Chocolate"])

u1.adicionarProduto(p1)
u1.adicionarProduto(p2)
u2.adicionarProduto(p3)

sistema.usuarios.append(u1)
sistema.usuarios.append(u2)
sistema.usuarios.append(u3)
sistema.usuarios.append(u4)

sistema.menuPrincipal()