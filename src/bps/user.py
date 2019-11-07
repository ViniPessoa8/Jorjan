from flask import Blueprint, request, abort
from ..util.errors import InvalidRequest, CouldNotUpdateUser, CouldNotRegisterUser, error_resp

from ..db.user import (
    get_all_users, 
    register_new_user, 
    get_info, 
    update_user_pass, 
    get_history,
    get_available_sellers, 
    get_user_state_by_id, 
    set_user_state_by_id
)


from ..db.auth import check_auth

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/list', methods=['GET'])
def user_list():
    result = get_all_users()
    return { "users": result }

@bp.route('/register', methods=['POST'])
def user_register():
    params = request.json
    
    try:
        if (
            params == None or
            not 'name'     in params or
            not 'email'    in params or
            not 'password' in params or
            not 'username' in params
        ):
            raise InvalidRequest

        name     = params["name"]
        email    = params["email"]
        ps       = params["password"]
        username = params["username"]

        result = register_new_user(name=name, email=email, ps=ps, username=username)
        
        return result
    except BaseException as e:
        return error_resp(e)
    
@bp.route('/info', methods=['GET'])
def user_info():
    auth   = request.headers.get("Authorization")
    result = get_info(auth)

    if result == None:
        abort(403)

    return result

@bp.route('/password', methods=['PUT'])
def user_password():
    auth   = request.headers.get("Authorization")
    params = request.json
    
    user = check_auth(auth)
    if user == None:
        abort(403)

    try:
        if params == None or not 'password' in params:
            raise InvalidRequest

        new_pass = request.json["password"]

        user = update_user_pass(email=user["email"], new_pass=new_pass)

        if user == None:
            raise CouldNotUpdateUser

        return { "auth": auth }
    except BaseException as e:
        return error_resp(e)

@bp.route('/history', methods=['GET'])
def get_user_history():
    auth   = request.headers.get("Authorization")
    
    user = check_auth(auth)
    if user == None:
        abort(403)
    
    result = get_history(user_id=user['id'])
    return result

@bp.route('/state', methods=['PUT'])
def user_set_state():
    auth   = request.headers.get("Authorization")
    params = request.json

    user = check_auth(auth)
    if user == None:
        abort(403)

    try:
        if( 'id'    in params and
            'state' in params
            ):
            id = user['id']
            state = user['state']
            return set_user_state_by_id(id=id, state=state)
        else:
            raise InvalidRequest
    except InvalidRequest as e:
        return error_resp(e)

@bp.route('/state', methods=['GET'])
def user_get_state():
    auth   = request.headers.get("Authorization")
    params = request.args

    user = check_auth(auth)
    if user == None:
        abort(403)

    try:
        if 'id' in params:
            id = user['id']
            return get_user_state_by_id(id=id)
        else:
            raise InvalidRequest
    except InvalidRequest as e:
        return error_resp(e)
    
@bp.route('/sellers', methods=['GET'])
def user_get_available_sellers():
    auth = request.headers.get("Authorization")

    user = check_auth(auth)
    if user == None:
        abort(403)
    try:
        return get_available_sellers()
    except BaseException as e:
        return error_resp(e)
