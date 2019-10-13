from flask import Blueprint
from ..db.user import get_all_users

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/list', methods=['GET'])
def user_list():
    result = get_all_users()
    return {
        "users": result
    }
    
