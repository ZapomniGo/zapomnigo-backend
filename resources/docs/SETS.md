1. `GET /sets`

   This endpoint is used to get all sets. They are ordered first by verified status (true) and then by creation date.

* query parameters:

    * page (int): The page number to retrieve (default is 1).
    * size (int): The number of sets per page (default is 20).
    * category_id (str) If passed shows all sets with the given category,
    * subcategory_id (str) If passed shows all sets with the given subcategory,
    * user_id (str): If provided, fetch sets associated with the specified user (default is an empty string).
    * folder_id (str): If provided, fetch sets in the given folder (default is an empty string).
    * sort_by_date (bool): If True (default), the sets are ordered by creation date.
    * ascending (bool): If True, the sets are ordered in ascending order, else in descending order.
    * search_terms (str): If provided, fetch sets that match the search terms (default is None).
    * exclude_user_sets (bool): If True, exclude sets created by the logged-in user (default is False).
  
    * if sort_by_date=true&ascending=false - Order items by creation date (from last to first created)
    * if sort_by_date=true&ascending=true - Order items by creation date (from first to last created)
    * if sort_by_date=false&ascending=true - Order items by alphabetical order (from A-Z)
    * if sort_by_date=false&ascending=false - Order items by alphabetical order (from Z-A)

  Responses:
    - 200:

```json
    {
  "current_page": 1,
  "sets": [
    {
      "category_name": null,
      "set_description": "asd",
      "set_id": "01HPKSRZVCVXP2S1C5C23G5X7H",
      "set_modification_date": "2024-02-14 12:34:27.820104",
      "set_name": "math test",
      "subcategory_name": null,
      "username": "zapomnigo",
      "verified": true
    }
  ],
  "total_items": 239,
  "total_pages": 239
}
```

- 404: `{"message": "No sets found"}`

2. `GET /sets/<set_id>`

   This endpoint is used to get a specific set and the flashcards in it.
    * query parameters:

    * page (int): The page number to retrieve (default is 1).
    * size (int): The number of flashcards per page (default is 20).
    * sort_by_date (bool): If True (default), the flashcards are ordered by creation date.
    * ascending (bool): If True, the flashcards are ordered in ascending order, else in descending order.

    * if sort_by_date=true&ascending=false - Order items by creation date (from last to first created)
    * if sort_by_date=true&ascending=true - Order items by creation date (from first to last created)
    * if sort_by_date=false&ascending=true - Order items by alphabetical order (from A-Z)
    * if sort_by_date=false&ascending=false - Order items by alphabetical order (from Z-A)

   Responses:
    - 200:

```json
{
  "current_page": 1,
  "set": {
    "category_name": null,
    "flashcards": [
      {
        "definition": "<p>0</p>",
        "flashcard_creation_time": "2024-02-14 12:34:27.854092",
        "flashcard_id": "01HPKSRZWEJKTNT2TQPC0GD6C5",
        "notes": null,
        "term": "<p>5-5</p>"
      },
      {
        "definition": "<p>10</p>",
        "flashcard_creation_time": "2024-02-14 12:34:27.853880",
        "flashcard_id": "01HPKSRZWD36RSAQD078RZTA9P",
        "notes": null,
        "term": "<p>5+5</p>"
      },
      {
        "definition": "<p>1</p>",
        "flashcard_creation_time": "2024-02-14 12:34:27.853734",
        "flashcard_id": "01HPKSRZWD45VMBC4CVJSV2MAP",
        "notes": null,
        "term": "<p>2-1</p>"
      },
      {
        "definition": "<p>3</p>",
        "flashcard_creation_time": "2024-02-14 12:34:27.853486",
        "flashcard_id": "01HPKSRZWDHT83ZFF7P1B18T4W",
        "notes": null,
        "term": "<p>1+2</p>"
      }
    ],
    "set_description": "asd",
    "set_id": "01HPKSRZVCVXP2S1C5C23G5X7H",
    "set_modification_date": "2024-02-14 12:34:27.820104",
    "set_name": "math test",
    "subcategory_name": null,
    "username": "zapomnigo",
    "verified": true
  },
  "total_items": 4,
  "total_pages": 1
}
```

- 404: `{"message": "Set doesn't exist"}`

3. `POST /sets`

   This endpoint is used to create a new set.

* query params:
* folder_id (str): If provided, the set is added to the given folder.

  Example request body:
   ```json
   {
       "set_name": "New Set",
       "set_description": "Description of the new set",
       "set_category": "category_id",
       "set_subcategory": "subcategory_id",
       "flashcards": [
           {
               "term": "Term 1",
               "definition": "Definition 1"
           },
           {
               "term": "Term 2",
               "definition": "Definition 2"           }
       ]
   }
   ```
  Responses:
    - 200: `{"set_id": "id"}`
    - 422: `{"validation errors": {...}}`
    - 400: `{"message": "Cannot create more than 2000 flashcards per set"}`
    - 409: `{"error": "Key (user_id)=(test) is not present in table \"users\"."}`
      or `{"error": "Key (category_id)=(test) is not present in table \"categories\"."}`
      or `{"error": "Key (subcategory_id)=(test) is not present in table \"subcategories\"."} or {"error": "Key (folder_id)=(test) is not present in table \"folders\"."}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`


4. `PUT /sets/<set_id>`

   This endpoint is used to update a specific set.

