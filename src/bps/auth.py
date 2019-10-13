from ..util.jwt_manager import decode, encode
from flask import Blueprint, request

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    ps    = request.json['password']

    encoded = encode({'email': email, 'ps': ps})
    print(encoded)

    decoded = decode(encoded)
    print(decoded)

    return 'login'