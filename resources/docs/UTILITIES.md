### `GET /health` - could be used for e heartbeat service
Responses: `{"status": healthy}, 200`

### `GET /search`

This endpoint is used to search for sets and folders.

* query parameters:

    * q (str): The search terms to use.
    * sets_page_number (int): The page number to retrieve for sets (default is 1).
    * sets_page_size (int): The number of sets per page (default is 20).
    * folders_page_number (int): The page number to retrieve for folders (default is 1).
    * folders_page_size (int): The number of folders per page (default is 20).
    * category_id (str): If provided, fetch sets and folders associated with the specified category (default is None).
    * subcategory_id (str): If provided, fetch sets and folders associated with the specified subcategory (default is None).

Responses:

- 200:

```json
{
  "results": {
    "sets": [
      {
        "set_id": "set_id",
        "set_name": "set_name",
        "set_description": "set_description",
        "set_modification_date": "set_modification_date",
        "category_name": "category_name",
        "subcategory_name": "subcategory_name",
        "username": "username",
        "verified": true,
        "rank": "rank"
      },
      ...
    ],
    "sets_pagination": {
      "total_pages": "total_pages",
      "current_page": "current_page",
      "total_items": "total_items"
    },
    "folders": [
      {
        "folder_id": "folder_id",
        "folder_title": "folder_title",
        "folder_description": "folder_description",
        "folder_modification_date": "folder_modification_date",
        "category_name": "category_name",
        "subcategory_name": "subcategory_name",
        "username": "username",
        "verified": true,
        "rank": "rank"
      },
      ...
    ],
    "folders_pagination": {
      "total_pages": "total_pages",
      "current_page": "current_page",
      "total_items": "total_items"
    }
  }
}
```
* 400: `{"message": "No search query provided"}`

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
- 422: `{"validation errors": {...}}`
* 404 
`{"message": "invalid argument provided"}` or `{"message": "user doesn't exist"}`
- 429: `{"message": "Rate limit exceeded."}`