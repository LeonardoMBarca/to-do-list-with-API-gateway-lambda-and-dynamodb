import streamlit as st
import requests
import json
from datetime import date

# Endpoints da sua API
API_URL = ""  # Substitua pela URL da sua API

# Funções para interagir com a API
def get_all_tasks():
    response = requests.get(f"{API_URL}/task")
    return response.json()

def create_task(name, description, status, due_date):
    task = {
        "httpMethod": "POST",
        "body": {
            "name": name,
            "description": description,
            "status": status,
            "date": due_date.strftime('%Y-%m-%d')
        },
        "queryStringParameters": None,
        "pathParameters": None
    }
    response = requests.post(f"{API_URL}/task", json=task)
    return response.json()

def get_task(task_id):
    payload = {
        "httpMethod": "GET",
        "pathParameters": {
            "taskId": task_id
        }
    }
    response = requests.get(f"{API_URL}/task/taskId", json=payload)
    return response.json()

def update_task(task_id, name, description, status, due_date):
    task = {
        "httpMethod": "PUT",
        "pathParameters": {
            "taskId": task_id
        },
        "body": {
            "name": name,
            "description": description,
            "status": status,
            "date": due_date.strftime('%Y-%m-%d')
        }
    }
    response = requests.put(f"{API_URL}/task/taskId", json=task)
    return response.json()

def delete_task(task_id):
    payload = {
        "httpMethod": "DELETE",
        "pathParameters": {
            "taskId": task_id
        }
    }
    response = requests.delete(f"{API_URL}/task/taskId", json=payload)
    return response.json()

def get_task_items(task_id):
    payload = {
        "httpMethod": "GET",
        "queryStringParameters": None,
        "pathParameters": {
            "PK": task_id
        }
    }
    response = requests.get(f"{API_URL}/task/taskId/itens", json=payload)
    return response.json()

def create_task_item(task_id, items):
    payload = {
        "PK": task_id,
        "itens": items
    }
    response = requests.post(f"{API_URL}/task/taskId/itens", json=payload)
    return response.json()

def get_task_item(task_id, item_id):
    payload = {
        "httpMethod": "GET",
        "body": {
            "pathParameters": {
                "PK": task_id,
                "SK": item_id
            }
        }
    }
    response = requests.get(f"{API_URL}/task/taskId/itens/itemId", json=payload)
    return response.json()

def update_task_item(task_id, item_id, name, description, status, due_date):
    item = {
        "httpMethod": "PUT",
        "body": {
            "name": name,
            "description": description,
            "status": status,
            "date": due_date.strftime('%Y-%m-%d')
        },
        "pathParameters": {
            "PK": task_id,
            "SK": item_id
        },
        "queryStringParameters": {}
    }
    response = requests.put(f"{API_URL}/task/taskId/itens/itemId", json=item)
    return response.json()

def delete_task_item(task_id, item_id):
    payload = {
        "httpMethod": "DELETE",
        "body": "{}",
        "pathParameters": {
            "PK": task_id,
            "SK": item_id
        },
        "queryStringParameters": {}
    }
    response = requests.delete(f"{API_URL}/task/taskId/itens/itemId", json=payload)
    return response.json()

# Interface do Streamlit
st.set_page_config(page_title="To-Do List", page_icon=":memo:", layout="wide")

st.title("📝 To-Do List")
st.markdown("---")

# Seção de Exibição de Todas as Tarefas
st.header("📋 Todas as Tarefas")
if st.button("Mostrar Todas as Tarefas"):
    tasks = get_all_tasks()
    if len(tasks) > 0:
        for task in tasks:
            st.subheader(task['name'])
            st.write(f"PK: {task['PK']}")
            st.write(f"Descrição: {task['description']}")
            st.write(f"Status: {task['status']}")
            st.write(f"Data Limite: {task['date']}")
            st.write(f"Itens: {task['itens']}")
            st.write("---")
    else:
        st.write("Nenhuma tarefa encontrada.")
st.markdown("---")

# Seção de Criação de Nova Tarefa
st.header("🆕 Criar Nova Tarefa")
with st.form(key='create_task_form'):
    name = st.text_input("Nome")
    description = st.text_area("Descrição")
    status = st.selectbox("Status", ["pendente", "fazendo", "feito"])
    due_date = st.date_input("Data Limite", value=date.today())
    submit_button = st.form_submit_button(label='Criar Tarefa')
    if submit_button:
        result = create_task(name, description, status, due_date)
        st.success("Tarefa criada com sucesso!")
        st.json(result)

st.markdown("---")

# Seção de Visualização de Tarefa
st.header("🔍 Visualizar Tarefa")
task_id_view = st.text_input("Chave PK da Tarefa para Visualizar")
if st.button("Mostrar Tarefa"):
    task = get_task(task_id_view)
    if task:
        st.subheader(task['name'])
        st.write(f"PK: {task['PK']}")
        st.write(f"Descrição: {task['description']}")
        st.write(f"Status: {task['status']}")
        st.write(f"Data Limite: {task['date']}")
        st.write(f"Itens: {task['itens']}")
    else:
        st.error("Tarefa não encontrada")

