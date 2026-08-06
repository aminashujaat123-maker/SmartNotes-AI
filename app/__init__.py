from flask import Flask

from config import Config
from app.extensions import db, bcrypt, login_manager


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from app.models.user import User


    @login_manager.user_loader
    def load_user(user_id):
     return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.notes import notes

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(notes)

    return app