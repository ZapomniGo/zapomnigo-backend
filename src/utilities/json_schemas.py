register_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', "minLength": 2,
                 "maxLength": 40},
        'username': {'type': 'string', "minLength": 2,
                     "maxLength": 40},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'},
        'age': {'type': 'integer', "minimum": 5,
                "maximum": 99},
        'gender': {'type': 'string'},
        'privacy_policy': {'type': 'string'},
        'terms_and_conditions': {'type': 'string'},
        'marketing_consent': {'type': 'string'}
    },
    'required': ['username', 'name', 'email', 'password', 'privacy_policy', 'terms_and_conditions',
                 'marketing_consent'],
    'additionalProperties': False
}
