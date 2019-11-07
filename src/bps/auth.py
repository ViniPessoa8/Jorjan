from ..util.jwt_manager import encode
from flask import Blueprint, request, abort
from random import randint
from ..util.errors import InvalidRequest, InvalidLogin, error_resp
from ..db.auth import (
    check_login_email, 
    check_auth,
    logout,
    check_login_username,
    update_auth_key
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    params = request.json
    
    try:
        if params == None or not 'password' in params :
            raise InvalidRequest

        ps   = params['password']
        user = None

        if 'email' in params:
            email = params['email']
            user  = check_login_email(email=email, ps=ps)
        elif 'username' in params:
            username = params['username']
            user = check_login_username(username=username, ps=ps)
        else:
            raise InvalidRequest

        if (user == None):
            raise InvalidLogin

        user['auth'] = encode({'email': user['email'], 'ps': ps, 'bullet': randint(0, 255)})
            
        update_auth_key(auth=user['auth'], email=user['email'], ps=ps)

        return {
            'user': {
                'name'    : user['name'],
                'email'   : user['email'],
                'auth'    : user['auth'],
                'username': user['username']
            }
        }
    except BaseException as e:
        return error_resp(e)

@bp.route('/logout', methods=['DELETE'])
def user_logout():
    auth = request.headers.get("Authorization") 
    
    user = check_auth(auth)
    if user == None:
        abort(403)
    
    try:
        result = logout(user['email'])

        return result
    except BaseException as e:
        return error_resp(e)
    