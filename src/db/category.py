from ..config.db import get_connection
from ..util.errors import error_resp, CouldNotRegisterCategory, CategoryNotFound
from .queries.category_queries import (
    qr_create_category,
    qr_get_categories,
    qr_get_category_by_id,
    qr_get_category_by_name,
    qr_remove_category
)

def create_category(name):
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            # Checks if category already exists
            c.execute(qr_get_category_by_name(name=name))
            result = c.fetchall()    
            if c.fetchall() != ():
                raise CouldNotRegisterCategory
            
            # Creates category
            c.execute(qr_create_category(name=name))
        conn.commit()
    except CouldNotRegisterCategory as e:
        result = error_resp(e)
    except CategoryNotFound as e:
        result = error_resp(e)
    finally:
        conn.close()
        return result

def get_categories():
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(qr_get_categories())
            result = c.fetchall()
            if result != ():
                raise CategoryNotFound
        conn.commit() 
    finally:
        conn.close()
        return result

def create_category(name):
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(qr_create_category(name=name))
            result = c.fetchall()    
    finally:
        conn.close()
        return result

def create_category(name):
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(qr_create_category(name=name))
            result = c.fetchall()    
    finally:
        conn.close()
        return result