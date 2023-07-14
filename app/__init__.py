from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .models import db,User,Admin



def create_app():
    
    app = Flask(__name__,static_url_path='/static')
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:MYSQL9pool@localhost/quickfix"
    app.config['SQLALCHEMY_TRACK_MMODIFICATIONS'] = False

    db.init_app(app)
    
    from .views import view
    from .auth import auth

    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    with app.app_context():
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = User.query.get(int(id))
        if user:
            return user

        # Load admin user
        admin = Admin.query.get(int(id))
        if admin:
            return admin

    
    return app


