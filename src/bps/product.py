from flask import Blueprint, request, abort
from ..util.errors import error_resp, InvalidRequest
from ..db.auth import check_auth
from ..db.product import (
    register_new_product,
    get_products,
    get_products_seller,
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
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    user = check_auth(auth)
    # if user == None:
    #     abort(403)


    try:    
        if params:
            seller_id = params['seller_id']
            if seller_id:
                # print(1)
                result = get_products_seller(seller_id) 
                print(result)

            else:
                result = 'No Seller'
        else:
            result = get_products()
    except BaseException as e:
        result = error_resp(e)
    finally:
        return {'result': result}