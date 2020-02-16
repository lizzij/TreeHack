import os

from flask import Flask, request
import houndify

clientId = "6gG_SPtR_YNCOaTvI0IK5w=="
clientKey = "3lHbv1T8X5UDUa4tGhogToKa9iBIAMLdGK02zUq-ZwsBZ6BdaAElh42Z-nVnDoKfiu_3zCYxqrL4Ux2Iqs7X9A=="
userId = "test_user"
requestInfo = {
  "Latitude": 37.388309,
  "Longitude": -121.973968
}

client = houndify.TextHoundClient(clientId, clientKey, userId, requestInfo)

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/textSearchProxy")
    def text_search_proxy():
        query = ' '.join(request.args.get('query').split('%20'))
        print("input query:", query)
        response = client.query(query)
        print(response)
        return response

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    # register the database commands
    from flaskr import db

    db.init_app(app)

    # apply the blueprints to the app
    from flaskr import record, score, practice

    app.register_blueprint(record.bp)
    app.register_blueprint(score.bp)
    app.register_blueprint(practice.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
