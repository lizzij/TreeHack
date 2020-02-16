#!/usr/bin/python3

import os

from flask import Flask, request, send_from_directory
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

    @app.route('/hello')
    def hello_world():
        return 'Hello, World!'

    # for face-api.js
    @app.route('/age_gender_model-weights_manifest.json')
    def serve_model1():
        return send_from_directory('static/weights', 'age_gender_model-weights_manifest.json')

    @app.route('/age_gender_model-shard1')
    def serve_shard1():
        return send_from_directory('static/weights', 'age_gender_model-shard1')

    @app.route('/face_expression_model-weights_manifest.json')
    def serve_model2():
        return send_from_directory('static/weights', 'face_expression_model-weights_manifest.json')

    @app.route('/face_expression_model-shard1')
    def serve_shard2():
        return send_from_directory('static/weights', 'face_expression_model-shard1')

    @app.route('/face_landmark_68_model-weights_manifest.json')
    def serve_model3():
        return send_from_directory('static/weights', 'face_landmark_68_model-weights_manifest.json')

    @app.route('/face_landmark_68_model-shard1')
    def serve_shard3():
        return send_from_directory('static/weights', 'face_landmark_68_model-shard1')

    @app.route('/face_landmark_68_tiny_model-weights_manifest.json')
    def serve_model4():
        return send_from_directory('static/weights', 'face_landmark_68_tiny_model-weights_manifest.json')

    @app.route('/face_landmark_68_tiny_model-shard1')
    def serve_shard4():
        return send_from_directory('static/weights', 'face_landmark_68_tiny_model-shard1')

    @app.route('/face_recognition_model-weights_manifest.json')
    def serve_model5():
        return send_from_directory('static/weights', 'face_landmark_68_tiny_model-weights_manifest.json')

    @app.route('/face_recognition_model-shard1')
    def serve_shard5():
        return send_from_directory('static/weights', 'face_recognition_model-shard1')

    @app.route('/face_recognition_model-shard2')
    def serve_shard5_2():
        return send_from_directory('static/weights', 'face_recognition_model-shard2')

    @app.route('/mtcnn_model-weights_manifest.json')
    def serve_model6():
        return send_from_directory('static/weights', 'mtcnn_model-weights_manifest.json')

    @app.route('/mtcnn_model-shard1')
    def serve_shard6():
        return send_from_directory('static/weights', 'mtcnn_model-shard1')

    @app.route('/ssd_mobilenetv1_model-weights_manifest.json')
    def serve_model7():
        return send_from_directory('static/weights', 'ssd_mobilenetv1_model-weights_manifest.json')

    @app.route('/ssd_mobilenetv1_model-shard1')
    def serve_shard7():
        return send_from_directory('static/weights', 'ssd_mobilenetv1_model-shard1')

    @app.route('/ssd_mobilenetv1_model-shard2')
    def serve_shard7_2():
        return send_from_directory('static/weights', 'ssd_mobilenetv1_model-shard2')

    @app.route('/tiny_face_detector_model-weights_manifest.json')
    def serve_model8():
        return send_from_directory('static/weights', 'tiny_face_detector_model-weights_manifest.json')

    @app.route('/tiny_face_detector_model-shard1')
    def serve_shard8():
        return send_from_directory('static/weights', 'tiny_face_detector_model-shard1')

    @app.route('/practice/menu_icon.png')
    def serve_menu_icon():
        return send_from_directory('static', 'menu_icon.png')

    @app.route('/practice/github_link_icon.png')
    def serve_link_icon():
        return send_from_directory('static', 'github_link_icon.png')

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
