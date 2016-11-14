from flask_restful import Resource

from models.core_models import Job


class JobsFull(Resource):
    def get(self, job_id, deep=0):
        job, is_new = Job.get_unique(job_id)
        return {job_id: job.to_json(deep)}

    def put(self, job_id):
        job = Job.get_unique(job_id)
        print(job)
        # create new instance
        return {job.id}
