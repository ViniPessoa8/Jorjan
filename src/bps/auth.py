from ..util.jwt_manager import encode
from flask import Blueprint, request
from ..db.user import check_login, update_auth_key

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    ps    = request.json['password']

    user = check_login(email=email, ps=ps)
    if (user != None):
        user["auth"] = encode({'email': email, 'ps': ps}).decode("utf-8")
    else :
        return {
            "Error":"Usuário não encontrado."
        }
    
    update_auth_key(auth=user["auth"], email=email, ps=ps)

    return {
        'user': {
            'nome' : user["nome"],
            'email': user["email"],
            'auth' : user["auth"]
        }
    }
