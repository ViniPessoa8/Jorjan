from ..config.db import get_connection
from ..util.constants import SALE_STATES
from ..util.errors import (
    error_resp, 
    CouldNotAddToCart,
    CouldNotStartCart, 
    CouldNotChangeSaleStatus,
    CouldNotCheckSaleSellerExists,
    CouldNotRemoveCartItem
)
from .queries.sale_queries import (
    qr_check_cart_exists,
    qr_check_sale_exists_seller,
    qr_add_to_cart,
    qr_create_cart,
    qr_get_cart_info,
    qr_get_sale_by_buyer,
    qr_get_sale_product,
    qr_update_sale_product,
    qr_update_sale_status,
    qr_remove_product_from_cart
)

def check_cart_exists(buyer_id):
    conn   = get_connection()
    result = None

    with conn.cursor() as c:
        c.execute(qr_check_cart_exists(buyer_id))
        result = c.fetchone()

        conn.close()
        return result

def add_product_cart(product_id, quantity, cart_id):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_get_sale_product(product_id=product_id, cart_id=cart_id))
            product = c.fetchone()

            if product == None:
                c.execute(qr_add_to_cart(product_id=product_id, quantity=quantity, cart_id=cart_id))
            else:
                c.execute(qr_update_sale_product(product_id=product_id, quantity=quantity, cart_id=cart_id))
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
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_create_cart(buyer_id=buyer_id, seller_id=seller_id))
        conn.commit()
        
        cart = check_cart_exists(buyer_id)
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
        
def get_sale_by_buyer(buyer_id, status):
    conn   = get_connection()
    result = None

    with conn.cursor() as c:
        c.execute(qr_get_sale_by_buyer(buyer_id, status))
        result = c.fetchone()

        conn.close()
        return result

def update_sale_status(sale_id, status):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_update_sale_status(sale_id=sale_id, status=status))
        conn.commit()

        result = {
            'sale_id': sale_id,
            'status': status
        }
    except BaseException:
        result = error_resp(CouldNotChangeSaleStatus())
    finally:
        conn.close()
        return result

def remove_product_from_cart(product_id, cart_id):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_remove_product_from_cart(product_id=product_id, cart_id=cart_id))
            conn.commit()

            cart = get_cart_info(cart_id)
            if cart == ():
                c.excute(qr_update_sale_status(sale_id=cart_id, status=SALE_STATES['CANCELED']))
                conn.commit()

        result = { 'product_id': product_id }
    except BaseException:
        result = error_resp(CouldNotRemoveCartItem())
    finally:
        print(result)
        conn.close()
        return result

def get_cart_info(cart_id):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_get_cart_info(cart_id=cart_id))
            result = c.fetchall()
        
        if len(result) == 0:
            return {}
        
        sale_id   = result[0]['sale_id']
        sale_date = result[0]['date']
        products  = list(map(lambda r: {
            'name':        r['product_name'],
            'id':          r['product_id'],
            'description': r['product_description'],
            'price':       r['price'],
            'quantity':    r['quantity'],
        }, result))

        result = { 
            'id': sale_id,
            'date': sale_date,
            'products': products
        }
    except BaseException:
        result = error_resp(CouldNotRemoveCartItem())
    finally:
        conn.close()
        return result

def check_sale_exists_seller(seller_id, sale_id):
    conn   = get_connection()
    result = None

    try:
        with conn.cursor() as c:
            c.execute(qr_check_sale_exists_seller(seller_id=seller_id, sale_id=sale_id))
            result = c.fetchone()
    except BaseException:
        result = error_resp(CouldNotCheckSaleSellerExists())
    finally:
        conn.close()
        return result