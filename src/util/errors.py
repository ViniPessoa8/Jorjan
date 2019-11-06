def error_resp(e):
    return { 'error': e.__str__() }

class EmailAlreadyRegistered(BaseException):
    def __str__(self):
        return "Email já registrado"

class UsernameAlreadyRegistered(BaseException):
    def __str__(self):
        return "Username já registrado"

class InvalidRequest(BaseException):
    def __str__(self):
        return "Requisição Inválida"

class InvalidLogin(BaseException):
    def __str__(self):
        return "Login Inválido"

class CouldNotRegisterUser(BaseException):
    def __str__(self):
        return "Não foi possível registrar o usuário"

class CouldNotUpdateUser(BaseException):
    def __str__(self):
        return "Não foi possível atualizar o usuário"