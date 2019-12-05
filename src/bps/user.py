from flask import Blueprint, request, abort
from flask_mail import Message
from random import randint
from ..util.errors import InvalidRequest, CouldNotUpdateUser, CouldNotRegisterUser, CouldNotFindUser, error_resp
from ..util.jwt_manager import encode
from ..db.user import (
    get_all_users, 
    register_new_user, 
    get_info, 
    update_user_pass, 
    get_history,
    get_available_sellers, 
    get_user_state_by_id, 
    set_user_state_by_id,
    update_user_profile,
    check_user_email,
    get_user_by_id,
    update_auth_key_user
)


from ..db.auth import check_auth

def create_user_blueprint(mail):
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
            if not 'state' in params:
                raise InvalidRequest

            return set_user_state_by_id(id=user['id'], state=params['state'])
        except InvalidRequest as e:
            return error_resp(e)

    @bp.route('/state', methods=['GET'])
    def user_get_state():
        auth   = request.headers.get("Authorization")
        params = request.args

        user = check_auth(auth)
        if user == None:
            abort(403)

        return get_user_state_by_id(id=user['id'])
        
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

    @bp.route('/update', methods=['PUT'])
    def user_update_profile():
        auth = request.headers.get("Authorization")
        params = request.json

        user = check_auth(auth)
        if user == None:
            abort(403)

        id = user['id']
        user = get_user_by_id(id)

        name = user['name']
        username = user['username']
        password = user['password']

        try:
            if 'name' in params:
                name = params['name']
            if 'username' in params:
                username = params['username']
            if 'password' in params:
                password = params['password']

            return update_user_profile(id, name, username, password)
        except BaseException as e:
            return error_resp(e)

    @bp.route('/recover', methods=['GET'])
    def user_recover_password():
        params = request.args

        if params == None or not 'email' in params:
            raise InvalidRequest
        
        try:
            user = check_user_email(params['email'])

            if user == None:
                raise CouldNotFindUser

            key = encode({ 'email': user['email'], 'bullet': randint(0, 255) })

            result = update_auth_key_user(auth=key, email=user['email'])

            if result == None:
                raise CouldNotUpdateUser

            mensagem = f"""
            Caro(a) {user['name']}, foi solicitada a redefinição de sua senha. Para confirmar, acesse esse
            """

            msg = Message("Reset de Senha", sender="noreply@teste.com", recipients=["teste@teste.com"])
            msg.body = f'{mensagem} link'
            msg.html = f'<p>{mensagem}<a href="http://localhost:3000/reset/{key}">link</a></p>'
            mail.send(msg)

            return { 'status': 'Done!' }
        except BaseException as e:
            return error_resp(e)

    return bp