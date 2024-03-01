Sure, here is the documentation for your `subcategories_routes.py` file:

1. `POST /subcategories`

   This endpoint is used to create a new subcategory.

   Example request body:
   ```json
   {
       "subcategory_name": "Test subcategory"
   }
   ```
   Responses:
    - 200: `{"message": "Subcategory added to db"}`
    - 422: `{"validation errors": {...}}`
    - 409: `{"error": "Subcategory already exists"}`

2. `GET /categories/<category_id>/subcategories`

   This endpoint is used to get all subcategories for a specific category.

   Responses:
    - 200: `{"category_id": "category_id", "category_name": "category_name", "subcategories": [{...}, {...}, ...]}`
    - 404: `{"message": "The current category doesn't have subcategories"}`

3. `POST /categories/<category_id>/subcategories`

   This endpoint is used to create new subcategories for a specific category.

   Example request body:
   ```json
   {
       "subcategories": ["subcategory_id1", "subcategory_id2", ...],
       "order": [1, 2, ...]
   }
   ```
   Responses:
    - 200: `{"message": "Subcategories successfully added to category"}`
    - 422: `{"validation errors": {...}}`
    - 404: `{"message": "category with such id doesn't exist"}`
