"""
UMP Flask Application Configuration

This module provides configuration settings and functions for the Flask app.
"""

from os import environ as env
from dotenv import load_dotenv
from flask import Flask
from mongoengine import connect
from flask_security import (
    Security,
    MongoEngineUserDatastore,
    uia_email_mapper,
)
from .views import blueprint
from flask_mailman import Mail
from typing import Optional

load_dotenv()


class configure_app():
    def basic_auth(app: Flask,
                   debug: Optional[bool] = False,
                   SECURITY_REGISTERABLE: Optional[bool] = False,
                   ) -> Flask:
        """
        Configure basic auth for the given app.

        Args:
            app: The Flask application instance to configure.
            debug: Whether to enable debug mode for the app.
            SECURITY_REGISTERABLE: Whether to enable user registration.

        Returns:
            The configured app.
        """
        app.config['DEBUG'] = debug or (env.get("DEBUG") == "True")

        # for security these variables should be set in .env
        app.config['SECRET_KEY'] = env.get("SECRET_KEY")
        app.config['SECURITY_PASSWORD_SALT'] = (
            env.get("SECURITY_PASSWORD_SALT").encode("utf-8")
            )
        if not app.config.get('SECRET_KEY'):
            raise Exception("SECRET_KEY is not set in .env file")
        if not app.config.get('SECURITY_PASSWORD_SALT'):
            raise Exception("SECURITY_PASSWORD_SALT is not set in .env file")

        app.config['SECURITY_REGISTERABLE'] = SECURITY_REGISTERABLE
        app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
        app.register_blueprint(blueprint)
        return app

    def with_mail(app: Flask,
                  SECURITY_CONFIRMABLE: Optional[bool] = False,
                  SECURITY_RECOVERABLE: Optional[bool] = False,
                  SECURITY_CHANGEABLE: Optional[bool] = False,
                  ) -> Flask:
        """
        Configure the Mail features for the given app.

        Args:
            app: The Flask application instance to configure.
            SECURITY_CONFIRMABLE: Whether to enable email confirmation.
            SECURITY_RECOVERABLE: Whether to enable password recovery.
            SECURITY_CHANGEABLE: Whether to enable password changes.

        Returns:
            The configured app.
        """
        # for security these variables should be set in .env
        assert env.get('MAIL_SERVER') is not None, \
            "MAIL_SERVER is not set in .env file.\n" \
            "Configuration variables should be set in the .env file."
        assert env.get("MAIL_PORT") is not None, \
            "MAIL_PORT is not set in .env file.\n" \
            "Configuration variables should be set in the .env file."
        assert str(env.get("MAIL_PORT")).isdigit(), \
            "MAIL_PORT is not a number (for example 25, 465 or 587)"
        assert not (env.get('MAIL_USE_TLS') == "True" and
                    env.get('MAIL_USE_SSL') == "True"), \
            "MAIL_USE_TLS and MAIL_USE_SSL cannot be both set to True"
        assert env.get('MAIL_USERNAME') is not None, \
            "MAIL_USERNAME is not set in .env file.\n" \
            "Configuration variables should be set in the .env file."
        assert env.get('MAIL_PASSWORD') is not None, \
            "MAIL_PASSWORD is not set in .env file.\n" \
            "Configuration variables should be set in the .env file."

        app.config['MAIL_SERVER'] = env.get("MAIL_SERVER")
        app.config['MAIL_PORT'] = env.get("MAIL_PORT")
        app.config['MAIL_USE_TLS'] = env.get("MAIL_USE_TLS") == "True"
        app.config['MAIL_USE_SSL'] = env.get("MAIL_USE_SSL") == "True"
        app.config['MAIL_USERNAME'] = env.get("MAIL_USERNAME")
        app.config['MAIL_PASSWORD'] = env.get("MAIL_PASSWORD")

        app.config['SECURITY_SEND_REGISTER_EMAIL'] = SECURITY_CONFIRMABLE
        app.config["SECURITY_CONFIRMABLE"] = SECURITY_CONFIRMABLE
        app.config["SECURITY_RECOVERABLE"] = SECURITY_RECOVERABLE
        app.config["SECURITY_CHANGEABLE"] = SECURITY_CHANGEABLE
        mail = Mail(app)
        return app

    def security(app: Flask) -> Security:
        """
        Create a Flask-Security instance for the given app.

        Args:
            app: The Flask application instance to configure.

        Returns:
            A Flask-Security instance for the given app.
        """
        from .models import User, Role
        db_name = env.get("DB_NAME", "mydatabase")
        db = connect(alias=db_name, db=db_name,
                     host="mongodb://localhost", port=27017)
        # Setup Flask-Security
        user_datastore = MongoEngineUserDatastore(db, User, Role)
        security = Security(app, user_datastore)
        return security
