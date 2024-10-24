"""
views.py
~~~~~~~~

Defines application routes using Flask's Blueprint.

Blueprints:
    - root: Handles the home page route.

Routes:
    - /: Renders the default security template.

Dependencies:
    - flask: Manages views and templates.
"""

from flask import (Blueprint, render_template)


blueprint = Blueprint("root", __name__, template_folder="templates")


@blueprint.route("/")
def home():
    """
    The home page of the application.
    """
    return render_template("security/default.html")
