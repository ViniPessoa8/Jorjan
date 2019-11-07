from ...util.constants import USER_STATES

def qr_get_users():
    return "SELECT * FROM user;"

def qr_get_user_info(auth):
    return "SELECT name, email, username FROM user WHERE auth='%s';" % (auth)

def qr_get_user_by_email(email):
    return "SELECT name, email, auth, id, username FROM user WHERE email='%s'" % (email)

def qr_get_user_by_username(username):
    return "SELECT name, email, auth, id, username FROM user WHERE username='%s'" % (username)

def qr_get_user_by_email_ps(email, ps):
    return "SELECT name, email, auth, username, id FROM user WHERE (email='%s' and password='%s')" % (email, ps)

def qr_get_user_by_username_ps(username, ps):
    return "SELECT name, email, auth, id, username FROM user WHERE (username='%s' and password='%s')" % (username, ps)

def qr_get_user_by_auth(auth):
    return "SELECT id, email FROM user WHERE auth='%s';" % auth

def qr_register_user(email, name, ps, username):
    return "INSERT INTO user(name, email, password, username, state) \
        VALUES ('%s', '%s', '%s', '%s', FALSE);" % (name, email, ps, username)

def qr_register_user_with_auth(email, name, ps, auth, username):
    return "INSERT INTO user(name, email, password, auth, username, state) \
        VALUES ('%s', '%s', '%s', '%s', '%s', FALSE );" % (name, email, ps, auth, username)

def qr_remove_user(email, ps):
    return "DELETE FROM user WHERE (email='%s' AND password='%s')" % (email, ps)
    
def qr_update_auth(auth, email, ps):
    return "UPDATE user SET auth = '%s' WHERE email = '%s' AND password = '%s'" % (auth, email, ps)

def qr_update_pass_by_id(email, new_pass):
    return "UPDATE user SET password='%s' WHERE email='%s';" % (new_pass, email)

def qr_get_product_owner(product_id):
    return f"""
        SELECT u.id, u.email
        FROM user u
        LEFT JOIN product p ON (p.owner_id = u.id)
        WHERE p.id={product_id};
    """

def qr_get_user_state_by_id(id):
    return f"""
        SELECT state
        FROM user
        WHERE id={id};
    """

def qr_get_available_sellers():
    return f"""
        SELECT *
        FROM user
        where state={USER_STATES['SELLER']};
    """

def qr_set_user_state_by_id(id, state):
    return f"""
        UPDATE user
        SET state={state}
        WHERE id={id};
    """