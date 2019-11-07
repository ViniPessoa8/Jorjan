from ..config.db import get_connection
from ..util.errors import (
    error_resp, 
    CouldNotRegisterProduct, 
    CouldNotGetProduct, 
    CouldNotListProducts,
    CouldNotUpdateProduct
)
from .queries.product_queries import (
    qr_register_product,
    qr_get_product_id,
    qr_update_product_stock,
    qr_get_products
)

def register_new_product(product, owner_id):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_register_product(product=product, owner_id=owner_id))
        conn.commit()

        result = { 
            'name': product['name'], 
            'description': product['description'], 
            'category_id': product['category_id'], 
            'price': product['price'], 
            'stock': product['stock'] 
        }
    except BaseException:
        result = error_resp(CouldNotRegisterProduct())
    finally:
        conn.close()
        return result

def get_products():
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_get_products())
            products = c.fetchall()

        result = { 'products': products }
    except BaseException:
        result = error_resp(CouldNotListProducts())
    finally:
        conn.close()
        return result

def get_product_id(product_id):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_get_product_id(product_id))
            result = c.fetchone()
    except BaseException:
        result = error_resp(CouldNotGetProduct())
    finally:
        conn.close()
        return result

def update_product_stock(product_id, quantity):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_update_product_stock(product_id=product_id, quantity=quantity))
        conn.commit()

        result = { 'product_id': product_id, 'quantity': quantity }
    except BaseException as e:
        print(e)
        result = error_resp(CouldNotUpdateProduct())
    finally:
        conn.close()
        return result