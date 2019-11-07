def error_resp(e):
    return { 'error': e.__str__() }

class InvalidRequest(BaseException):
    def __str__(self):
        return "Requisição Inválida"

# User ================================================================
class EmailAlreadyRegistered(BaseException):
    def __str__(self):
        return "Email já registrado"

class UsernameAlreadyRegistered(BaseException):
    def __str__(self):
        return "Username já registrado"

class InvalidLogin(BaseException):
    def __str__(self):
        return "Login Inválido"

class CouldNotRegisterUser(BaseException):
    def __str__(self):
        return "Não foi possível registrar o usuário"

class CouldNotUpdateUser(BaseException):
    def __str__(self):
        return "Não foi possível atualizar o usuário"

class CouldNotFindProductOwner(BaseException):
    def __str__(self):
        return "Não foi possível encontrar o produto ou o dono do mesmo"
# Product ============================================================
class CouldNotRegisterProduct(BaseException):
    def __str__(self):
        return "Não foi possível registrar o produto"

# Sales ==============================================================
class CouldNotStartCart(BaseException):
    def __str__(self):
        return "Não foi possível iniciar o carrinho"

class CouldNotAddToCart(BaseException):
    def __str__(self):
        return "Não foi possível adicionar produto ao carrinho"

class CouldNotChangeSaleStatus(BaseException):
    def __str__(self):
        return "Não foi possível alterar sua compra"
