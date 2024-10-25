**Insallation**

1. `pip install djform_navigation`
2. Add `form_navigation` in installed apps in `settings.py` of django project
   

    INSTALLED_APPS = [
       'form_navigation',
       # ...
    ]
(at the top)

**Description**

It adds Next and Prev buttons to the top of each edit form of django admin site
for all the models of all the apps in your project, without need to do anything
except installing the module with pip plus adding to the top of INSTALLED_APPS in settings.py

**Instructions to run the sample usage**

1. `git clone https://github.com/humblesami/djform_navigation.git`
2. `cd djform_navigation/sample_usage`
3. `pip install -r requirements.txt`

*Not required* but if you want to reset the database, you can do this
3.1. `python manage.py initsql.py`

4. `python manage.py runsever`

5. Open following url in your browser and login with given username and password
   http://127.0.0.1:8000/admin/login/?next=/admin/login
   username
   sa
   password
   123

6. Go to
   http://127.0.0.1:8000/admin/form_navigation/model1/add/

7. Add image to check preview

**Make you own pip package**
See https://github.com/humblesami/djform_navigation/blob/master/docs/make_pip.md to make/build/test and upload
`your own pip package`
