from flask import Blueprint, request, abort
from ..util.errors import error_resp, InvalidRequest
from ..db.auth import check_auth
from ..db.product import (
    register_new_product,
    get_products
)

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
    params = request.json
    auth   = request.headers.get('Authorization')

    user = check_auth(auth)
    if user == None:
        abort(403)

    try:    
        result = get_products()
        return result
    except BaseException as e:
        return error_resp(e)