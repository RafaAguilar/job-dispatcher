import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from database import db


def create_app():
    app = Flask(__name__)
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api = Api(app)
    set_views(api)
    return app


def set_views(api):
    """
    This mutation is only to avoid circular imports issues.
    """
    from views.jobs import JobsFull
    api.add_resource(JobsFull, '/<string:job_id>')

if __name__ == '__main__':
    app = create_app()
    app.run()
