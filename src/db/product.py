from ..config.db import get_connection
from ..util.errors import error_resp, CouldNotRegisterProduct
from .queries.product_queries import (
    qr_register_product
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
        result = error_resp(CouldNotRegisterProduct().__str__())
    finally:
        conn.close()
        return result