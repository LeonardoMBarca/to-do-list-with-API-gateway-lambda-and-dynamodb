import json
import boto3
import uuid
from normalize import normalize_event
from response import build_response

AWS_REGION = "us-east-1"
DYNAMO_TABLE_NAME = "desafio-to-do-leonardo-barca"

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMO_TABLE_NAME)

def lambda_handler(event, context):
    print("Dados recebidos no lambda_handler:", event)
    
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return get_method(event, context)
    elif http_method == 'POST':
        return post_method(event, context)
    else:
        return build_response(405, {'message': 'Method not allowed'})

def get_method(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])
        return build_response(200, items)
    except Exception as e:
        return build_response(500, {'error': str(e)})
        
def post_method(event, context):
    try:
        normalized_event = normalize_event(event)
        data = normalized_event['data']['body']
        
        print("Dados recebidos:", data)
        
        name = data.get('name', None)
        description = data.get('description', None)
        status = data.get('status', None)
        date = data.get('date', None)
        
        print("Valores dos campos:", name, description, status, date)
        
        task_id = f'TASK#{str(uuid.uuid4())}'
        

        item = {
            'PK': task_id,  
            'SK': 'TASK#TASK',
            'name': name,
            'description': description,
            'status': status,
            'date': date,
            'itens': []
        }
        
        print("Item a ser inserido:", item)
        
        table.put_item(Item=item)
        
        return build_response(200, {'message': 'Tarefa criada com sucesso'})
    except Exception as e:
        return build_response(500, {'error': str(e)})

