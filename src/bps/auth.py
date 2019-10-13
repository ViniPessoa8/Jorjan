from ..util.jwt_manager import decode, encode
from flask import Blueprint, request
from ..db.user import check_login, update_auth_key

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    ps    = request.json['password']

    user = check_login(email=email, ps=ps)
    if (user != None):
        auth_key = encode({'email': email, 'ps': ps})
        
    update_auth_key(auth=auth_key, email=email, ps=ps)

    return {
        'user': {
            'nome' : user["nome"],
            'email': user["email"],
            'auth' : user["auth"]
        }
    }
