from flask import Blueprint, request, abort
from ..db.user import get_all_users, register_new_user, get_info, update_user_pass
from ..db.auth import check_auth

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/list', methods=['GET'])
def user_list():
    result = get_all_users()
    return { "users": result }

@bp.route('/register', methods=['POST'])
def user_register():
    params = request.json

    name     = params["name"]
    email    = params["email"]
    ps       = params["password"]
    username = params["username"]

    result = register_new_user(name=name, email=email, ps=ps, username=username)

    if result == None:
        abort(500)

    return result
    
@bp.route('/info', methods=['GET'])
def user_info():
    auth   = request.headers.get("Authorization")
    result = get_info(auth)

    if result == None:
        abort(403)

    return result

@bp.route('/password', methods=['PUT'])
def user_password():
    auth     = request.headers.get("Authorization")
    new_pass = request.json["password"]

    user_email = check_auth(auth)

    if user_email == None:
        abort(403)

    user_email = user_email["email"]
    user_email = update_user_pass(user_email, new_pass)

    if user_email == None:
        return { "status": False } 

    return { "status": True }
