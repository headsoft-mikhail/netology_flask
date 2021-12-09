POST_CREATE = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'text': {'type': 'string'},
        'created_at': {'type': 'string',
                       'pattern': '^\d{4}-\d{2}-\d{2}$'
                       }
    },
    'required': ['title']
}

POST_UPDATE = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'text': {'type': 'string'},
        'created_at': {'type': 'string',
                       'pattern': '^\d{4}-\d{2}-\d{2}$'
                       }
    },
    'required': []
}

USER_CREATE = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string',
                  'pattern': '.+\@.+\..+'},
        'password': {'type': 'string'},
        'name': {'type': 'string'}
    },
    'required': ['email', 'password']
}
