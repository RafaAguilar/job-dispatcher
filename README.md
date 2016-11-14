# Flask Job Dispatcher Simulator

This is a small project to learn how to use Flask with two new libraries I just found:

- `flask_restful`[¹]
- `flask_sqlalchemy`[²]

The main goal is to build a generic and reusable task synchronizer that allows to manage jobs, tasks, storages, clients, and related stuff.
 
In the first uploaded version (0.1) will have the most abstract concepts, almost not usable in a real scenario, but my (could be our goal) to reach V1.0 is to simulate a Coffee spending machine, that have flavors, cups, time to serve, a _witdrawal window_ and such only configuring the application, through API, without specifying (hopefully) new _Coffee_ classes.
 
##Which technologies we will use?



[¹]: http://flask-restful.readthedocs.io/en/0.3.5/
[²]: http://flask-sqlalchemy.pocoo.org/2.1/