def get_users():
    return "SELECT * FROM usuario;"

def get_user_by_email(email):
    return "SELECT * FROM usuario WHERE email='%s'" % (email)

def get_user_by_email_ps(email, ps):
    return "SELECT * FROM usuario WHERE (email='%s' and senha='%s')" % (email, ps)

def register_user(email, name, ps):
    return "INSERT INTO usuario(nome, email, senha) \
        VALUES ('%s', '%s', '%s');" % (name, email, ps)