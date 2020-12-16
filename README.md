<h1>CRM system</h1>

<h3>This is the new version of crm system, which was moved from dmc_project</h3>
The first commit starts from commit `fb0f0fe907eded69952fc4683de79f77ed83afb2` in `dmc_project`


<b>If you do not have venv, complete next steps</b>: 
1. `python -m venv venv`. install it in crm_system root directory

If you are on Linux/Mac: 
2. `source venv/bin/activate`

Windows:
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt`

Commands to run for <b>crm</b>: 
1. `cd crm_system`. Ensure that file manage.py is in your current dir.
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py populate`

You are ready to work
To start server run: 
`python manage.py runserver`


Run test contractors mode: 
1. `python manage.py contractors`