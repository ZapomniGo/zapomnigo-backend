register_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'username': {'type': 'string'},
        'email': {'type': 'string', 'format': 'email'},
        'password': {'type': 'string'},
        'age': {'type': 'integer'},
        'gender': {'type': 'string'},
        'privacy_policy': {'type': 'string'},
        'terms_and_conditions': {'type': 'string'},
        'marketing_consent': {'type': 'string'}
    },
    'required': ['name', 'username', 'email', 'password', 'privacy_policy', 'terms_and_conditions',
                 'marketing_consent'],
    'additionalProperties': False
}
