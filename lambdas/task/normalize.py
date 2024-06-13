import json

def normalize_event(event):
    http_method = event['httpMethod']
    
    if 'body' in event and event['body'] is not None:
        body = json.loads(event['body'])
    else:
        body = {}

    query_string_parameters = event['queryStringParameters'] or {}
    path_parameters = event['pathParameters'] or {}

    return {
        'method': http_method,
        'data': body,
        'querystring': query_string_parameters,
        'pathParameters': path_parameters
    }
