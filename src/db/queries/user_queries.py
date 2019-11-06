def get_users():
    return "SELECT * FROM user;"

def get_user_info(auth):
    return "SELECT name, email FROM user WHERE auth='%s';" % (auth)

def get_user_by_email(email):
    return "SELECT name, email, auth, id FROM user WHERE email='%s'" % (email)

def get_user_by_email_ps(email, ps):
    return "SELECT name, email, auth, id FROM user WHERE (email='%s' and password='%s')" % (email, ps)

def get_user_by_auth(auth):
    return "SELECT email FROM user WHERE auth='%s';" % auth

def register_user(email, name, ps):
    return "INSERT INTO user(name, email, password) \
        VALUES ('%s', '%s', '%s');" % (name, email, ps)

def register_user_with_auth(email, name, ps, auth):
    return "INSERT INTO user(name, email, password, auth) \
        VALUES ('%s', '%s', '%s', '%s');" % (name, email, ps, auth)

def remove_user(email, ps):
    return "DELETE FROM user WHERE (email='%s' AND password='%s')" % (email, ps)
    
def update_auth(auth, email, ps):
    return "UPDATE user SET auth = '%s' WHERE email = '%s' AND password = '%s'" % (auth, email, ps)

def update_pass_by_id(email, new_pass):
    return "UPDATE user SET password='%s' WHERE email='%s';" % (new_pass, email)