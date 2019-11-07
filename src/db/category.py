from ..config.db import get_connection
from ..util.errors import error_resp, CouldNotRegisterCategory, CategoryNotFound, EmptyCategoryTable
from .queries.category_queries import (
    qr_register_category,
    qr_get_categories,
    qr_get_category_by_id,
    qr_get_category_by_name,
    qr_remove_category_by_id
)

def register_category(name):
    conn   = get_connection()
    result = ()
    try:
        with conn.cursor() as c:
            # Checks if category already exists
            c.execute(qr_get_category_by_name(name=name))
            result = c.fetchone()    
            if result != None:
                raise CouldNotRegisterCategory
            
            # Registers category
            c.execute(qr_register_category(name=name))
        conn.commit()
        result = {'name':name}
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
        result = {'categories':result}
    except EmptyCategoryTable as e:
        result = error_resp(e)
    finally:
        conn.close()
        return result

def get_category_by_name(name):
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(qr_get_category_by_name(name=name))
            result = c.fetchone()  
            print(result)  
            if result == None:
                raise CategoryNotFound
        
    except CategoryNotFound as e:
        result = error_resp(e)
    finally:
        conn.close()
        return result

def get_category_by_id(id):
    conn   = get_connection()
    result = ()

    try:
        with conn.cursor() as c:
            c.execute(qr_get_category_by_id(id=id))
            result = c.fetchone()    
            if result == None:
                raise CategoryNotFound
            
    except CategoryNotFound as e:
        result = error_resp(e)
    finally:
        conn.close()
        return result

def remove_category_by_id(id):
    conn   = get_connection()

    try:
        with conn.cursor() as c:
            # Checks if category already exists
            c.execute(qr_get_category_by_id(id=id))
            result = c.fetchone()    
            if result != None:
                raise CategoryNotFound
        
            # Removes category
            c.execute(qr_remove_category_by_id(id=id))
        c.commit()
        result = {'id':id}
    except CategoryNotFound as e:
        result = error_resp(e)
    finally:
        conn.close()
        return result