**Project Description:** A blog on PostgreSQL deployed using Flask Flamework and SQLAlchemy as ORM with contaneirzization in Docker. Features included are CRUD, list of favorites, a REST API for addingg groups, and provided unit tests. 

**How to run locally:**

0. Install requirements from requirements.txt and manually the missing ones, or from requirements_full.txt, but it will install a bunch of not required packages
1. Make sure you have you postgres running on your localhost and port 5434 (In case other port change path
   app.config[
   "SQLALCHEMY_DATABASE_URI"
   ] = "postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/flask_db"
2. Run flask migration (flask db upgrade)
3. Run app.py

To run the tests, run pytest . in the directory

To go to admin panel, got to /admin

**Tests:**

1. token Fixture:
Sends a login request to the app with a predefined username and password.
Retrieves an authentication token.
Tests authenticated endpoints.

2. give_own_post_id Fixture:
Retrieves the ID of a post where the user is the owner (based on the token).
Tests post-related functionality specific to the owner.

3. give_not_own_post_id Fixture:
Retrieves the ID of a post where the user is not the owner.
Tests post-related functionality for non-owners.


MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
