def get_users():
    return "SELECT * FROM usuario;"

def get_user_by_email(email):
    return "SELECT nome, email, auth, id FROM usuario WHERE email='%s'" % (email)

def get_user_by_email_ps(email, ps):
    return "SELECT nome, email, auth, id FROM usuario WHERE (email='%s' and senha='%s')" % (email, ps)

def register_user(email, name, ps):
    return "INSERT INTO usuario(nome, email, senha) \
        VALUES ('%s', '%s', '%s');" % (name, email, ps)

def remove_user(email, ps):
    return "DELETE FROM usuario WHERE (email='%s' AND senha='%s')" % (email, ps)
    
def update_auth(auth, email, ps):
    return "UPDATE usuario SET auth = '%s' WHERE email = '%s' AND senha = '%s'" % (auth, email, ps)
    