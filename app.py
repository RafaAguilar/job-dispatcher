import os

from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api = swagger.docs(Api(app), apiVersion='0.1')
    db.init_app(app)
    set_views(api)
    return app


def set_views(api):
    """
    This mutation is only to avoid circular imports issues.
    """
    from views.jobs import JobsCRUD
    from views.jobs import JobsList
    api.add_resource(JobsList, '/jobs')
    api.add_resource(JobsCRUD, '/jobs/<string:job_id>')

if __name__ == '__main__':
    app = create_app()
    app.run()
