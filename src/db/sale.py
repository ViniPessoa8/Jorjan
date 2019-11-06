from ..config.db import get_connection
from ..util.errors import error_resp, CouldNotAddToCart, CouldNotStartCart
from .queries.sale_queries import (
    qr_check_cart_exists,
    qr_add_to_cart,
    qr_create_cart
)

def check_cart_exists(buyer_id):
    conn = get_connection()
    result = None

    with conn.cursor() as c:
        c.execute(qr_check_cart_exists(buyer_id))
        result = c.fetchone()

        conn.close()
        return result

def add_product_cart(product_id, quantity, cart_id):
    conn = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_add_to_cart(product_id=product_id, quantity=quantity, cart_id=cart_id))
        conn.commit()

        result = {
            'product_id': product_id,
            'quantity': quantity
        }
    except BaseException:
        result = error_resp(CouldNotAddToCart())
    finally:
        conn.close()
        return result

def add_product_new_cart(buyer_id, product_id, quantity, seller_id):
    conn = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_create_cart(buyer_id=buyer_id, seller_id=seller_id))
        conn.commit()
        
        cart = check_cart_exists(buyer_id)
        print(cart)
        if 'error' in cart:
            raise CouldNotStartCart

        with conn.cursor() as c:
            c.execute(qr_add_to_cart(product_id=product_id, quantity=quantity, cart_id=cart['id']))
        conn.commit()

        result = {
            'product_id': product_id,
            'quantity': quantity,
            'seller_id': seller_id
        }
    except BaseException:
        result = error_resp(CouldNotAddToCart())
    finally:
        conn.close()
        return result
        