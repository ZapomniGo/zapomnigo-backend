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
---
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
* 418
`{"user_info": 
{"email": user.email,
"user_id": user.user_id,
"username": user.username}}`

### `GET /verify?token=jwt` - verifies a registered user
* `{"message": "Your account has been verified"}, 200`
* `{"message": "user doesn't exist"}, 404`
* `{"message": "Verification link expired."}, 420`
* `{"message": "Invalid verification token signature."}, 401`
* `{"message": "Invalid or missing verification token."}, 499`
* `{"message": "No user_id provided"}, 499`

### `POST /send-email?verification=true` - sends an email to a registered user
If verification=false a forgot-password email will be send
Example body:
```json
{"email": "test@test.com"}
```
Responses:
* 200
```json
{
    "message": "Email send to test@test.com"
}
```
* 422
* 404 
```json
{
    "message": "invalid argument provided"
}
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

---
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

### `GET /organizations/01HG6QGNWTZK2N0TBQCHDEWAJQ/sets`
Responses:
```json
{
    "Sets": [
        {
            "organization": "01HG6QGNWTZK2N0TBQCHDEWAJQ",
            "set_category": "01HJ6DSCG5YG6YQMGFT9PVZJQA",
            "set_description": "naskoebobur",
            "set_id": "01HJM8KH8EW70K977WHDW30ARF",
            "set_modification_date": "2023-12-27 01:50:50.382284",
            "set_name": "TestORG",
            "username": "ivanobreshkov"
        }
    ]
}
```
* `{"message": "Organization with such id doesn't exist"}, 404`
* `{"message": "No sets were found for this organization"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint
---
### `POST /categories` - create a category

Responses:
*`{"message": "Category added to db"}, 200`
* 409 - `{"error": "Key (category_name)=(english) already exists."}`
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
* 409 - `{"error": "Key (category_name)=(biologybratle) already exists."}`
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

---
### `POST /sets` - create a set

Responses:
*`{"message": "Set added to db"}, 200`
* 409 - `"error": "Key (set_category)=(English) is not present in table \"categories\"."`
* 422
* 401, 403, 498, 499 As it is a protected endpoint

Example body
```json
{
    "set_name": "TestORG",
    "set_description": "naskoebobur",
    "set_category": "01HJ6DSCG5YG6YQMGFT9PVZJQA",
    "organization_id": "01HG6QGNWTZK2N0TBQCHDEWAJQ",
    "flashcards": [
        {
            "definition": "capital of bulgaria",
            "term": "sofia"
        },
        {
            "definition": "capital of UK",
            "notes": "testtesttestsetest",
            "term": "london"
        }
    ]
}
```

### `GET /sets?page=1&size=2&sort_by_date=false&ascending=true` - get all sets from the db
/sets could also be used and the default params are 1 and 20 for page and size
true for sort_by_date and false for ascending 
Responses:
* 200
```json
{
    "current_page": 1,
    "last_page": 6,
    "sets": [
        {
            "category_name": "biologybratle",
            "organization_name": null,
            "set_description": "kurvi",
            "set_id": "01HJBKF94QV95TW35F5S7DZQAP",
            "set_modification_date": "2023-12-23 17:07:35.447655",
            "set_name": "TEst",
            "username": "ivanobreshkov"
        },
        {
            "category_name": "biologybratle",
            "organization_name": null,
            "set_description": "kurvi",
            "set_id": "01HJBKF9WTWRYZY2GAMACTC7AN",
            "set_modification_date": "2023-12-23 17:07:36.218534",
            "set_name": "TEst",
            "username": "ivanobreshkov"
        }
    ],
    "total_pages": 6
}
```
* 404
```json
{"message": "No sets were found"}
```
### `GET /users/01HF4S35XAGB1KC52XBCWW8Z5N/sets?page=1&size=20&sort_by_date=false&ascending=true` - get all sets  for a specific user
/users/01HF4S35XAGB1KC52XBCWW8Z5N/sets the default params are 1 and 20 for page and size
true for sort_by_date and false for ascending 

Responses:
* 200
```json
{
    "current_page": 1,
    "last_page": 6,
    "sets": [
        {
            "category_name": "biologybratle",
            "organization_name": null,
            "set_description": "kurvi",
            "set_id": "01HJBKF94QV95TW35F5S7DZQAP",
            "set_modification_date": "2023-12-23 17:07:35.447655",
            "set_name": "TEst",
            "username": "ivanobreshkov"
        },
        {
            "category_name": "biologybratle",
            "organization_name": null,
            "set_description": "kurvi",
            "set_id": "01HJBKF9WTWRYZY2GAMACTC7AN",
            "set_modification_date": "2023-12-23 17:07:36.218534",
            "set_name": "TEst",
            "username": "ivanobreshkov"
        }
    ],
    "total_pages": 6
}
```
* 404

```json
{
    "message": "user doesn't exist"
}
```
or
```json
{
    "message": "No sets were found"
}
```
### `GET /sets/id?page=1&size=1` - get info for specific set
the pagination is for the number of flashcards
/sets/id could also be used and the default params are 1 and 20
Responses:
* 200
```json
{
    "current_page": 1,
    "last_page": 2,
    "set": {
        "category_name": "biologybratle",
        "flashcards": [
            {
                "definition": "capital of Bulgaria",
                "flashcard_id": "01HJM17CGYC6XMCDYZDTDQXCX2",
                "notes": null,
                "term": "sofia"
            }
        ],
        "organization_name": null,
        "set_description": "bobreee",
        "set_id": "01HJM17CGHV66Q9940GAP8AJXK",
        "set_modification_date": "2023-12-26 23:41:52.273972",
        "set_name": "Capitals",
        "username": "ivanobreshkov"
    },
    "total_pages": 2
}
```

* 404
```json
{
    "message": "Set with such id doesn't exist"
}
```

### `PUT /sets/set_id` - edit a set

Responses:
*`{"message": "Set successfully updated"}, 200`
* 422
* 401, 403, 498, 499 As it is a protected endpoint

```json
{"set_name":"ZabraviGo"}
```
This is how to add new flashcards to a current set
```json
{"flashcards": [
        {
            "definition": "capital of Bulgaria",
            "flashcard_id": "01HJECQHJTJSWJZ852364SJ51Z",
            "term": "sofia"
        },
        {
            "definition": "capital of UK",
            "flashcard_id": "01HJECRT8FTKNMVVBR7DEGKBGG",
            "notes": "testtesttestsetest",
            "term": "london"
        }
    ]}
```
### `DELETE /set/set_id` - delete a set and all flashcards related to it
Responses:
*`{"message": "Set successfully deleted"}, 200`
*`{"message": "Set with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint
---

### POST /sets/set_id/copy - create a copy set of the passed one in the db
Responses:
* `{"set_id": 01HJBKFAJQMMAS0ZKWC83VV1AY}, 200`
* `{"message": "set with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint

### POST /sets/set_id/study - get flashcards with confidence levels
Responses:
* 200
```json
    "flashcards": [
        {
            "confidence": null,
            "definition": "capital of bulgaria",
            "flashcard_id": "01HJPF4S35MCRP12BT8247J1KN",
            "term": "sofia"
        },
        {
            "confidence": null,
            "definition": "capital of UK",
            "flashcard_id": "01HJPF4S35XABGJMW8W6E6BX4M",
            "term": "london"
        }]
```
* `{"message": "set with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint

### `GET /flashcards/flashcard_id` - get info for a given flashcard

Responses:
 * 200 - 
```json
{
    "flashcard": {
        "definition": "capital of bulgaria",
        "flashcard_id": "01HJECQHJTJSWJZ852364SJ51Z",
        "notes": null,
        "set_id": "01HJBKFAJQMMAS0ZKWC83VV1AY",
        "term": "sofia"
    }
}
```
* 404 - 
```json
{
    "message": "flashcard with such id doesn't exist"
}
```

### `DELETE /flashcard/flashcard_id` - deletes a flashcard
Responses:
* `{"message": "Flashcard successfully deleted"}, 200`
* `{"message": "Flashcard with such id doesn't exist"}, 404`
* `{"message": "Set with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint

### `PUT /flashcard/flashcard_id` - updates a flashcard
Responses:
* `{"message": "Flashcard successfully updated"}, 200`
* `{"message": "Flashcard with such id doesn't exist"}, 404`
* `{"message": "Set with such id doesn't exist"}, 404`
* 401, 403, 498, 499 As it is a protected endpoint
Example body
```json
{
    "term": "london",
    "definition": "capital of UK"
}
```

### `PUT /flashcard/flashcard_id/study` - updates a flashcards confidence
Responses:
* `{"message": "Confidence level of flashcard updated!"}, 200`
* `{"message": "Flashcard with such id doesn't exist"}, 404`
* 409
```json
{
    "error": "Key (user_id)=(pomo6t) is not present in table \"users\"."
}
```
* 401, 403, 498, 499 As it is a protected endpoint
Example body
```json
{
    "correctness": 0,
    "username": "ivan",
    "user_id": "01HJSJSXHNYG58SQJJPYB84Q5Z"
}
```
