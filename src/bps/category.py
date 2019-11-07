from flask import Blueprint, request, abort
from ..util.errors import error_resp, InvalidRequest
from ..db.auth import check_auth
from ..db.category import (
    register_category,
    get_categories,
    get_category_by_id,
    get_category_by_name,
    remove_category_by_id
)

bp = Blueprint('category', __name__, url_prefix='/category')

@bp.route('/register', methods=['POST'])
def category_register():
    params = request.json
    auth   = request.headers.get('Authorization')
    result = None
    
    buyer = check_auth(auth)  
    if buyer == None:
        abort(403)

    try:
        if (
            params == None or
            not 'name' in params
        ):
            raise InvalidRequest

        name = params["name"]
        result = register_category(name=name)

        return result
    except BaseException as e:
        return error_resp(e)

@bp.route('/get', methods=['GET'])
def category_list():
    params = request.json
    auth   = request.headers.get('Authorization')
    result = None
    
    buyer = check_auth(auth)  
    if buyer == None:
        abort(403)

    try:
        if ( params != None and  (
            not 'name'  in params or
            not 'id'    in params)
        ):
            raise InvalidRequest

        if (params == None):        
            result = get_categories()
            return { "categories": result }
        
        if ('name' in params):
            name = params["name"]
            result = get_category_by_name(name=name)
            return { "category": result}

        if ('id' in params):
            id = params["id"]
            result = get_category_by_id(id=id)
            return { "category": result}
    except BaseException as e:
        return error_resp(e)

@bp.route('/remove', methods=['POST'])
def category_remove():
    params = request.json
    auth   = request.headers.get('Authorization')
    
    buyer = check_auth(auth)  
    if buyer == None:
        abort(403)

    try:
        if (
            params == None or
            not 'id' in params
        ):
            raise InvalidRequest

        id = params["id"]
        result = remove_category_by_id(id=id)
        
        return result
    except BaseException as e:
        return error_resp(e)