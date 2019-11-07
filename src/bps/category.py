from ..config.db import get_connection
from flask import Blueprint, request, abort
from ..util.errors import error_resp, InvalidRequest, CouldNotRegisterCategory, EmptyCategoryTable, CategoryNotFound
from ..db.auth import check_auth
from ..db.category import (
    register_category,
    get_categories,
    get_category_by_id,
    get_category_by_name,
    remove_category_by_id
)

bp = Blueprint('category', __name__, url_prefix='/category')

@bp.route('/new', methods=['POST'])
def category_register():
    params = request.json
    auth   = request.headers.get('Authorization')
    
    buyer = check_auth(auth)  
    if buyer == None:
        abort(403)

    try:
        if (params == () or
        not 'name' in params
        ):
            raise InvalidRequest
        
        name = params["name"]
        result = register_category(name=name)

    except InvalidRequest:
        result = error_resp(e)
    except BaseException as e:
        result = error_resp(e)
    finally:
        return result


@bp.route('/', methods=['GET'])
def category_list():
    params = request.args
    auth   = request.headers.get('Authorization')
    result = None

    buyer = check_auth(auth)  
    if buyer == None:
        abort(403)

    try:
        if ('id' in params):
            id = params["id"]
            result = get_category_by_id(id=id)

        elif ('name' in params):
            name = params["name"]
            result = get_category_by_name(name=name)

        else:  
            result = get_categories()      
    except InvalidRequest:
        return error_resp(e)
    except BaseException as e:
        return error_resp(e)
    finally:
        return result


@bp.route('/remove', methods=['POST'])
def category_remove():
    params = request.json
    auth   = request.headers.get('Authorization')
    
    buyer = check_auth(auth)  
    if buyer == None:
        abort(403)

    try:
        if (params == () or
            not 'id' in params
        ):
            raise InvalidRequest

        id = params["id"]
        result = remove_category_by_id(id=id)

    except BaseException as e:
        result = error_resp(e)
    finally:
        return result
