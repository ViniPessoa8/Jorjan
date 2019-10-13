from .bps.user import bp as user_bp
from .bps.auth import bp as auth_bp

def register_bps(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)