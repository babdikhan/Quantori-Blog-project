**Project Description:** A blog on PostgreSQL deployed using Flask Flamework and SQLAlchemy as ORM with contaneirization in Docker. Features included are CRUD, list of favorites, a REST API for addingg groups, and provided unit tests. 

Prerequisites:
1. Python 3.7 or higher
2. Docker (for containerization)
3. PostgreSQL (installed locally or via Docker)

**How to run locally:**

Install Requirements:
1. Ensure you have the necessary Python packages installed. You can do this by running:
pip install -r requirements.txt
2. Additionally, manually install any missing packages that are not included in the requirements.txt file.

Database Configuration:
1. Make sure your PostgreSQL database is running on your localhost (usually 127.0.0.1) and port 5434 (or the port you’ve configured).
2. Update your Flask app configuration to connect to the database. Modify the following line in your app.py or configuration file:
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/flask_db"
3. Replace {postgres_user}, {postgres_password}, {postgres_host}, and {postgres_port} with your actual database credentials and connection details.
4. Run Database Migrations:
Execute the following command to apply database migrations (assuming you’ve set up Flask-Migrate):
flask db upgrade

Run Your Flask Application:
1. Start your Flask app by running:
python app.py

Running Tests:
1. To run tests, execute the following command in your project directory:
pytest .

6. Access the Admin Panel:
To access the admin panel, navigate to /admin in your web browser.


**Tests:**

Fixtures
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

Blog tests
1. test_create_post(app):
Creates a new post with a predefined title (“title”), body (“body”), and user ID (1).
Commits the changes to the database.
Asserts that True is equal to True, which always passes.
Checks if post creation works as expected.

2. test_update_post(app):
Retrieves an existing post with ID 49 from the database.
Updates the post’s title and body to new values (“title” and “body”).
Commits the changes to the database.
Asserts that True is equal to True.
Verifies if post updating (editing) works correctly.

3. test_delete_post(app):
Deletes the post with ID 49 from the database.
Commits the changes to the database.
Asserts that True is equal to True.
Ensures that post deletion is functioning as expected.

4. test_index_with_valid_data(token):
Sends an authenticated request to the /api/post/ endpoint.
Expects a successful response (status code 200) with a “success” status in the JSON.
Validates that the API endpoint works correctly for authorized users.

5. test_index_without_token(token):
Sends a request to the /api/post/ endpoint without an authorization token.
Expects a response with a “Missing Authorization Header” message.
Verifies that the API handles missing tokens appropriately.

6. test_index_with_invalid_token(token):
Sends a request to the /api/post/ endpoint with an invalid authorization token.
Expects a response with an “Invalid token. Please log in again.” message.
Validates the handling of invalid tokens.

7. test_create_with_valid_data(token):
Sends a POST request to create a new post with valid data (title: “API 1 title”, body: “API 1 Body”).
Expects a successful response (status code 200) with a “success” status in the JSON.
Tests if post creation via the API works correctly.

8. test_create_without_title(token):
Sends a POST request to create a new post without a valid title (using “ti” instead of “title”).
Expects a response with a “Title is required.” message.
Validates that the API enforces title requirements during post creation.

9. test_create_without_body: This test checks whether the system correctly handles creating a post without a body. It does the following:
Sends a POST request to the specified URL with a valid title but missing the “body” field.
Expects a response with the message “Body is required.”

10. test_create_with_empty_body: This test checks whether the system correctly handles creating a post with an empty body. It does the following:
Sends a POST request to the specified URL with a valid title and an empty body.
Expects a response with the message “Body is required.”

11. test_create_with_empty_title: This test checks whether the system correctly handles creating a post with an empty title. It does the following:
Sends a POST request to the specified URL with an empty title and a valid body.
Expects a response with the message “Title is required.”

12. test_update_with_valid_data: This test checks whether updating a post works as expected. It does the following:
Retrieves the list of posts.
Sends a POST request to update the first post’s title and body.
Expects a response with the message “Post updated.”

13. test_update_with_invalid_post_id: This test checks whether updating a post with an invalid post ID fails gracefully. It does the following:
Sends a POST request to update a post with an invalid post ID.
Expects a response indicating that the post was not found.

14. test_update_someone_else_post: This test checks whether editing someone else’s post is prohibited. It does the following:
Attempts to update a post with a hardcoded post ID (63) that may not belong to the user.
Expects a response with the message “Can’t edit someone else’s post.”

15. test_delete_with_valid_data: This test checks whether deleting a post works as expected. It does the following:
Retrieves the list of posts.
Sends a POST request to delete the first post.
Expects a response with the message “Post deleted.”

16. test_delete_with_invalid_token_id: This test checks whether deleting a post with an invalid post ID fails gracefully. It does the following:
Sends a POST request to delete a post with an invalid post ID.
Expects a response indicating that the post was not found.

