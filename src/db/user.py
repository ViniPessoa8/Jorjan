from hashlib import sha1
from ..config.db import get_connection
from ..util.jwt_manager import encode as jwt_encode
from .user_queries import (
    get_users, 
    get_user_info,
    get_user_by_email, 
    get_user_by_email_ps, 
    register_user, 
    register_user_with_auth, 
    remove_user
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

def register_new_user(name, ps, email):
    ps     = sha1(ps.encode('utf-8')).hexdigest()
    conn   = get_connection()
    result = {}

    try:
        with conn.cursor() as c:
            c.execute(get_user_by_email(email))
            if c.fetchall() != ():
                raise ValueError
                    
            auth = jwt_encode({ 'email': email, 'ps': ps })
            c.execute(register_user_with_auth(name=name, ps=ps, email=email, auth=auth))
        conn.commit()
        
        result = { 'name': name, 'email': email, 'auth': auth }
    except ValueError:
        result = { 'error': "User already exist" }
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
