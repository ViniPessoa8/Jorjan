from flask import Blueprint, request, abort
from ..util.errors import error_resp, InvalidRequest
from ..db.auth import check_auth
from ..db.product import (
    register_new_product,
    get_products,
    get_products_seller,
)
from ..db.category import get_category_by_id
from ..db.user import get_user_name_by_id

bp = Blueprint('product', __name__, url_prefix='/product')

@bp.route('/new', methods=['POST'])
def product_register():
    params = request.json
    auth   = request.headers.get('Authorization')

    owner = check_auth(auth)
    if owner == None:
        abort(403)

    try:
        if (
            params == None or
            not 'name'        in params or
            not 'description' in params or
            not 'category_id' in params or
            not 'price'       in params or
            not 'stock'       in params
        ):
            raise InvalidRequest
            
        result = register_new_product(product=params, owner_id=owner["id"])
        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/all', methods=['GET'])
def get_all_products():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    user = check_auth(auth)
    if user == None:
        abort(403)

    try:    
        result = get_products()
    except BaseException as e:
        result = error_resp(e)
    finally:
        return result

@bp.route('/info', methods=['GET'])
def get_info_product():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    user = check_auth(auth)
    if user == None:
        abort(403)

    try:
        if (
            params == None or
            not 'slr' in params or
            not 'ctg' in params
        ):
            raise InvalidRequest
        
        cat_id    = params['ctg']
        seller_id = params['slr']

        seller = get_user_name_by_id(id=seller_id)
        category = get_category_by_id(id=cat_id)

        if seller == None or category == None:
            raise InvalidRequest

        result = {
            'category': category['name'],
            'seller': seller['name']
        }
    except BaseException as e:
        result = error_resp(e)
    finally:
        return result