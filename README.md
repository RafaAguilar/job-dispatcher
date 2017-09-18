# Flask Job Dispatcher Simulator

This is a small project to learn how to use Flask with two new libraries I just found:

- `flask_restful`[¹]
- `flask_sqlalchemy`[²]
- `flask_migrate`[³]

The main goal is to build a generic and reusable task synchronizer that allows to manage jobs, tasks, storages, clients, and related stuff.
 
In the first uploaded version (0.1) it will have the most abstract concepts, almost not usable in a real scenario, but my (could be ours..) goal to reach V1.0 is to simulate a Coffee spending machine, that have flavors, cups, time to serve, a _witdrawal window_ and such only configuring the application, through API, without specifying (hopefully) new _Coffee_ classes.
 
## Which technologies will we use?

_It includes much more techonlogies, but these are the interesting ones_
![Technoglies of interest](https://github.com/RafaAguilar/job-dispatcher/raw/master/diagrams/Techs%20Used.png)

## Which is the proposed Workflow?
_note: It will need another diagrams for sure._
![Proposed Workflow](https://rawgit.com/RafaAguilar/job-dispatcher/master/diagrams/Job%20Dispatcher%20Workflow(1).svg)

## Do you have any Classes Diagram?
_note: The Classes Diagram still lacks of labour, it is constanly changing now, and actually does not correspond with code in a 100% but almost._
![Classes Diagram](https://github.com/RafaAguilar/job-dispatcher/raw/master/diagrams/ClassesDiagram.png)

## Do it has any documentation?
It have all the needed to be documented, thanks to OpenAPI and _swagger.io[⁴]_, after you run the application enter to: http://localhost:5000/api/spec.html#!/spec you should be able to see this:

![API Spec](https://github.com/RafaAguilar/job-dispatcher/raw/master/diagrams/swagger_support.png)

## Where can I interact with a demo?

_It will be ~soon~ someday in a Heroku Test Instance_

## Steps to deploy?

I suggest you to use `virtualenv` to play with it, here is what I did:

```bash
#install python3.5 and virtualenv according with your distribution / OS
#this steps are for a unix-like system

git clone https://github.com/RafaAguilar/job-dispatcher.git

cd job-dispatcher/
virtualenv venv
source venv/bin/activate

pip install -r requirements.txt

#change dispatcher with your PostgreSQL proper data
export APP_SETTINGS="config.DevelopmentConfig" #check config.py to see the options 
export DATABASE_URL="postgresql://dispatcher:dispatcher@localhost/dispatcher"

#python manage.py migrate #this only will be needed when you make changes
                          #and warning, flask_migrate isn't behaving  
                          #if you have any issues read the "KnowN issues" subject.
python manage.py upgrade

#If everything goes well, just type:
python app.py
```

## Known Issues

- _After changing models it won't upgrade DB:_
   - `alembic`, as part of `flask_migrate` doesn't recognize a bunch of _outsider models_, like the custom ones or the ones from `sqlalchemy_utils` for example, so you just need to add the proper updates on the **generated migration**. It also has a problem with `JSON` fields, so you have to manually add `sa.` in the migrations where there is only a `Text()`. This is while they fix this issue :P

[¹]: http://flask-restful.readthedocs.io/en/0.3.5/
[²]: http://flask-sqlalchemy.pocoo.org/2.1/
[³]: https://flask-migrate.readthedocs.io/
[⁴]: http://swagger.io/
