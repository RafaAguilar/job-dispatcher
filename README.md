# Flask Job Dispatcher Simulator

This is a small project to learn how to use Flask with two new libraries I just found:

- `flask_restful`[¹]
- `flask_sqlalchemy`[²]
- `flask_migrate`[³]

The main goal is to build a generic and reusable task synchronizer that allows to manage jobs, tasks, storages, clients, and related stuff.
 
In the first uploaded version (0.1) will have the most abstract concepts, almost not usable in a real scenario, but my (could be our goal) to reach V1.0 is to simulate a Coffee spending machine, that have flavors, cups, time to serve, a _witdrawal window_ and such only configuring the application, through API, without specifying (hopefully) new _Coffee_ classes.
 
##Which technologies will We use?
_It includes much more techonlogies, but these are the interest one_
![Technoglies of interest](https://github.com/RafaAguilar/job-dispatcher/raw/master/diagrams/Techs%20Used.png)

##Which is the proposed Workflow?
_note: It will need another diagrams for sure._
![Proposed Workflow](https://github.com/RafaAguilar/job-dispatcher/raw/master/diagrams/Job%20Dispatcher%20Workflow.png)

## Do you have any Classes Diagram?
_note: The Classes Diagram still lacks of labour, it is too changing now, and actually doesn't correspond with code, in a 100%, but almost._
![Classes Diagram](https://github.com/RafaAguilar/job-dispatcher/raw/master/diagrams/ClassesDiagram.png)

##Where I can interact with a demo?

_It will be soon in a Heroku Test Instance_

##Steps to deploy?

I suggest you to use `virtualenv` to play with it, here is what I did:

```bash
#install python3.5 and virtualenv according with your distribution / OS
#this steps are for a unix-like system

git clone https://github.com/RafaAguilar/job-dispatcher.git

cd job-dispatcher/
virtualenv venv
source venv/bin/activate

#change dispatcher with your PostgreSQL proper data
export APP_SETTINGS="config.DevelopmentConfig" #check config.py to see the options 
export DATABASE_URL="postgresql://dispatcher:dispatcher@localhost/dispatcher"

python manage.py db init
#python manage.py migrate #this only will be needed when you make changes
                          #and warning, flask_migrate isn't behaving really well 
                          #if you have any issues read the "Know issues" subject.
python manage.py upgrade

#If everything goes well, just type:
python app.py
```


[¹]: http://flask-restful.readthedocs.io/en/0.3.5/
[²]: http://flask-sqlalchemy.pocoo.org/2.1/
[³]: https://flask-migrate.readthedocs.io/