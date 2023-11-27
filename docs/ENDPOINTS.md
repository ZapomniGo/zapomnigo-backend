# Endpoints:
### Base url `localhost:5000/v1`

### `GET /health` - could be used for e heartbeat service
Responses: `{"status": healthy}, 200`

### `POST /register` - Used to register a new user

Responses:
* `{"message": "user added to db"}, 200`
* `{"error": "Key (username)=(test_username) already exists."}, 409` - this is valid for email as well
* `{"validation errors": list of dictionaries}, 422`
```json
{
    "validation errors": [
        {
            "password": "String should have at least 8 characters"
        },
        {
            "gender": "Input should be 'M', 'F' or 'O'"
        },
        {
            "subscription_model": "Input should be '6 months', '1 month' or '1 year'"
        }
    ]
}
```

Example body:
```json
{
"name": "test",
"email": "test@test.com",
"username": "testusername",
"password": "T3stpswd*",
"subscription_model":"6 months",
"gender": "M",
"age": 18,
"privacy_policy": true,
"terms_and_conditions": false,
"marketing_consent": false
}
```
### `POST /subscription-models` - used to add a new subscription model to the DB

Responses: `200`, `422`, `409`. The same as the previous endpoint.
Also we have `{"message": "Admin privileges required."}, 403` 

Example body: 
```json
{"subscription_model":"6 months"}
```

### `POST /login` Used to login a user

Responses:
* `{"message": "invalid password"}, 401`

2 cookies in the form of JWT:
* `access_token`: SameSite="Strict", Secure=True, the decoded format is 
```json
{
  "username": "test4username",
  "admin": false,
  "exp": 1701008381
}
```
* `refresh_token`: SameSite="Strict", Secure=True, HttpOnly=True

Example body:
```json
{"email_or_username":"test4@test.com","password": "T3stpswd"}
```

### `POST /logout` logs out the user

Responses:
`{"message": "user logged out"}, 200` and unsets the cookies

### `POST /refresh` refresh the two JWT tokens

Responses:
* `{"message": "Token refreshed"}, 200` and the two new JWT tokens as cookies
* `{"message": "Auth token expired."}, 498`
* `{"message": "Invalid or missing auth token."}, 499`
* `{"message": "Invalid token signature."}, 401`

### `GET /organizations` get a list of all organizations

Responses:
* 200 Status code
```json
    "organizations": [
        {
            "organization_domain": "aubg.edu",
            "organization_id": "01HG6QGNWTZK2N0TBQCHDEWAJQ",
            "organization_name": "AUBG",
            "subscription_model_id": "01HG6QGEK1GEYDSQ34HKS637AR"
        }
    ]
```
* `{"message": "No organizations were found"}, 404`

### `GET /organization/id` get info for a specific organization

Responses 
* 200
```json
    "organization": {
        "organization_domain": "aubg.edu",
        "organization_id": "01HG6QGNWTZK2N0TBQCHDEWAJQ",
        "organization_name": "AUBG",
        "subscription_model_id": "01HG6QGEK1GEYDSQ34HKS637AR"
    }
```
* `{"message": "Organization with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint

### `DELETE /organization/id` - deletes an organization by id

Responses:
* `{"message": "Organization successfully deleted"}, 200`
* `{"message": "Organization with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint

### `POST /organizations` - create an organization

Responses:
* `{"message": "Organization added to db"}, 200`
* 422, 409
* 401, 403, 498, 499 As it is a protected endpoint

Example body:

```json
{"organization_name": "AUBG",
"organization_domain": "aubg.edu",
"subscription_model": "Free trial"}
```

### `PUT /organization/id` - edit organization info

Responses:
* `{"message": "Organization successfully updated"}, 200`
* `{"message": "Organization with such id doesn't exist"}, 404`
* 422
* 401, 403, 498, 499 As it is a protected endpoint

Example body: (You pass only the fields you wand to change)
```json
{"organization_name": "Nasko"}
```