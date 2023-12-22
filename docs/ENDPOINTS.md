# Endpoints:
### Base url `localhost:5000/v1`
### Common Responses:
* 498 Status code`{"message": "Auth token expired."}`
* 499 Status code `{"message": "Invalid or missing auth token."}`
* 401 Status code not on `/login` -> `{"message": "Invalid token signature."}`
* 403 Status code `{"message": "Admin privileges required."}`
* 422 Status code: Validation errors when parsing the json body. The keys are the fields passed in the json body.

`{"validation errors": list of dictionaries}`
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
            "organization_name": "String should have at least 2 characters"
        },
        {
            "test_field": "Extra inputs are not permitted"
        }
    ]
}
```
### `GET /health` - could be used for e heartbeat service
Responses: `{"status": healthy}, 200`

### `POST /register` - Used to register a new user

Responses:
* `{"message": "user added to db"}, 200`
* `{"error": "Key (username)=(test_username) already exists."}, 409` - this is valid for `email` as well
* 422
* `{"message": "Organization with such id doesn't exist"}, 404`

Example body:
```json
{
"name": "test",
"email": "test@test.com",
"username": "testusername",
"password": "T3stpswd*",
"organization": "01HG6QGNWTZK2N0TBQCHDEWAJQ",
"gender": "M",
"age": 18,
"privacy_policy": true,
"terms_and_conditions": false,
"marketing_consent": false
}
```
### `POST /subscription-models` - used to add a new subscription model to the DB

Responses: `200`, `422`, `409`, `403`. The same as the previous endpoint.

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
* 498
* 499
* 401

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
* 409 - `{"error": "Key (organization_domain)=(aubg.edu) already exists."}` or\
`{"error": "Key (organization_name)=(AUBGbrad) already exists."}`
* 422
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

### `POST /categories` - create a category

Responses:
*`{"message": "Category added to db"}, 200`
*`{"error": "Key (category_name)=(english) already exists."}`
* 422
* 401, 403, 498, 499 As it is a protected endpoint

Example body: The value is saved as lower case in the db
```json
{"category_name":"English"}
```

### `GET /categories` - get all categories from the db

Responses:
* 200
```json
    "categories": [
        {
            "category_id": "01HGGQ54X84PP3S0CZWB2HED9T",
            "category_name": "english"
        }
    ]
```
* 404
```json
{"message": "No categories were found"}
```

### `GET /category/id` - get info for specific category

Responses:
* 200
```json
"category": { "category_id": "01HGTTQTZPCVVC3XFGZH9VMMTB", 
            "category_name": "english" }
```

* 404
```json
{
    "message": "Category with such id doesn't exist"
}
```

### `PUT /categories/category_id` - edit a category

Responses:
*`{"message": "Category successfully updated"}, 200`
*`{"error": "Key (category_name)=(biologybratle) already exists."}`
* 422
* 401, 403, 498, 499 As it is a protected endpoint

Example body: The value is saved as lower case in the db
```json
{"category_name":"English"}
```

### `DELETE /categories/category_id` - delete a category
Responses:
*`{"message": "Category successfully deleted"}, 200`
*`{"message": "Category with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint