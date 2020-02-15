from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flaskr.db import get_db

bp = Blueprint("practice", __name__)


@bp.route("/")
def start_practice():
    """Practice wrong movements"""

    return render_template("practice/index.html")
