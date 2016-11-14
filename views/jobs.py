from flask_restful import Resource
from flask_restful import abort
from flask_restful_swagger import swagger

from models.core_models import Job
from database import db


class BaseView(Resource):

    def abort_if_does_not_exist(self, o_id):
        o, is_new = self.__managed_class__.get_unique(o_id)
        if is_new:
            self.__managed_class__.remove_from_cache(o)
            abort(404, message="Job {} doesn't exist".format(o_id))
        return o

    def pagination(self, page=1, step=10):
        pass


class JobsList(BaseView):
    __managed_class__ = Job

    "An Endpoint to manage Jobs"

    @swagger.operation(
        notes='This endpoint will list existing jobs',
        responseClass=__managed_class__.__name__,
        nickname='Jobs',
        parameters=[
            {
                "name": "job_id",
                "description": "Job Unique Identifier: is needed to seek for the job instance.",
                "required": True,
                "allowMultiple": False,
                "dataType": 'UUID',
                "paramType": "url"
            }
        ],
        responseMessages=[
            {
                "code": 302,
                "message": "Found. It should show a JSON Array with all the created jobs."
            }
        ]
    )
    def get(self):
        return db.session.query(Job).all()


class JobsCRUD(BaseView):
    __managed_class__ = Job

    "An endpoint to get a Job details"
    @swagger.operation(
        notes='This endpoint will handle the CRUD operation for jobs',
        responseClass=__managed_class__.__name__,
        nickname='Jobs',
        parameters=[],
        responseMessages=[
            {
                "code": 302,
                "message": "Found. The URL of the found job should be in the Location header"
            },
            {
                "code": 202,
                "message": "Feature not implemented YET. It will be soon"
            }
        ]
    )
    def get(self, job_id, deep=0):
        job = self.abort_if_does_not_exist(job_id)
        return {job_id: job.to_json(deep)}

    def delete(self, job_id):
        return abort(202, message="The API doesn't have the proper methods to delete objects yet, soon will have.")

    def put(self, job_id):
        return abort(202, message="The API doesn't have the proper methods to delete objects yet, soon will have.")
