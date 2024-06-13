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
        return get_item_method(event, context)
    elif http_method == 'POST':
        return post_item_method(event, context)
    else:
        return build_response(405, {'message': 'Method not allowed'})

def get_item_method(event, context):
    # Normaliza o evento para obter os dados relevantes
    normalized_event = normalize_event(event)
    print(f'Dados normalizados: {normalized_event}')
    # Extrai a chave PK da pathParameters
    path_parameters = normalized_event['body']['pathParameters']
    
    if path_parameters is None or 'PK' not in path_parameters:
        return build_response(400, {'message': 'Missing PK in path parameters'})
    
    pk = path_parameters['PK']
    
    try:
        # Corrige a chave PK para incluir o prefixo "TASK#"
        pk_with_prefix = f"TASK#{pk}"
        
        print(f"Consultando DynamoDB para PK: {pk_with_prefix}")
        
        # Consulta o DynamoDB para obter a tarefa com a chave PK especificada
        response = table.get_item(Key={'PK': pk_with_prefix, 'SK': 'TASK#TASK'})
        item = response.get('Item', None)
        
        if not item:
            return build_response(404, {'message': 'Task not found'})
            
        items = item.get('itens', [])
        
        print(f"Itens encontrados: {items}")
        
        # Prepara a resposta com os detalhes de todos os itens encontrados
        response_data = {
            'message': 'Items found successfully',
            'items': items
        }
        
        return build_response(200, response_data)
    
    except Exception as e:
        print(f"Error fetching items: {e}")
        return build_response(500, {'message': 'Failed to fetch items'})
def post_item_method(event, context):
    # Normaliza o evento para obter os dados relevantes
    normalized_event = normalize_event(event)
    
    # Extrai os dados do corpo da requisição
    body = normalized_event['body']
    
    # Verifica se todos os dados necessários estão presentes
    if 'PK' not in body or 'itens' not in body:
        return build_response(400, {'message': 'PK and itens array are required in the request body'})
    
    pk = body['PK']
    subtasks = body['itens']
    
    # Verifica se a tarefa já existe no DynamoDB
    try:
        # Corrige a chave PK para incluir o prefixo "TASK#"
        pk_with_prefix = f"TASK#{pk}"
        
        response = table.get_item(Key={'PK': pk_with_prefix, 'SK': "TASK#TASK"})
        item = response.get('Item')
        
        if not item:
            return build_response(404, {'message': 'Task not found'})
        
        # Gera a chave sk aleatória para cada subtarefa
        for subtask in subtasks:
            subtask['sk'] = uuid.uuid4().hex
        
        # Atualiza a lista de subtarefas na tarefa existente
        if 'itens' in item:
            item['itens'].extend(subtasks)
        else:
            item['itens'] = subtasks
        
        # Atualiza a tarefa no DynamoDB
        table.put_item(Item=item)
        
        return build_response(200, {'message': 'Itens added successfully'})
    
    except Exception as e:
        print(f"Error updating task: {e}")
        return build_response(500, {'message': 'Failed to add itens to task'})
