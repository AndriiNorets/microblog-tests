# Tests Documentation

## End to End tests

### ```test_user1_message_user2.py```
Verify the complete user flow of sending and receiving a private message
### ```test_profile_editing.py```
Verify that a user can successfully update their profile information

## Integration tests

### ```test_auth_routes.py```
-   `test_registration_page_loads`: Checks that the registration page loads.
-   `test_successful_registration`: Verifies a new user can register with valid data.
-   `test_registration_with_duplicate_username`: Ensures registration fails if the username is taken.
-   `test_registration_with_duplicate_email`: Ensures registration fails if the email is in use.
-   `test_registration_with_password_mismatch`: Checks that passwords must match.
-   `test_login_page_loads`: Checks that the login page loads.
-   `test_successful_login`: Verifies a registered user can log in.
-   `test_login_with_invalid_username`: Ensures login fails for a non-existent user.
-   `test_login_with_wrong_password`: Ensures login fails for an incorrect password.
-   `test_user_logout`: Verifies that a logged-in user can successfully log out.

### `test_messaging.py`
-   `test_inbox_shows_received_messages`: Verify users inbox displays received messages.
-   `test_inbox_only_shows_received_not_sent`: Verify the inbox filters out sent messages.


### `test_post_routes.py`
-   `test_create_post_success`: Verifies a logged-in user can create a new post.
-   `test_create_post_empty_body_error`: Ensures an empty post cannot be submitted.
-   `test_timeline_shows_followed_user_posts`: Checks that the main timeline includes posts from followed users.

### `test_user_endpoint.py`
-   `test_users_endpoint2`: Verifies the API can return a list of all users.
-   `test_get_user2`: Verifies the API can return data for a single user.
-   `test_api_create_user`: Checks that a new user can be created via a `POST` request.
-   `test_api_create_user_duplicate_email`: Ensure the API returns an error for a duplicate email.

### `test_user_profile.py`
-   `test_view_own_profile`: Checks that a user sees the "Edit your profile" link on their own profile.
-   `test_edit_profile_success`: Verifies a user can update their profile information.
-   `test_follow_and_unfollow_user`: Tests the complete cycle of following and then unfollowing.
-   `test_cannot_follow_self`: Ensures a user is prevented from following their own account.

## Unit tests

### `test_models.py`
-   `test_password_hashing`: Checks that passwords are correctly hashed.
-   `test_password_is_not_plaintext`: Verifies passwords are not stored in plain text.
-   `test_avatar_generation`: Verifies the generation of Gravatar URLs.
-   `test_user_repr`: Checks the string representation of the User object.
-   `test_post_repr`: Checks the string representation of the Post object.

### `test_forms.py`
-   `test_login_form_rejects_empty_fields`: Ensures the login form requires input.
-   `test_registration_form_rejects_mismatched_passwords`: Checks password confirmation validation.
-   `test_edit_profile_form_rejects_long_about_me`: Verifies the character limit for the 'about me' field.
-   `test_post_form_rejects_empty_post`: Ensures the post form requires content.

### `test_utils.py`
-   `test_send_email_function_creates_correct_message`: Verifies email content construction using mocks.
-   `test_translate_function_handles_no_key_error`: Checks graceful error handling when a translation API key is missing.