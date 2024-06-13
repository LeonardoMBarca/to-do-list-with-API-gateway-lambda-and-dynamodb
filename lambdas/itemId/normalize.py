import json

def normalize_event(event):
    http_method = event['httpMethod']
    
    body = {}
    if 'body' in event and event['body']:
        body = json.loads(event['body'])

    query_string_parameters = event.get('queryStringParameters', {})
    path_parameters = event.get('pathParameters', {})

    return {
        'httpMethod': http_method,
        'body': body,
        'queryStringParameters': query_string_parameters,
        'pathParameters': path_parameters
    }
