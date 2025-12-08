from flask import Flask
from dotenv import load_dotenv 
from .config import Config
from .extensions import db, login_manager
from .auth import auth_bp
from .orders import orders_bp
from .invoices import invoices_bp
from .shipments import shipments_bp

# app factory sencillo

def create_app():
    load_dotenv()  # lee variables de .env si existe
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(shipments_bp)

    with app.app_context():
        db.create_all()

    return app
