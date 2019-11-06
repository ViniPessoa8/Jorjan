import sys
from hashlib import sha1
from ..config.db import get_connection
from ..util.jwt_manager import encode as jwt_encode
from ..util.errors import EmailAlreadyRegistered, UsernameAlreadyRegistered, error_resp, CouldNotRegisterUser
from .queries.user_queries import (
    get_users, 
    get_user_info,
    get_user_by_email,
    get_user_by_username,
    get_user_by_email_ps, 
    register_user, 
    register_user_with_auth, 
    remove_user,
    update_pass_by_id
)

def get_all_users():
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(get_users())
            result = c.fetchall()    
    finally:
        conn.close()
        return result

def get_info(auth):
    conn   = get_connection()
    result = {}
    try:
        with conn.cursor() as c:
            c.execute(get_user_info(auth))
            result = c.fetchone()

    finally:
        conn.close()
        return result

def register_new_user(name, ps, email, username):
    ps     = sha1(ps.encode('utf-8')).hexdigest()
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(get_user_by_email(email))
            if c.fetchall() != ():
                raise EmailAlreadyRegistered

            c.execute(get_user_by_username(username))
            if c.fetchall() != ():
                raise UsernameAlreadyRegistered
                    
            auth = jwt_encode({ 'email': email, 'ps': ps })
            c.execute(register_user_with_auth(name=name, ps=ps, email=email, auth=auth, username=username))
        conn.commit()
        
        result = { 'name': name, 'email': email, 'auth': auth, 'username': username }
    except EmailAlreadyRegistered as e:
        result = error_resp(e)
    except UsernameAlreadyRegistered as e:
        result = error_resp(e)
    except BaseException:
        result = error_resp(CouldNotRegisterUser().__str__())
    finally:
        conn.close()
        return result
            
def remove_user_email_ps(email, ps):
    ps     = sha1(ps.encode('utf-8')).hexdigest()
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(get_user_by_email_ps(email=email, ps=ps))
            if(c.fetchone()):
                c.execute(remove_user(email=email,ps=ps))
                result = c.fetchone()
                conn.commit()

    finally:
        conn.close()
        return result

def update_user_pass(email, new_pass):
    ps = sha1(new_pass.encode('utf-8')).hexdigest()
    conn = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(update_pass_by_id(email, ps))
        conn.commit()
        result = new_pass
    finally:
        conn.close()
        return result
