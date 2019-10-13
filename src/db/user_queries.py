def get_users():
    return "SELECT * FROM usuario;"

def get_user_info(auth):
    return "SELECT nome, email FROM usuario WHERE auth='%s';" % (auth)

def get_user_by_email(email):
    return "SELECT nome, email, auth, id FROM usuario WHERE email='%s'" % (email)

def get_user_by_email_ps(email, ps):
    return "SELECT nome, email, auth, id FROM usuario WHERE (email='%s' and senha='%s')" % (email, ps)

def register_user(email, name, ps):
    return "INSERT INTO usuario(nome, email, senha) \
        VALUES ('%s', '%s', '%s');" % (name, email, ps)

def register_user_with_auth(email, name, ps, auth):
    return "INSERT INTO usuario(nome, email, senha, auth) \
        VALUES ('%s', '%s', '%s', '%s');" % (name, email, ps, auth)

def remove_user(email, ps):
    return "DELETE FROM usuario WHERE (email='%s' AND senha='%s')" % (email, ps)
    
def update_auth(auth, email, ps):
    return "UPDATE usuario SET auth = '%s' WHERE email = '%s' AND senha = '%s'" % (auth, email, ps)
    