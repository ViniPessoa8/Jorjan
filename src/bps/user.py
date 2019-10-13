from flask import Blueprint, request
from ..db.user import get_all_users, register_new_user

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
