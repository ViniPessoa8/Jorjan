from .bps.auth     import bp as auth_bp
from .bps.user     import create_user_blueprint as user_bp
from .bps.product  import bp as product_bp
from .bps.sale     import bp as sale_bp
from .bps.category import bp as category_bp

def register_bps(app, mail):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp(mail))
    app.register_blueprint(product_bp)
    app.register_blueprint(sale_bp)
    app.register_blueprint(category_bp)