17. test_favorite_with_valid_data: This test checks whether adding a post to favorites works as expected. It does the following:
Retrieves the list of posts.
Sends a POST request to add the first post to favorites.
Expects a response with the message “Added post to favorites.”

18. test_favorite_with_invalid_post_id: This test checks whether adding a post with an invalid post ID to favorites fails gracefully. It does the following:
Sends a POST request to add a post with an invalid post ID to favorites.
Expects a response indicating that the post was not found.

19. test_index_favorites_with_valid_data: This test checks whether retrieving the list of favorite posts works as expected. It does the following:
Sends a GET request to the favorites endpoint.
Expects a response with the message “List of favorites posts.”

20. test_unfavorite_with_valid_data: This test checks whether removing a post from favorites works as expected. It does the following:
Retrieves the list of favorite posts.
Sends a POST request to remove the first post from favorites.
Expects a response with the message “Removed post from favorites.”

21. test_unfavorite_with_invalid_post_id: This test checks whether removing a post with an invalid post ID from favorites fails gracefully. It does the following:
Sends a POST request to remove a post with an invalid post ID from favorites.
Expects a response indicating that the post was not found.

22. test_index_with_old_token: This test checks whether using an old token results in an appropriate error message. It does the following:
Waits for 6 seconds (simulating an expired token).
Sends a GET request to retrieve posts using the expired token.
Expects a response with the message “Signature expired. Please log in again.”

23. test_index_with_blacklisted_token: This test checks whether using a blacklisted token results in an appropriate error message. It does the following:
Logs out using the token.
Sends a GET request to retrieve posts using the blacklisted token.
Expects a response indicating that the token is blacklisted.



User tests
1. test_create_user: This test checks whether a new user can be created and then deleted successfully. It does the following:
Creates a new user with the name “a” and password “a”.
Adds the user to the database.
Queries the database to retrieve the user with the same name and password.
Asserts that the retrieved user matches the newly created user.
Deletes the user from the database.

2. test_register_with_valid_data: This test checks whether user registration works as expected. It does the following:
Sends a POST request to the specified URL with valid registration data (username, password, and groups).
Expects a successful registration response with the message “Successfully registered. Please Login.”

3. test_delete_of_exiting_user: This test checks whether a user can be successfully deleted. It does the following:
Sends a POST request to the specified URL with the username and password of the user to be deleted.
Expects a successful deletion response with the message “Successfully deleted user.”

4. test_register_with_empty_username: This test checks whether registration fails when an empty username is provided. It does the following:
Sends a POST request with an empty username and a valid password.
Expects a failure response with the message “Username is required.”

5. test_register_with_empty_password: This test checks whether registration fails when an empty password is provided. It does the following:
Sends a POST request with a valid username and an empty password.
Expects a failure response with the message “Password is required.”

6. test_register_without_groups: This test checks whether registration fails when no groups are provided. It does the following:
Sends a POST request with a valid username and password but without specifying any groups.
Expects a failure response with the message “Groups are required. Submit at least an empty list.”

7. test_register_with_no_password: This test checks whether registration fails when the “assword” field (typo) is used instead of “password.” It does the following:
Sends a POST request with a valid username and a misspelled “assword” field.
Expects a failure response with the message “Password is required.”

8. test_login_with_valid_data: This test checks whether user login works as expected. It does the following:
Sends a POST request to the login URL with a valid username and password.
Expects a successful login response with the message “Successfully logged in.”

9. test_logout_with_valid_data: This test checks whether user logout works as expected. It does the following:
Logs in using a valid username and password.
Retrieves the authentication token.
Sends a POST request to the logout URL with the token in the Authorization header.
Expects a successful logout response.

10. test_logout_with_invalid_header: This test checks whether logout fails when an invalid Authorization header is provided. It does the following:
Logs in using a valid username and password.
Retrieves the authentication token.
Sends a POST request to the logout URL with a misspelled “Authorizatioa” header.
Expects a response with the message “Missing Authorization Header.”

11. test_logout_with_invalid_token: This test checks whether logout fails when an invalid token is provided. It does the following:
Logs in using a valid username and password.
Retrieves the authentication token.
Sends a POST request to the logout URL with an incorrect token.
Expects a response indicating an invalid token.

12. test_logout_with_timed_out_token: This test checks whether the system handles a timed-out token correctly during logout. It does the following:
Logs in using a valid username and password.
Retrieves the authentication token.
Waits for 6 seconds (simulating token expiration).
Sends a POST request to the logout URL with the expired token in the Authorization header.
Expects a response with the message “Signature expired. Please log in again.”

13. test_login_with_invalid_username: This test checks whether the system handles an invalid username during login. It does the following:
Sends a POST request to the login URL with an invalid username (“qqw”) and a valid password.
Expects a response with the message “User/Password incorrect. Please try again.”


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