st.markdown("---")

# Seção de Exclusão de Tarefa
st.header("🗑️ Excluir Tarefa")
task_id_delete = st.text_input("Chave PK da Tarefa para Excluir")
if st.button("Excluir Tarefa"):
    result = delete_task(task_id_delete)
    if 'error' in result:
        st.error("Erro ao excluir a tarefa")
    else:
        st.success("Tarefa excluída com sucesso!")
    st.json(result)

st.markdown("---")

# Seção de Atualização de Tarefa
st.header("✏️ Atualizar Tarefa")
with st.form(key='update_task_form'):
    task_id_update = st.text_input("Chave PK da Tarefa para Atualizar")
    name_update = st.text_input("Nome")
    description_update = st.text_area("Descrição")
    status_update = st.selectbox("Status", ["pendente", "fazendo", "feito"])
    due_date_update = st.date_input("Data Limite", value=date.today())
    submit_button_update = st.form_submit_button(label='Atualizar Tarefa')
    if submit_button_update:
        result = update_task(task_id_update, name_update, description_update, status_update, due_date_update)
        st.success("Tarefa atualizada com sucesso!")
        st.json(result)

st.markdown("---")

# Seção de Itens da Tarefa
st.header("📋 Itens da Tarefa")
task_id_items = st.text_input("Chave PK da Tarefa para Ver Itens")
if st.button("Mostrar Itens"):
    items = get_task_items(task_id_items)
    print(items)
    if len(items['items']) > 0: 
        for item in items['items']:
            st.subheader(item['name'])
            st.write(f"Descrição: {item['description']}")
            st.write(f"Status: {item['status']}")
            st.write(f"Data: {item['date']}")
            st.write(f"SK: {item['sk']}")
            st.write("---")
    else:
        st.error("Nenhum item encontrado")

st.markdown("---")

# Seção de Criação de Item na Tarefa
st.header("🆕 Criar Item na Tarefa")
with st.form(key='create_item_form'):
    task_id_item_create = st.text_input("Chave PK da Tarefa para Criar Item")
    name_item_create = st.text_input("Nome do Item")
    description_item_create = st.text_area("Descrição do Item")
    status_item_create = st.selectbox("Status do Item", ["pendente", "fazendo", "feito"])
    due_date_item_create = st.date_input("Data do Item", value=date.today())
    submit_button_item_create = st.form_submit_button(label='Criar Item')
    if submit_button_item_create:
        items = [
            {
                "sk": "",
                "name": name_item_create,
                "description": description_item_create,
                "status": status_item_create,
                "date": due_date_item_create.strftime('%Y-%m-%d')
            }
        ]
        result = create_task_item(task_id_item_create, items)
        st.success("Item criado com sucesso!")
        st.json(result)

st.markdown("---")

# Seção de Visualização de Item da Tarefa
st.header("🔍 Visualizar Item da Tarefa")
with st.form(key='view_item_form'):
    task_id_item_view = st.text_input("Chave PK da Tarefa para Visualizar Item")
    item_id_view = st.text_input("Chave SK do Item para Visualizar")
    submit_button_item_view = st.form_submit_button(label='Mostrar Item')
    if submit_button_item_view:
        item = get_task_item(task_id_item_view, item_id_view)
        print(item)
        if item:
            st.subheader(item['item']['name'])
            st.write(f"Descrição: {item['item']['description']}")
            st.write(f"Status: {item['item']['status']}")
            st.write(f"Data: {item['item']['date']}")
            st.write(f"SK: {item['item']['sk']}")
        else:
            st.error("Item não encontrado")

st.markdown("---")

# Seção de Exclusão de Item da Tarefa
st.header("🗑️ Excluir Item da Tarefa")
with st.form(key='delete_item_form'):
    task_id_item_delete = st.text_input("Chave PK da Tarefa para Excluir Item")
    item_id_delete = st.text_input("Chave SK do Item para Excluir")
    submit_button_item_delete = st.form_submit_button(label='Excluir Item')
    if submit_button_item_delete:
        result = delete_task_item(task_id_item_delete, item_id_delete)
        if 'error' in result:
            st.error("Erro ao excluir o item")
        else:
            st.success("Item excluído com sucesso!")
        st.json(result)

st.markdown("---")

# Seção de Atualização de Item da Tarefa
st.header("✏️ Atualizar Item da Tarefa")
with st.form(key='update_item_form'):
    task_id_item_update = st.text_input("Chave PK da Tarefa para Atualizar Item")
    item_id_update = st.text_input("Chave SK do Item para Atualizar")
    name_item_update = st.text_input("Nome do Item")
    description_item_update = st.text_area("Descrição do Item")
    status_item_update = st.selectbox("Status do Item", ["pendente", "fazendo", "feito"])
    due_date_item_update = st.date_input("Data do Item", value=date.today())
    submit_button_item_update = st.form_submit_button(label='Atualizar Item')
    if submit_button_item_update:
        result = update_task_item(task_id_item_update, item_id_update, name_item_update, description_item_update, status_item_update, due_date_item_update)
        st.success("Item atualizado com sucesso!")
        st.json(result)
