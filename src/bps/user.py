from flask import Blueprint, request, abort
from ..db.user import get_all_users, register_new_user, get_info

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/list', methods=['GET'])
def user_list():
    result = get_all_users()
    return {
        "users": result
    }

@bp.route('/register', methods=['POST'])
def user_register():
    name  = request.json["name"]
    email = request.json["email"]
    ps    = request.json["password"]

    result = register_new_user(name=name, email=email, ps=ps)

    return result
    
@bp.route('/info', methods=['GET'])
def user_info():
    auth = request.headers.get("Authorization")
    result = get_info(auth)

    if result == None:
        abort(403)

    return result


