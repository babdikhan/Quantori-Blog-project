# How to run locally:

0. Install requirements from requirements.txt and manually the missing ones, or from requirements_full.txt, but it will install a bunch of not required packages
1. Make sure you have you postgres running on your localhost and port 5434 (In case other port change path
   app.config[
   "SQLALCHEMY_DATABASE_URI"
   ] = "postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/flask_db"
2. Run flask migration (flask db upgrade)
3. Run app.py

To run the tests, run pytest . in the directory

To go to admin panel, got to /admin
