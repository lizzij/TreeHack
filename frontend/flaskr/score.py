import functools
import json
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
import urllib.parse
from flaskr.db import get_db

bp = Blueprint("score", __name__, url_prefix="/score")

@bp.route("/<string:word_analysis>", methods=("GET", "POST"))
def display_score(word_analysis):
    """display a dashboard for score """
    default_word_analysis = [
        {
            "is_match": True,
            "true_words": ["I"],
            "spoken_words": ["I"],
            "type": None,
            "conf": 50,
        },
        {
            "is_match": False,
            "true_words": ["love"],
            "spoken_words": ["dove"],
            "type": "dyspraxia",
            "conf": 50,
        },
        {
            "is_match": False,
            "true_words": ["cheese"],
            "spoken_words": ["glove", "grove", "shove"],
            "type": "stutter",
            "conf": 50,
        },
        {
            "is_match": True,
            "true_words": ["please"],
            "spoken_words": ["please"],
            "type": None,
            "conf": 75,
        }
    ]
    if word_analysis is None or len(word_analysis) == 0:
        word_analysis = default_word_analysis
    else:
        word_analysis = json.loads(urllib.parse.unquote(word_analysis))
        if len(word_analysis) == 0 or 'words_analysis' not in word_analysis:
            word_analysis = default_word_analysis
            #return render_template("record/index.html")
        else:
            word_analysis = word_analysis['words_analysis']

    #raise Exception(word_analysis)
    words_cols = []
    # Entry format: ((true_word:, true_color:, spoken_word:, spoken_color:)
    for data in word_analysis:
        col = {
            "true_word": "",
            "true_color": "#FFF",
            "spoken_word": "",
            "spoken_color": "#FFF",
            "true_issue": "",
            "spoken_issue": "",
            "conf": -1,
        }
        colors = {
            "omission": "#E2E2E2",
            "stutter": "#FFC8D9",
            "dyspraxia": "#D6BBB6",
            "correct": "#B3DBCE",
            "filler": "##FFEFE0"
        }

        col['conf'] = data['conf']

        if isinstance(data["true_words"], str):
            col["true_word"] = data["true_words"]
            col["spoken_word"] = data["spoken_words"]
        else:
            col["true_word"] = " ".join(data["true_words"])
            col["spoken_word"] = " ".join(data["spoken_words"])

        if data["is_match"]:
            col["true_color"] = colors["correct"]
            col["spoken_color"] = colors["correct"]
        elif len(data["spoken_words"]) == 0:
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
        elif len(data["true_words"]) == 0:
            col["spoken_color"] = colors["stutter"]
            col["spoken_issue"] = "stutter"
        elif data["type"] == "stutter":
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
            col["spoken_color"] = colors["stutter"]
            col["spoken_issue"] = "stutter"
        elif data["type"] == "dyspraxia":
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
            col["spoken_color"] = colors["dyspraxia"]
            col["spoken_issue"] = "dyspraxia"
        elif data["type"] == "filler":
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
            col["spoken_color"] = colors["filler"]
            col["spoken_issue"] = "filler"
        else:
            col["true_color"] = colors["omission"]
            col["true_issue"] = "omission"
            col["spoken_color"] = colors["stutter"]
            col["spoken_issue"] = "stutter"
        words_cols.append(col)

    return render_template("score/index.html", word_analysis=words_cols)
