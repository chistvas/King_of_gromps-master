from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from application.config import Config


db = SQLAlchemy()
migrate = Migrate(db)
mail = Mail()


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)

    from application.contact.routes import contact_me
    from application.main.routes import main
    from application.search_engine.routes import search_engine
    app.register_blueprint(contact_me)
    app.register_blueprint(main)
    app.register_blueprint(search_engine)
    
    return app