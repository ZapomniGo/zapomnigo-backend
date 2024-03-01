### GET /sets/set_id/study - get flashcards with confidence levels
Responses:
* 200
```json
{
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
    }
  ]
}
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