* query params:
* folder_id (str): If provided, the set is added to the given folder.

  Example request body:
   ```json
   {
       "set_name": "Updated Set",
       "set_description": "Updated description of the set",
       "set_category": "category_id",
       "set_subcategory": "subcategory_id",
       "flashcards": [
           {
               "term": "Updated Term 1",
               "definition": "Updated Definition 1",
               "notes": "Updated Notes 1"
           },
           {
               "term": "Updated Term 2",
               "definition": "Updated Definition 2",
               "notes": "Updated Notes 2"
           }
       ]
   }
   ```
  Responses:
    - 200: `{"message": "set successfully updated"}`
    - 422: `{"validation errors": {...}}`
    - 404: `{"message": "set with such id doesn't exist"}`
    - 409: `{"error": "Key (user_id)=(test) is not present in table \"users\"."}`
      or `{"error": "Key (category_id)=(test) is not present in table \"categories\"."}`
      or `{"error": "Key (subcategory_id)=(test) is not present in table \"subcategories\"."} or {"error": "Key (folder_id)=(test) is not present in table \"folders\"."}`
    - 403: `{"message": "Admin privileges required."}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

5. `DELETE /sets/<set_id>`

   This endpoint is used to delete a specific set.

   Responses:
    - 200: `"message": "Set successfully deleted"}`
    - 404: `{"message": "set with such id doesn't exist"}`
    - 403: `{"message": "Admin privileges required."}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

6. `GET /users/<user_id>/sets`

   This endpoint is used to get all sets for a specific user.

    * query parameters:

    * page (int): The page number to retrieve (default is 1).
    * size (int): The number of sets per page (default is 20).
    * category_id (str) If passed shows all sets with the given category,
    * subcategory_id (str) If passed shows all sets with the given subcategory,
    * sort_by_date (bool): If True (default), the sets are ordered by creation date.
    * ascending (bool): If True, the sets are ordered in ascending order, else in descending order.
    * search_terms (str): If provided, fetch sets that match the search terms (default is None).

    * if sort_by_date=true&ascending=false - Order items by creation date (from last to first created)
    * if sort_by_date=true&ascending=true - Order items by creation date (from first to last created)
    * if sort_by_date=false&ascending=true - Order items by alphabetical order (from A-Z)
    * if sort_by_date=false&ascending=false - Order items by alphabetical order (from Z-A)

   Responses:
    - 200:

```json
    {
  "current_page": 1,
  "sets": [
    {
      "category_name": null,
      "set_description": "asd",
      "set_id": "01HPKSRZVCVXP2S1C5C23G5X7H",
      "set_modification_date": "2024-02-14 12:34:27.820104",
      "set_name": "math test",
      "subcategory_name": null,
      "username": "zapomnigo",
      "verified": true
    }
  ],
  "total_items": 239,
  "total_pages": 239
}
```

- 404: `{"message": "user doesn't exist"}, 404`

7. `POST /sets/<set_id>/copy`

   This endpoint is used to copy a specific set.

   Responses:
    - 200: `{"set_id": "id"}`
    - 404: `{"message": "set with such id doesn't exist"}`

8. `GET /sets/<set_id>/study`

   This endpoint is used to study a specific set.

    * query parameters:

    * page (int): The page number to retrieve (default is 1).
    * size (int): The number of sets per page (default is 20).
    * sort_by_date (bool): If True (default), the sets are ordered by creation date.
    * ascending (bool): If True, the sets are ordered in ascending order, else in descending order.

    * if sort_by_date=true&ascending=false - Order items by creation date (from last to first created)
    * if sort_by_date=true&ascending=true - Order items by creation date (from first to last created)
    * if sort_by_date=false&ascending=true - Order items by alphabetical order (from A-Z)
    * if sort_by_date=false&ascending=false - Order items by alphabetical order (from Z-A)

Responses:

- 200

```json
{
  "current_page": 1,
  "flashcards": [
    {
      "confidence": null,
      "definition": "<p>0</p>",
      "flashcard_id": "01HPKSRZWEJKTNT2TQPC0GD6C5",
      "term": "<p>5-5</p>"
    },
    {
      "confidence": null,
      "definition": "<p>10</p>",
      "flashcard_id": "01HPKSRZWD36RSAQD078RZTA9P",
      "term": "<p>5+5</p>"
    },
    {
      "confidence": null,
      "definition": "<p>1</p>",
      "flashcard_id": "01HPKSRZWD45VMBC4CVJSV2MAP",
      "term": "<p>2-1</p>"
    },
    {
      "confidence": null,
      "definition": "<p>3</p>",
      "flashcard_id": "01HPKSRZWDHT83ZFF7P1B18T4W",
      "term": "<p>1+2</p>"
    }
  ],
  "total_items": 4,
  "total_pages": 1
}
```

- 404: `{"message": "set with such id doesn't exist"}`


9. `POST /sets/<set_id>/study`

   This endpoint is used to create a studied set.

   Responses:
    - 200: `{"message": "studied set successfully created"}`
    - 404: `{"message": "set with such id doesn't exist"}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

10. `POST /sets/<set_id>/report`

    This endpoint is used to report a specific set.
    Example request body:

```json
    {
  "reason": "reason"
}

```

Responses:

- 200: `{"message": "Report sent successfully"}`
- 422: `{"validation errors": {...}}`
- 404: `{"message": "set with such id doesn't exist"}`
- 498: `{"message": "Auth token expired."}`
- 401: `{"message": "Invalid token signature."}`
- 499: `{"message": "Invalid or missing auth token."}`


11. `POST /sets/<set_id>/verify`

    This endpoint is used to change the verified status of a specific set.

    Responses:
    - 200: `{"message": "set verified status changed successfully", "set": {...}}`
    - 404: `{"message": "set with such id doesn't exist"}`
    - 403: `{"message": "Admin privileges required."}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

12. `POST /sets/<set_id>/folders/<folder_id>`

    This endpoint is used to add a specific set to a folder.

    Responses:
    - 200: `{"message": "set successfully added to folder"}`
    - 404: `{"message": "set with such id doesn't exist"}` or `{"message": "folder with such id doesn't exist"}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

