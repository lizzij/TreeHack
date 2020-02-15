from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flaskr.db import get_db

bp = Blueprint("record", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""

    return render_template("record/index.html")
