def get_users():
    return "SELECT * FROM user;"

def get_user_info(auth):
    return "SELECT name, email, username FROM user WHERE auth='%s';" % (auth)

def get_user_by_email(email):
    return "SELECT name, email, auth, id, username FROM user WHERE email='%s'" % (email)

def get_user_by_username(username):
    return "SELECT name, email, auth, id, username FROM user WHERE username='%s'" % (username)

def get_user_by_email_ps(email, ps):
    return "SELECT name, email, auth, username, id FROM user WHERE (email='%s' and password='%s')" % (email, ps)

def get_user_by_username_ps(username, ps):
    return "SELECT name, email, auth, id, username FROM user WHERE (username='%s' and password='%s')" % (username, ps)

def get_user_by_auth(auth):
    return "SELECT email FROM user WHERE auth='%s';" % auth

def register_user(email, name, ps, username):
    return "INSERT INTO user(name, email, password, username, state) \
        VALUES ('%s', '%s', '%s', '%s', FALSE);" % (name, email, ps, username)

def register_user_with_auth(email, name, ps, auth, username):
    return "INSERT INTO user(name, email, password, auth, username, state) \
        VALUES ('%s', '%s', '%s', '%s', '%s', FALSE );" % (name, email, ps, auth, username)

def remove_user(email, ps):
    return "DELETE FROM user WHERE (email='%s' AND password='%s')" % (email, ps)
    
def update_auth(auth, email, ps):
    return "UPDATE user SET auth = '%s' WHERE email = '%s' AND password = '%s'" % (auth, email, ps)

def update_pass_by_id(email, new_pass):
    return "UPDATE user SET password='%s' WHERE email='%s';" % (new_pass, email)