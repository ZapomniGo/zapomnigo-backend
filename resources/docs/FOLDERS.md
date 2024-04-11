1. `GET /folders`

   This endpoint is used to get all folders.

* query parameters:

    * page (int): The page number to retrieve (default is 1).
    * size (int): The number of folders per page (default is 20).
    * user_id (str): If provided, fetch folders associated with the specified user (default is an empty string).
    * sort_by_date (bool): If True (default), the folders are ordered by creation date.
    * ascending (bool): If True, the folders are ordered in ascending order, else in descending order.
    * search_terms (str): If provided, fetch folders that match the search terms (default is None).

    * if sort_by_date=true&ascending=false - Order items by creation date (from last to first created)
    * if sort_by_date=true&ascending=true - Order items by creation date (from first to last created)
    * if sort_by_date=false&ascending=true - Order items by alphabetical order (from A-Z)
    * if sort_by_date=false&ascending=false - Order items by alphabetical order (from Z-A)

  Responses:
    - 200:

```json
{
  "current_page": 1,
  "folders": [
    {
      "category_name": "Биология",
      "folder_description": "тест ",
      "folder_id": "01HPHM2PPHTW6YHVQKGEN2HA8A",
      "folder_modification_date": "2024-02-13 16:16:25.809227",
      "folder_title": "Биология 12 клас",
      "subcategory_name": "7. клас",
      "username": "ivanobreshkov",
      "verified": true
    }
  ],
  "total_items": 41,
  "total_pages": 41
}
```

- 404: `{"message": "No folders found"}`

2. `GET /folders/<folder_id>`

   This endpoint is used to get a specific folder and the sets in it.

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
    - 200:

```json
{
    "current_page": 1,
    "folder": {
        "category_name": "Биология",
        "folder_description": "тест ",
        "folder_id": "01HPHM2PPHTW6YHVQKGEN2HA8A",
        "folder_modification_date": "2024-02-13 16:16:25.809227",
        "folder_title": "Биология 12 клас",
        "subcategory_name": "7. клас",
        "username": "ivanobreshkov",
        "verified": true
    },
    "sets": [
        {
            "category_name": null,
            "set_description": "TestXSS2",
            "set_id": "01HPAHT16F5D952J6RVM5YVS9Y",
            "set_modification_date": "2024-02-11 00:22:03.471414",
            "set_name": "TestXSS2",
            "subcategory_name": null,
            "username": "ivanobreshkov",
            "verified": true
        },
        {
            "category_name": "Немски език",
            "set_description": "dasasdasd",
            "set_id": "01HNTG557YFV22V35F2CSV968C",
            "set_modification_date": "2024-02-04 16:45:19.999109",
            "set_name": "aslkdnoiasnfasofniosanfoiansfoifasiansfoisanfoasnfo",
            "subcategory_name": "A2",
            "username": "ivanobreshkov",
            "verified": null
        },
        {
            "category_name": null,
            "set_description": "English B2.2 Conditionals",
            "set_id": "01HM28VZ67JWD4496BJEY6V5RX",
            "set_modification_date": "2024-01-13 20:40:30.663416",
            "set_name": "Conditionals",
            "subcategory_name": null,
            "username": "zapomnigo",
            "verified": null
        }
    ],
    "total_pages": 1
}
```

- 404: `{"message": "Folder doesn't exist"}`

3. `POST /folders`

   This endpoint is used to create a new folder.

  Example request body:
```json
{
    "folder_title": "test_folder1",
    "folder_description": "test_description",
    "category_id": "01HJM17CGHV66Q9940GAP8AJXK",
    "organization_id": "01HJPEXW8Y21R5P4JGME8X5Q19",
    "sets": [
        "01HJM17CGHV66Q9940GAP8AJXK",
        "01HJPEXW8Y21R5P4JGME8X5Q19"
    ]
}
```

  Responses:
    - 200: `{"folder_id": "id"}`
    - 422: `{"validation errors": {...}}`
    - 409: 
