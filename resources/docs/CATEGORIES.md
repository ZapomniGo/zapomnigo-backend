1. `GET /categories`

   This endpoint is used to get all categories.

   Responses: 
   - 200: `{"categories": [{...}, {...}, ...]}`
   - 404: `{"message": "No categories found"}`

2. `GET /categories/<category_id>`

   This endpoint is used to get a specific category.

   Responses: 
   - 200: `{"category": {...}}`
   - 404: `{"message": "Category doesn't exist"}`

3. `POST /categories`

   This endpoint is used to create a new category. This endpoint requires admin privileges.

   Example request body:
   ```json
   {
       "category_name": "New Category"
   }
   ```
   Responses: 
   - 200: `{"message": "Category created", "category": {...}}`
   - 422: `{"validation errors": {...}}`
   - 409: `{"error": "Category already exists"}`
   - 403: `{"message": "Admin privileges required"}`
