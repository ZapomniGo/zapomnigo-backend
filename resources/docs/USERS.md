1. `POST /register`

   This endpoint is used to register a new user.

   Example request body:
   ```json
   {
       "name": "John Doe",
       "username": "johndoe",
       "email": "johndoe@example.com",
       "password": "Password123",
       "age": 30,
       "gender": "M",
       "privacy_policy": true,
       "terms_and_conditions": true,
       "marketing_consent": false
   }
   ```
   Responses:
    - 200: `{"message": "user added to db"}`
    - 422: `{"validation errors": {...}}`
    - 409: `{"error": "unique constraint violation message"}`

2. `POST /login`

   This endpoint is used to login a user.

   Example request body:
   ```json
   {
       "email_or_username": "johndoe",
       "password": "Password123"
   }
   ```
   Responses:
    - 200: `{"message": "user logged in", "access_token": "access_token", "refresh_token": "refresh_token"}`
    - 401: `{"message": "invalid password"}`
    - 404: `{"message": "user doesn't exist"}`
    - 401: `{"message": "invalid password"}`
    - 418: `{"user_info": {"email": user.email,"user_id": user.user_id,"username": user.username}}` - if user is not verified

3. `POST /logout`

   This endpoint is used to logout a user.

   Responses:
    - 200: `{"message": "user logged out"}`

4. `POST /refresh`

   This endpoint is used to refresh the JWT token.

   Responses:
    - 200: `{'message': 'Token refreshed', 'access_token': 'new_access_token', "refresh_token": "new_refresh_token"}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

5. `POST /forgot-password`

   This endpoint is used to reset the password.

   Example request body:
   ```json
   {
       "token": "reset_token",
       "new_password": "NewPassword123"
   }
   ```
   Responses:
    - 200: `{"message": "Your password has been changed"}`
    - 422: `{"validation errors": {...}}`
    - 404: `{"message": "user doesn't exist"}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

6. `PUT /users/<user_id>`

   This endpoint is used to edit a user.

   Example request body:
   ```json
   {
       "name": "John Doe",
       "username": "johndoe",
       "email": "johndoe@example.com",
       "password": "Password123",
       "new_password": "NewPassword123",
       "age": 30,
       "gender": "M",
       "organization": "org123",
       "privacy_policy": true,
       "terms_and_conditions": true,
       "marketing_consent": false
   }
   ```
   Responses:
    - 200: `{"message": "user updated"}`
    - 422: `{"validation errors": {...}}`
    - 409: `{"error": "unique constraint violation message"}`
    - 498: `{"message": "Auth token expired."}`
    - 404: `{"message": "user doesn't exist"}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`
    - 403: `{"message": "Admin privileges required."}`

7. `DELETE /users/<user_id>`

   This endpoint is used to delete a user.

   Responses:
    - 200: `{"message": "user deleted"}`
    - 404: `{"message": "user doesn't exist"}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`
    - 403: `{"message": "Admin privileges required."}`


8. `GET /users/<user_id>`

   This endpoint is used to export user data.

   Responses:
    - 200: `{"user_info": {...}}`
    - 404: `{"message": "user doesn't exist"}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`
    - 403: `{"message": "Admin privileges required."}`

