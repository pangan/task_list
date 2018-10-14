Task List
=========

By Amir Mofakhar <amir@mofakhar.info>

Description
-----------

  1. It is possible to create a new task by clicking "Create" from top menu.
  2. Created task will be assigned to the user automatically.
  3. Each user can delete/edit only his/her own tasks and can view detail of
     other's tasks.
  4. It is possible to move the tasts (changing the status) by left/right arrows
     in each task box. only owner of the task can do that.
  5. By moving a task from ToDo to Doing column, a timestamp is written automatically.
     It shows the time user has started to work on that task.
  6. By moving the task from Doing to Done column, a timestamp is written automatically.
     It shows the time user has completed the task. 
  7. It is possible to filter tasks by pressing Show All/My tasks
  8. It is possible to filter (turn off) each column by clicking on its header.
  9. Click on a task title to view, edit or delete it.     


Installation
------------

1. Make a Python 3.6 virtual environment and active it:

       $: virtualenv .venv
       $: source .venv/bin/activate

2. Install the requirements:

       $: pip install -r requirements.txt
       
       
Running
-------

Use the below command to run the server:

       $: python manage.py runserver
       
Use below url to access it:

       http://localhost:8080/
        
To add a new user use below address:

       http://localhost:8080/admin
                 

Unit tests
----------

 1. collect the static files:
 
        $: python manage.py collectstatic
        
 2. run tests:
 
        $: python manage.py test


Deployment
----------

It is deployed automatically on Openshift.

public address : http://tasklist.mofakhar.info