```json
{
    "error": "Key (category_id)=(test) is not present in table \"categories\"."
}

{
    "error": "Key (organization_id)=(fdafsda) is not present in table \"organizations\"."
}

{
    "error": "Key (set_id)=(dfasa) is not present in table \"sets\"."
}

{
    "error": "Key (folder_id, set_id)=(01HM6MDDWHX0MYNKJ06081W7NT, 01HJPEXW8Y21R5P4JGME8X5Q19) already exists."
}
```
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

4. `PUT /folders/<folder_id>`

   This endpoint is used to update a specific folder.

  Example request body:
   ```json
   {
       "folder_name": "Updated Folder"
   }
   ```
  Responses:
    - 200: `{"message": "folder successfully updated"}`
    - 422: `{"validation errors": {...}}`
    - 404: `{"message": "folder with such id doesn't exist"}`
    - 409: 
```json
{
    "error": "Key (category_id)=(test) is not present in table \"categories\"."
}

{
    "error": "Key (organization_id)=(fdafsda) is not present in table \"organizations\"."
}

{
    "error": "Key (set_id)=(dfasa) is not present in table \"sets\"."
}

{
    "error": "Key (folder_id, set_id)=(01HM6MDDWHX0MYNKJ06081W7NT, 01HJPEXW8Y21R5P4JGME8X5Q19) already exists."
}
```
    - 403: `{"message": "Admin privileges required."}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

5. `DELETE /folders/<folder_id>`

   This endpoint is used to delete a specific folder.

   Responses:
    - 200: `"message": "Folder successfully deleted"}`
    - 404: `{"message": "folder with such id doesn't exist"}`
    - 403: `{"message": "Admin privileges required."}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

6. `GET /users/<user_id>/folders`

   This endpoint is used to get all folders for a specific user.

    * query parameters:

    * page (int): The page number to retrieve (default is 1).
    * size (int): The number of folders per page (default is 20).
    * sort_by_date (bool): If True (default), the folders are ordered by creation date.
    * ascending (bool): If True, the folders are ordered in ascending order, else in descending order.
    * search_terms (str): If provided, fetch folders that match the search terms (default is None).

    * if sort_by_date=true&ascending=false - Order items by creation date (from last to first created)
    * if sort_by_date=true&ascending=true - Order items by creation date (from first to last created)
    * if sort_by_date=false&ascending=true - Order items by alphabetical order (from A-Z)
    * if sort_by_date=false&ascending=false - Order items by alphabetical order (from Z-A)

   Responses:
    - 200:

```json
    {
  "current_page": 1,
  "folders": [
    {
      "folder_id": "01HPKSRZVCVXP2S1C5C23G5X7H",
      "folder_name": "math",
      "folder_creation_date": "2024-02-14 12:34:27.820104",
      "username": "zapomnigo"
    }
  ],
  "total_items": 239,
  "total_pages": 239
}
```

- 404: `{"message": "user doesn't exist"}, 404`

7. `POST /folders/<folder_id>/report`

   This endpoint is used to report a specific folder.

  Example request body:
   ```json
   {
       "reason": "Report reason"
   }
   ```
  Responses:
    - 200: `{"message": "Folder successfully reported"}`
    - 422: `{"validation errors": {...}}`
    - 404: `{"message": "Folder doesn't exist"}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`

8. `POST /folders/<folder_id>/verify`

   This endpoint is used to change the verified status of a specific folder.

  Example request body:
   ```json
   {
       "verified": true
   }
   ```
  Responses:
    - 200: `{"message": "folder verified status changed successfully"}`
    - 422: `{"validation errors": {...}}`
    - 404: `{"message": "Folder doesn't exist"}`
    - 403: `{"message": "Admin privileges required."}`
    - 498: `{"message": "Auth token expired."}`
    - 401: `{"message": "Invalid token signature."}`
    - 499: `{"message": "Invalid or missing auth token."}`
