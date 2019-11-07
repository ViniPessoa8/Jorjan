import sys
from hashlib import sha1
from ..config.db import get_connection
from ..util.utils import format_history_result
from ..util.jwt_manager import encode as jwt_encode
from ..util.errors import (
    error_resp, 
    EmailAlreadyRegistered, 
    CouldNotGetUserHistory,
    UsernameAlreadyRegistered, 
    CouldNotRegisterUser,
    CouldNotFindProductOwner,
    CouldNotFindUserState,
    NoAvailableSellers
)

from .queries.user_queries import (
    qr_get_users, 
    qr_get_user_info,
    qr_get_user_by_email,
    qr_get_user_by_username,
    qr_get_user_by_email_ps, 
    qr_get_product_owner,
    qr_register_user,
    qr_get_history,
    qr_register_user_with_auth, 
    qr_remove_user,
    qr_update_pass_by_id,
    qr_get_user_state_by_id,
    qr_set_user_state_by_id,
    qr_get_available_sellers
)

def get_all_users():
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(qr_get_users())
            result = c.fetchall()    
    finally:
        conn.close()
        return result

def get_info(auth):
    conn   = get_connection()
    result = {}
    try:
        with conn.cursor() as c:
            c.execute(qr_get_user_info(auth))
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
            c.execute(qr_get_user_by_email(email))
            if c.fetchall() != ():
                raise EmailAlreadyRegistered

            c.execute(qr_get_user_by_username(username))
            if c.fetchall() != ():
                raise UsernameAlreadyRegistered
                    
            auth = jwt_encode({ 'email': email, 'ps': ps })
            c.execute(qr_register_user_with_auth(name=name, ps=ps, email=email, auth=auth, username=username))
        conn.commit()
        
        result = { 'name': name, 'email': email, 'auth': auth, 'username': username }
    except EmailAlreadyRegistered as e:
        result = error_resp(e)
    except UsernameAlreadyRegistered as e:
        result = error_resp(e)
    except BaseException:
        result = error_resp(CouldNotRegisterUser())
    finally:
        conn.close()
        return result
            
def remove_user_email_ps(email, ps):
    ps     = sha1(ps.encode('utf-8')).hexdigest()
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(qr_get_user_by_email_ps(email=email, ps=ps))
            if(c.fetchone()):
                c.execute(qr_remove_user(email=email,ps=ps))
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
            c.execute(qr_update_pass_by_id(email, ps))
        conn.commit()
        result = new_pass
    finally:
        conn.close()
        return result

def get_product_owner(product_id):
    conn   = get_connection()
    result = None
    try:
        with conn.cursor() as c:
            c.execute(qr_get_product_owner(product_id))
            result = c.fetchone()
        
        if result == None:
            raise CouldNotFindProductOwner
        
    except BaseException:
        result = error_resp(CouldNotFindProductOwner())
    finally:
        conn.close()
        return result
    
def get_history(user_id):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_get_history(user_id=user_id))
            result = c.fetchall()

        if result == ():
            result = { 'history': [] }
        else:
            history = format_history_result(result)
            result = { 'history':  history}
    except BaseException:
        result = error_resp(CouldNotGetUserHistory())

def get_user_state_by_id(id):
    conn   = get_connection()
    result = None
    
    try:
        with conn.cursor() as c:
            c.execute(qr_get_user_state_by_id(id=id))
            result = c.fetchone()
        
        if result == None:
            raise CouldNotFindUserState
        
    except BaseException:
        result = error_resp(CouldNotFindUserState())
    finally:
        conn.close()
        return result

def set_user_state_by_id(id, state):
    conn   = get_connection()
    result = None
    try:
        with conn.cursor() as c:
            c.execute(qr_get_user_state_by_id(id=id))
            result = c.fetchone()

            if result == None:
                raise CouldNotFindUserState

            c.execute (qr_set_user_state_by_id(id=id, state=state))
            conn.commit()
        result = {'id':id, 'state':state}
    except BaseException as e:
        result = error_resp(e)
    finally:
        conn.close()
        return result

def get_available_sellers():
    conn   = get_connection()
    result = None

    print(result)
    try:
        with conn.cursor() as c:
            c.execute(qr_get_available_sellers())
            result = c.fetchall()
            print(result)


            if (result == ()):
                raise NoAvailableSellers

        result = {'sellers':result}
    except BaseException:
        result = error_resp(NoAvailableSellers())
    finally:
        conn.close()
        return result