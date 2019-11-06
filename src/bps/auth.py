from ..util.jwt_manager import encode
from flask import Blueprint, request
from random import randint
from ..db.auth import (
    check_login_email, 
    check_login_username,
    update_auth_key
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    params = request.json

    ps     = params['password']
    user   = None

    if 'email' in params:
        email = params['email']
        user  = check_login_email(email=email, ps=ps)
    elif 'username' in params:
        username = params['username']
        user = check_login_username(username=username, ps=ps)

    if (user == None):
        return { "error":"Usuário não encontrado." }

    user["auth"] = encode({'email': user["email"], 'ps': ps, 'bullet': randint(0, 255)})
         
    update_auth_key(auth=user["auth"], email=user["email"], ps=ps)

    return {
        'user': {
            'name'    : user["name"],
            'email'   : user["email"],
            'auth'    : user["auth"],
            'username': user["username"]
        }
    }
