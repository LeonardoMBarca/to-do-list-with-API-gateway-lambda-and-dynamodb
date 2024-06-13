import json
import boto3
from normalize import normalize_event
from response import build_response

ddb = boto3.resource('dynamodb')
table = ddb.Table('desafio-to-do-leonardo-barca')  # Nome da tabela no DynamoDB

def lambda_handler(event, context):
    print("Dados recebidos no lambda_handler:", event)
    
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return get_item_method(event, context)
    elif http_method == 'PUT':
        return put_item_method(event, context)
    elif http_method == 'DELETE':
        return delete_item_method(event, context)
    else:
        return build_response(405, {'message': 'Method not allowed'})

def get_item_method(event, context):
    # Normaliza o evento para obter os dados relevantes
    normalized_event = normalize_event(event)
    print(f'Dados normalizados: {normalized_event}')
    
    # Extrai a chave PK dos pathParameters
    path_parameters = normalized_event['body']['body']['pathParameters']
    pk = path_parameters.get('PK')
    
    try:
        # Corrige a chave PK para incluir o prefixo adequado
        pk_with_prefix = f"TASK#{pk}"
        
        print(f"Consultando DynamoDB para PK: {pk_with_prefix}")
        
        # Consulta o DynamoDB para obter a tarefa com a chave PK especificada
        response = table.get_item(Key={'PK': pk_with_prefix, 'SK': 'TASK#TASK'})
        task = response.get('Item')
        print(f"Tarefa encontrada: {task}")
        
        # Se a tarefa não existir, retorna um erro 404
        if not task:
            return build_response(404, {'message': 'Task not found'})
        
        # Agora, vamos buscar o item específico dentro da tarefa com base na chave SK do item
        sk = path_parameters.get('SK')  # Aqui assumindo que 'SK' é a chave do item desejado
        
        print(f"Consultando item com SK: {sk}")
        
        # Busca o item específico dentro da tarefa encontrada

        items = task.get('itens', [])
        
        if not items:
            return build_response(404, {'message': 'Task not found'})
        
        for i in items:
            if i['sk'] == sk:
                item = i
                break            

        # Se o item não for encontrado, retorna um erro 404
        if not item:
            return build_response(404, {'message': 'Item not found'})
        
        # Prepara a resposta com os detalhes do item encontrado
        response_data = {
            'message': 'Item found successfully',
            'item': item
        }
        
        return build_response(200, response_data)
    
    except Exception as e:
        print(f"Error fetching item: {e}")
        return build_response(500, {'message': 'Failed to fetch item'})
        
def put_item_method(event, context):
    # Normaliza o evento para obter os dados relevantes
    normalized_event = normalize_event(event)
    print(f'Dados normalizados: {normalized_event}')
    
    # Extrai a chave PK e SK dos pathParameters
    path_parameters = normalized_event['body']['pathParameters']
    pk = path_parameters.get('PK')
    sk = path_parameters.get('SK')
    
    # Extrai os novos valores do corpo da solicitação
    body = normalized_event['body']['body']
    new_name = body.get('name')
    new_description = body.get('description')
    new_status = body.get('status')
    new_date = body.get('date')
    
    try:
        # Corrige a chave PK para incluir o prefixo adequado
        pk_with_prefix = f"TASK#{pk}"
        
        print(f"Consultando DynamoDB para PK: {pk_with_prefix}")
        
        # Consulta o DynamoDB para obter a tarefa com a chave PK especificada
        response = table.get_item(Key={'PK': pk_with_prefix, 'SK': 'TASK#TASK'})
        task = response.get('Item')
        print(f"Tarefa encontrada: {task}")
        
        # Se a tarefa não existir, retorna um erro 404
        if not task:
            return build_response(404, {'message': 'Task not found'})
        
        # Busca o item específico dentro da tarefa encontrada
        items = task.get('itens', [])
        
        if not items:
            return build_response(404, {'message': 'No items found in the task'})
        
        item = None
        for i in items:
            if i['sk'] == sk:
                item = i
                break
        
        # Se o item não for encontrado, retorna um erro 404
        if not item:
            return build_response(404, {'message': 'Item not found'})
        
        # Atualiza os campos do item com os novos valores
        if new_name is not None:
            item['name'] = new_name
        if new_description is not None:
            item['description'] = new_description
        if new_status is not None:
            item['status'] = new_status
        if new_date is not None:
            item['date'] = new_date
        
        # Atualiza a tarefa com a nova lista de itens
        task['itens'] = items
        
        # Salva a tarefa atualizada no DynamoDB
        table.put_item(Item=task)
        
        # Prepara a resposta com a confirmação da atualização do item
        response_data = {
            'message': 'Item updated successfully',
            'item': item
        }
        
        return build_response(200, response_data)
    
    except Exception as e:
        print(f"Error updating item: {e}")
        return build_response(500, {'message': 'Failed to update item'})
    
def delete_item_method(event, context):
    # Normaliza o evento para obter os dados relevantes
    normalized_event = normalize_event(event)
    print(f'Dados normalizados: {normalized_event}')
    
    # Extrai a chave PK dos pathParameters
    path_parameters = normalized_event['body']['pathParameters']
    pk = path_parameters.get('PK')
    
    try:
        # Corrige a chave PK para incluir o prefixo adequado
        pk_with_prefix = f"TASK#{pk}"
        
        print(f"Consultando DynamoDB para PK: {pk_with_prefix}")
        
        # Consulta o DynamoDB para obter a tarefa com a chave PK especificada
        response = table.get_item(Key={'PK': pk_with_prefix, 'SK': 'TASK#TASK'})
        task = response.get('Item')
        print(f"Tarefa encontrada: {task}")
        
        # Se a tarefa não existir, retorna um erro 404
        if not task:
            return build_response(404, {'message': 'Task not found'})
        
        # Agora, vamos buscar o item específico dentro da tarefa com base na chave SK do item
        sk = path_parameters.get('SK')  # Aqui assumindo que 'SK' é a chave do item desejado
        
        print(f"Consultando item com SK: {sk}")
        
        # Busca o item específico dentro da tarefa encontrada
        items = task.get('itens', [])
        
        if not items:
            return build_response(404, {'message': 'No items found in the task'})
        
        item = None
        for i in items:
            if i['sk'] == sk:
                item = i
                break
        
        # Se o item não for encontrado, retorna um erro 404
        if not item:
            return build_response(404, {'message': 'Item not found'})
        
        # Remove o item da lista de itens
        items.remove(item)
        
        # Atualiza a tarefa com a nova lista de itens
        task['itens'] = items
        
        # Salva a tarefa atualizada no DynamoDB
        table.put_item(Item=task)
        
        # Prepara a resposta com a confirmação da remoção do item
        response_data = {
            'message': 'Item deleted successfully'
        }
        
        return build_response(200, response_data)
    
    except Exception as e:
        print(f"Error deleting item: {e}")
        return build_response(500, {'message': 'Failed to delete item'})