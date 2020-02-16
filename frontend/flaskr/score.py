import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

bp = Blueprint("score", __name__, url_prefix="/score")

@bp.route("/", methods=("GET", "POST"))
def display_score():
    """display a dashboard for score """

    word_analysis = [
        {
            "is_match": True,
            "true_words": ["I"],
            "pred_words": ["I"],
            "type": None,
            "conf_score": 50,
        },
        {
            "is_match": False,
            "true_words": ["love"],
            "pred_words": ["dove"],
            "type": "dyspraxia",
            "conf_score": 50,
        },
        {
            "is_match": False,
            "true_words": ["cheese"],
            "pred_words": ["glove", "grove", "shove"],
            "type": "stutter",
            "conf_score": 50,
        },
        {
            "is_match": True,
            "true_words": ["please"],
            "pred_words": ["please"],
            "type": None,
            "conf_score": 75,
        }
    ]

    words_cols = []
    # Entry format: ((true_word:, true_color:, pred_word:, pred_color:)
    for data in word_analysis:
        col = {
            "true_word": "",
            "true_color": "#FFF",
            "pred_word": "",
            "pred_color": "#FFF",
            "true_issue": "",
            "pred_issue": "",
        }
        colors = {
            "omission": "#5c5c5c",
            "stutter": "#821129",
            "dyspraxia": "#791a87",
            "correct": "#156b2c",
            "filler": "#9e5c00"
        }

        col["true_word"] = " ".join(data["true_words"])
        col["pred_word"] = " ".join(data["pred_words"])
        if data["is_match"]:
            col["true_color"] = colors["correct"]
            col["pred_color"] = colors["correct"]
        elif len(data["pred_words"]) == 0:
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
        elif len(data["true_words"]) == 0:
            col["pred_color"] = colors["stutter"]
            col["pred_issue"] = "stutter"
        elif data["type"] == "stutter":
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
            col["pred_color"] = colors["stutter"]
            col["pred_issue"] = "stutter"
        elif data["type"] == "dyspraxia":
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
            col["pred_color"] = colors["dyspraxia"]
            col["pred_issue"] = "dyspraxia"
        elif data["type"] == "filler":
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
            col["pred_color"] = colors["filler"]
            col["pred_issue"] = "filler"
        words_cols.append(col)

    return render_template("score/index.html", word_analysis=words_cols)
