from hashlib import sha1
from ..config.db import get_connection
from .user_queries import (
    get_user_by_email_ps,
    update_auth
)

def check_login(email, ps):
    ps     = sha1(ps.encode('utf-8')).hexdigest()
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(get_user_by_email_ps(email=email, ps=ps))
            result = c.fetchone()
    finally:
        conn.close()
        return result

def update_auth_key(auth, email, ps):
    ps     = sha1(ps.encode('utf-8')).hexdigest()
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(get_user_by_email_ps(email=email, ps=ps))
            result_query = c.fetchone()
            if(result_query):
                c.execute(update_auth(auth=auth, email=email, ps=ps))
        conn.commit()
    finally:
        conn.close()
        return result
