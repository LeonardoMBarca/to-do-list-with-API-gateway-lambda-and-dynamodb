import json
import boto3
from normalize import normalize_event
from response import build_response

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('desafio-to-do-leonardo-barca')

def lambda_handler(event, context):
    print(f'Dados recebidos no lambda: {event}')
    
    http_method = event['httpMethod']
    print(f'Método HTTP: {http_method}')
    
    if http_method == 'GET':
        return get_task(event, context)
    elif http_method == 'DELETE':
        return delete_task(event, context)
    elif http_method == 'PUT':
        return update_task(event, context)
    else:
        return build_response(405, {'Message': 'Method is not allowed'})
    
def get_task(event, context):
    try:
        normalized_event = normalize_event(event)
        print(f'Evento normalizado: {normalized_event}')
        
        task_id = normalized_event.get('data', {}).get('pathParameters', {}).get('taskId')
        print(f'ID da tarefa: {task_id}')
        
        if task_id:
            response = table.get_item(Key={"PK": f'TASK#{task_id}', "SK": "TASK#TASK"})
            item = response.get('Item')
            print(f'Item encontrado: {item}')
            
            if item:
                return build_response(200, item)
            else:
                return build_response(404, {'error': 'Item not found'})
        else:
            return build_response(400, {'error': 'TaskId not provided'})
    except Exception as e:
        print(f'Erro ao buscar a tarefa: {e}')
        return build_response(500, {'error': str(e)})


def delete_task(event, context):
    try:
        normalized_event = normalize_event(event)
        print(f'Evento normalizado: {normalized_event}')
        
        task_id = normalized_event.get('data', {}).get('pathParameters', {}).get('taskId')
        print(f'ID da tarefa: {task_id}')
        
        if task_id:
            response = table.get_item(Key={'PK': f'TASK#{task_id}', "SK": "TASK#TASK"})
            if 'Item' not in response:
                return build_response(404, {'error': 'Item with specified PK not found'})
            
            table.delete_item(Key={'PK': f'TASK#{task_id}', "SK": "TASK#TASK"})
            print('Tarefa deletada com sucesso')
            return build_response(200, {'message': 'Item deleted successfully'})
        else:
            return build_response(400, {'error': 'TaskId not provided'})
    except Exception as e:
        print(f'Erro ao deletar a tarefa: {e}')
        return build_response(500, {'error': str(e)})


def update_task(event, context):
    try:
        print("Iniciando função update_task")
        normalized_event = normalize_event(event)
        print(f'Evento normalizado: {normalized_event}')
        
        task_id = normalized_event.get('data', {}).get('pathParameters', {}).get('taskId')
        print(f'ID da tarefa: {task_id}')
        

        body = normalized_event.get('data', {}).get('body', '{}')
        new_data = body  
        
        print(f'Novos dados da tarefa: {new_data}')
        

        if not task_id:
            print("TaskId não encontrado no evento")
            return build_response(400, {'error': 'TaskId not provided'})
        
        print("Chamando table.update_item")
        response = table.update_item(
            Key={'PK': f'TASK#{task_id}', "SK": "TASK#TASK"},
            UpdateExpression='SET #name = :name, #description = :description, #status = :status, #date = :date',
            ExpressionAttributeNames={
                '#name': 'name',
                '#description': 'description',
                '#status': 'status',
                '#date': 'date'
            },
            ExpressionAttributeValues={
                ':name': new_data.get('name'),
                ':description': new_data.get('description'),
                ':status': new_data.get('status'),
                ':date': new_data.get('date')
            },
            ConditionExpression='attribute_exists(PK) AND attribute_exists(SK)',
            ReturnValues='ALL_NEW'
        )
        print('Tarefa atualizada com sucesso')
        
        return build_response(200, {'message': 'Item updated successfully'})
    except table.meta.client.exceptions.ConditionalCheckFailedException:
        print('Tarefa não encontrada')
        return build_response(404, {'error': 'Item not found'})
    except Exception as e:
        print(f'Erro ao atualizar a tarefa: {e}')
        return build_response(500, {'error': str(e)})
