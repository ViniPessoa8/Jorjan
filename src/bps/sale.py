from flask import Blueprint, request, abort
from ..util.errors import error_resp, InvalidRequest
from ..db.auth import check_auth
from ..db.user import get_product_owner
from ..db.sale import (
    check_cart_exists,
    add_product_cart,
    add_product_new_cart
)

bp = Blueprint('sale', __name__, url_prefix='/sale')

@bp.route('/cart', methods=['POST'])
def request_sale():
    params = request.json
    auth   = request.headers.get('Authorization')
    result = None

    buyer = check_auth(auth)
    if buyer == None:
        abort(403)
    
    try:
        if (
            params == None or
            not 'product_id' in params or
            not 'quantity'   in params
        ):
            raise InvalidRequest
        
        cart = check_cart_exists(buyer_id=buyer['id'])

        if cart != None:
            result = add_product_cart(product_id=params['product_id'], quantity=params['quantity'], cart_id=cart['id'])
        else:
            seller = get_product_owner(product_id=params['product_id'])
            result = add_product_new_cart(buyer_id=buyer['id'], product_id=params['product_id'], quantity=params['quantity'], seller_id=seller['id'])

        return result
    except BaseException as e:
        return error_resp(e)
