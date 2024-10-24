"""
UMP_flask.models
~~~~~~~~~~~~~~~~

This module defines the database models for the user and role management
system using MongoEngine. The models are integrated with Flask-Security
to handle user authentication, roles, and permissions.

Classes:
    - Role: Represents the different roles users can have in the app.
    - User: Represents users, including credentials, active status, and roles.

Environment Variables:
    - DB_NAME: The name of the MongoDB database. Defaults to "mydatabase"
      if not provided.

Dependencies:
    - mongoengine: A MongoDB Object-Document Mapper (ODM) for Python.
    - flask_security: Provides utilities for user authentication and
      role management.
"""


from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    ListField,
    ReferenceField,
    StringField,
)
from mongoengine import Document
from flask_security import UserMixin, RoleMixin
from os import environ
from dotenv import load_dotenv

load_dotenv()

if environ.get("TEST") == "True":
    db_name = "testdb" # For testing purposes
else:
    db_name = environ.get("DB_NAME", "mydatabase")


class Role(Document, RoleMixin):
    """
    The Role class represents the roles that users can have in the application.

    Fields:
    - name: The unique name of the role (e.g., 'admin', 'editor').
    - description: A brief description of the role.
    - permissions: A list of permissions associated with the role.

    Inherits:
    - Document: Base class from mongoengine to represent MongoDB documents.
    - RoleMixin: A mixin from Flask-Security that adds role-related methods.
    """

    name = StringField(max_length=80, unique=True, required=True)
    description = StringField(max_length=255)
    permissions = ListField(required=False)
    meta = {"db_alias": db_name}


class User(Document, UserMixin):
    """
    The User class represents the users of the application.

    Fields:
    - email: User's email address, which must be unique.
    - password: Hashed password for user authentication.
    - active: Boolean flag indicating whether the user is active.
    - fs_uniquifier: A unique string for Flask-Security's unique identifier.
    - confirmed_at: DateTime indicating when the user's email was confirmed.
    - roles: A list of roles assigned to the user (linked to the Role model).

    Inherits:
    - Document: Base class from mongoengine to represent MongoDB documents.
    - UserMixin: A mixin from Flask-Security that adds user-related methods.
    """

    email = StringField(max_length=255, unique=True, required=True)
    password = StringField(max_length=255, required=True)  # Hashed password
    active = BooleanField(default=True)
    fs_uniquifier = StringField(max_length=64, unique=True, required=True)
    confirmed_at = DateTimeField()
    roles = ListField(ReferenceField(Role), default=[])
    meta = {"db_alias": db_name}
