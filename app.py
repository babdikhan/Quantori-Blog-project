import os

from flask import Flask
from src.admin import add_admin
from src import auth, blog, db
from src.api.auth import auth_blueprint
from src.api.blog import blog_blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="src/templates",
        static_folder="src/static",
    )
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:password@localhost:5434/flask_db"
    app.config["SQLALCHEMY_SESSION_OPTIONS"] = {"expire_on_commit": False}
    app.config["SECRET_KEY"] = "your_secret_key_here"

    db.init_app(app)

    app.config["IPYTHON_CONFIG"] = {
        "InteractiveShell": {
            "colors": "Linux",
            "confirm_exit": False,
        },
    }

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(blog_blueprint)

    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

    add_admin(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
