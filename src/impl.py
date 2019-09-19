class Usuario:

    def __init__(self, nome, nickName, senha, email):
        self.nome = nome
        self.nickName = nickName
        self.senha = senha
        self.email = email
        self.estado = 0
        self.produtos = []

    def adicionarProduto(self, produto):
        self.produtos.append(produto)

    def solicitarServico(serv):
        if (serv == "vendedor"):
            self.estado = 1
        elif (serv == "comprador"):
            self.estado = 0

    def comprar(self):
        print("Comprar")

    def pagar(self):
        print("Pagar")

    def receberPedido(self):
        print("Receber Pedido")

    def avaliarVendedor(self):
        print("AvaliarVendedor")

    def atualizarEstoque(self):
        print("Atualizar estoque")

    def entregarPedido(self):
        print("Entregar Pedido")

    def avaliarComprador(self):
        print("Avaliar Comprador")

    def solicitarEstatisticas(self):
        print("Solicitar Estatisticas")



class Comprador(Usuario):

    def __init__(self):
        super().__init__()

class Pedido:
    itens = []
    observacao = None

    def enviarNotificacao():
        print("Enviar Notificação")

class Notificacao:
    mensagem = None
    valorTroco = None
    observacao = None

class Item:
    
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def verificarProduto():
        print("Verifica Produto")

class Produto:
    nome = None
    descricao = None
    nickVendedor = None
    preco = 0.0
    categorias = []

    def __init__(self, nome, descricao, nickVendedor, preco, categorias):
        self.nome = nome
        self.descricao = descricao
        self.nickVendedor = nickVendedor
        self.preco = preco
        self.categorias = categorias


### MENU ###
carrinho = []
usuarios = []
escolha = 0

u1 = Usuario("João", "joaomvp", "123", "joaozinho@hotmail.com")
u2 = Usuario("Luiz", "luizmvp", "123", "luizinho@hotmail.com")
u3 = Usuario("Beatriz", "biamvp", "321", "biazinha@hotmail.com")
u4 = Usuario("Vinicius", "ViniPessoa8", "123", "vini")

p1 = Produto("Brigadeiro", "Bolas de chocolate", "joaomvp", 1.0, ["Doce", "Chocolate"])
p2 = Produto("Empada", "Frango e Camarão", "luizinhomvp", 3.0, ["Salgado", "Frango", "Camarão"])
p3 = Produto("Brigadeirão", "Bolas de chocolate", "luizmvp", 2.0, ["Doce", "Chocolate"])

u1.adicionarProduto(p1)
u1.adicionarProduto(p2)
u2.adicionarProduto(p3)

usuarios.append(u1)
usuarios.append(u2)
usuarios.append(u3)
usuarios.append(u4)


def listarVendedores(categoria):
    vendedores = []
    for usuario in usuarios:
        if (len(usuario.produtos) != 0):
            for produto in usuario.produtos:
                if (categoria in produto.categorias):
                    vendedores.append(usuario)
                    
    
    return vendedores

def finalizar():
    global carrinho
    if (len(carrinho) == 0):
        print("\nCarrinho vazio.")
    else :
        print("\nCarrinho:")
        for item in carrinho:
            print(item.produto.nome + "   " + str(item.quantidade) + " unid.   " + item.produto.nickVendedor)
        
        total = 0.0
        for item in carrinho:
            total += item.produto.preco * item.quantidade

        print("TOTAL: R$" + str(total))

        escolha = input("Comprar?(S/N)\n")

        if (escolha == "S"):
            print("Seu pedido está esperando por você.")
            carrinho = []
        else :
            escolha2 = input("Limpar carrinho?(S/N)\n")
            if (escolha2 == "S"):
                carrinho = []

while escolha >= 0:

    logado = False
    txt = "1) Cadastrar\n2) Logar\n0) Sair"
    print(txt)

    escolha = int(input("\nEscolha: "))

    # CADASTRO
    if escolha == 1:
        nome = input("Nome: ")
        nickName = input("NickName: ")
        email = input("E-mail:")
        senha = input("Senha:")

        usuario = Usuario(nome, nickName, senha, email)
        usuarios.append(usuario)

    # Login
    elif escolha == 2:
        email = input("\nE-mail:")
        senha = input("Senha:")
        for usuario in usuarios:
            if (usuario.email == email and usuario.senha == senha):
                print("Login bem-sucedido.")
                logado = True
        if(not logado):
            print("Falha no login.")

    elif escolha == 0:
        escolha = -1

    if (logado):

        escolha1 = 0

        while (escolha1 >= 0):
            txt = "\nForma de retirada:\n1) Delivery\n2) Retirar no local\n0) Sair"
            print(txt)

            escolha2 = int(input("\nEscolha: "))
            if(escolha2 == 0):
                escolha1 = -1
            elif(escolha2 == -2):
                finalizar()
            while (escolha2 > 0):
                        
                ## Categoria
                txt = "\nCategorias:\n1) Doces\n2) Salgados\n0) Sair"
                print (txt)

                escolha3 = int(input("\nEscolha: "))
                if(escolha3 == 0):
                    escolha2 = -1
                elif(escolha3 == -2):
                    finalizar()

                while(escolha3 > 0):
                    ## Vendedores

                    vendedores = []

                    if(escolha3 == 1):
                        vendedores = listarVendedores("Doce")
                    elif(escolha3 == 2):
                        vendedores = listarVendedores("Salgado")

                    i = 1
                    print("\nVendedores:")
                    for vendedor in vendedores:
                        print("" + str(i) + ") " + vendedor.nome + " (" + vendedor.nickName + ")")
                        i += 1
                    print("-2) Finalizar Compra\n0) Sair")
                        
                    escolha4 = int(input("\nEscolha: "))
                    if(escolha4 == 0):
                        escolha3 = -1
                    elif(escolha4 == -2):
                        finalizar()

                    while(escolha4 > 0):
                        ## Produtos
                        print("\nProdutos:")
                        i = 1
                        listaProdutos = []
                        for vendedor in vendedores:
                            if(escolha4 == i):
                                j = 1
                                listaProdutos = vendedor.produtos.copy()
                                for produto in vendedor.produtos:
                                    print(str(j) + ") " + produto.nome)
                                    j += 1
                                print("-2)Finalizar Compra\n0) Sair")
                            i += 1
                                        

                        escolha5 = int(input("\nEscolha: "))
                        if(escolha5 == 0):
                            escolha4 = -1
                        elif(escolha5 == -2):
                            finalizar()
                        while(escolha5 >= 1):
                            
                            achou = False
                            i = 1
                            for produto in listaProdutos:
                                print(i)
                                if(escolha5 == i):
                                    achou = True
                                    qt = int(input("\nQuantidade: "))
                                    item = Item(produto, qt)
                                    carrinho.append(item)
                                    escolha5 = 0
                                i += 1
                            
                            if (not achou):
                                print("Opção inválida")
                                escolha5 = 0


        
                




