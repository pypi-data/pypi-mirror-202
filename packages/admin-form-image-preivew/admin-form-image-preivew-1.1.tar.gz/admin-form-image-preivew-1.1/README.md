Test Django Package

See the sample app for usage/code


**Instructions to install/use**
1. `git clone https://github.com/humblesami/admin_form_image_preivew.git`
2. `cd admin_form_image_preivew/sample_usage`
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
http://127.0.0.1:8000/admin/admin_image_preview/model1/add/

7. Add image to check preview

8. See docs/make_pip.txt to make/build/test and upload your own pip package

