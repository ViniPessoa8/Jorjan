from flask import Blueprint, request, abort
from ..util.constants import SALE_STATES
from ..util.errors import error_resp, InvalidRequest, CouldNotFindProductOwner, ProductOutOfStock
from ..db.auth import check_auth
from ..db.user import get_product_owner
from ..db.product import get_product_id, update_product_stock
from ..db.sale import (
    get_cart_product,
    update_product_cart,
    check_cart_exists,
    get_buyer_sale_info,
    check_sale_exists_seller,
    add_product_cart,
    add_product_new_cart,
    get_sale_by_buyer,
    update_sale_status,
    get_cart_info,
    remove_product_from_cart
)

bp = Blueprint('sale', __name__, url_prefix='/sale')

@bp.route('/cart', methods=['POST'])
def add_to_cart():
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
        
        cart           = check_cart_exists(buyer_id=buyer['id'])
        product_result = get_product_id(params['product_id'])

        if product_result == None:
            raise InvalidRequest
        elif 'error' in product_result:
            return product_result

        old_quantity = product_result['stock']

        if cart != None:
            cart_product = get_cart_product(product_id=params['product_id'], cart_id=cart['id'])
            if cart_product == None:
                if params['quantity'] > product_result['stock']:
                    raise ProductOutOfStock
                
                new_stock = product_result['stock'] - params['quantity']
                result = update_product_stock(product_id=params['product_id'], quantity=new_stock)
                if 'error' in result:
                    return result
                    
                result = add_product_cart(product_id=params['product_id'], quantity=params['quantity'], cart_id=cart['id'])
            else:
                new_stock = product_result['stock'] + (cart_product['quantity'] - params['quantity'])
                if new_stock < 0:
                    raise ProductOutOfStock

                result = update_product_stock(product_id=params['product_id'], quantity=new_stock)
                result = update_product_cart(product_id=params['product_id'], quantity=params['quantity'], cart_id=cart['id'])
        else:
            seller = get_product_owner(product_id=params['product_id'])
            if 'error' in seller:
                raise CouldNotFindProductOwner
            
            new_stock = product_result['stock'] - params['quantity']
            result = update_product_stock(product_id=params['product_id'], quantity=new_stock)
            if 'error' in result:
                update_product_stock(product_id=params['product_id'], quantity=old_quantity)
                return result
            
            result = add_product_new_cart(buyer_id=buyer['id'], product_id=params['product_id'], quantity=params['quantity'], seller_id=seller['id'])

        if 'error' in result:
            update_product_stock(product_id=params['product_id'], quantity=old_quantity)

        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/cart', methods=['DELETE'])
def remove_from_cart():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    user = check_auth(auth)
    if user == None:
        abort(403)
    
    try:
        if params == None or not 'product_id' in params:
            raise InvalidRequest
        
        cart = check_cart_exists(buyer_id=user['id'])
        if cart == None:
            raise InvalidRequest
        
        product_result = get_product_id(params['product_id'])
        if product_result == None:
            raise InvalidRequest
        elif 'error' in product_result:
            return product_result

        cart_product = get_cart_product(product_id=params['product_id'], cart_id=cart['id'])
        if cart_product == None:
            raise InvalidRequest

        new_stock = product_result['stock'] + cart_product['quantity']
        result = update_product_stock(product_id=params['product_id'], quantity=new_stock)
        if 'error' in result:
            return result
        
        cart_product['quantity']
        result = remove_product_from_cart(product_id=params['product_id'], cart_id=cart['id'])
    
        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/cart', methods=['GET'])
def get_cart():
    auth   = request.headers.get('Authorization')
    result = None

    user = check_auth(auth)
    if user == None:
        abort(403)
    
    try:
        cart = check_cart_exists(buyer_id=user['id'])
        if cart == None:
            raise InvalidRequest

        result = get_cart_info(cart_id=cart['id'])

        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/buy', methods=['GET'])
def request_sale():
    auth = request.headers.get('Authorization')

    user = check_auth(auth)
    if user == None:
        abort(403)

    try:
        sale = get_sale_by_buyer(buyer_id=user['id'], status=SALE_STATES['CART'])
        if sale == None:
            raise InvalidRequest
        
        result = update_sale_status(sale_id=sale['id'], status=SALE_STATES['WAITING_CONFIRMATION'])

        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/confirm_request', methods=['GET'])
def confirm_request():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    seller = check_auth(auth)
    if seller == None:
        abort(403)
    
    try:
        if params == None or not 'sale_id' in params:
            raise InvalidRequest
        
        sale = check_sale_exists_seller(seller_id=seller['id'], sale_id=params['sale_id'])
        if sale == None or sale['status'] != SALE_STATES['WAITING_CONFIRMATION']:
            raise InvalidRequest

        result = update_sale_status(sale_id=sale['id'], status=SALE_STATES['WAITING_DELIVERY'])
    
        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/confirm_delivery', methods=['GET'])
def confirm_delivery():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    seller = check_auth(auth)
    if seller == None:
        abort(403)
    
    try:
        if params == None or not 'sale_id' in params:
            raise InvalidRequest
        
        sale = check_sale_exists_seller(seller_id=seller['id'], sale_id=params['sale_id'])
        if sale == None or sale['status'] != SALE_STATES['WAITING_DELIVERY']:
            raise InvalidRequest

        result = update_sale_status(sale_id=sale['id'], status=SALE_STATES['FINISHED'])
    
        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/cancel_request', methods=['DELETE'])
def cancel_request():
    auth = request.headers.get('Authorization')
    params = request.args
    
    user = check_auth(auth)
    if user == None:
        abort(403)

    try:
        if params == None or not 'sale_id' in params:
            raise InvalidRequest
        
        sale = get_buyer_sale_info(sale_id=params['sale_id'], buyer_id=user['id'])
    
        if (
            sale == None or not (
                sale['status'] <= SALE_STATES['WAITING_CONFIRMATION'] and 
                sale['status'] >= SALE_STATES['CART']
            )
        ):
            raise InvalidRequest
        
        result = update_sale_status(sale_id=sale['id'], status=SALE_STATES['CANCELED'])

        return result
    except BaseException as e:
        return error_resp(e)
