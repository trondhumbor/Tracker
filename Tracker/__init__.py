import os

from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
scheduler = APScheduler()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        TRACKER_TORRENT_FOLDER=os.path.join(app.instance_path, "torrents"),
        TRACKER_ANNOUNCE_INTERVAL=30,
        SCHEDULER_API_ENABLED=True,
        JOBS=[
            {
                "id": "job1", "func": "Tracker.task:reloadTorrents",
                "args": (), "trigger": "interval", "seconds": 10
            },
            {
                "id": "job2", "func": "Tracker.task:removeStalePeers",
                "args": (), "trigger": "interval", "seconds": 60
            }
        ],
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "tracker.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["TRACKER_TORRENT_FOLDER"], exist_ok=True)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
