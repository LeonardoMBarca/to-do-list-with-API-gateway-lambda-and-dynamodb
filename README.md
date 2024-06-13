# Sistema de Gerenciamento de Tarefas - Arquitetura Serverless na AWS

Este projeto implementa um sistema de gerenciamento de tarefas utilizando arquitetura serverless na AWS, integrando serviços como Amazon API Gateway, AWS Lambda e Amazon DynamoDB. O sistema oferece uma API REST para realizar operações CRUD (Create, Read, Update, Delete) em listas de tarefas e seus itens associados.

## Desafio e Objetivo

### Contexto do Desafio

Você foi contratado pela Tech Solutions para desenvolver e implementar a infraestrutura na AWS para um sistema de gerenciamento de tarefas. O projeto requer o uso das melhores práticas de arquitetura de nuvem para garantir escalabilidade e eficiência.

### Objetivo

O objetivo deste desafio é criar uma aplicação serverless na AWS que utilize Amazon API Gateway para expor endpoints RESTful, AWS Lambda para processar lógica de negócios e Amazon DynamoDB para armazenar os dados das tarefas e seus itens.

## Funcionalidades da API

A API oferece as seguintes funcionalidades:

- **Listar todas as listas de tarefas**
- **Obter uma lista de tarefas específica**
- **Criar uma nova lista de tarefas**
- **Editar uma lista de tarefas existente**
- **Apagar uma lista de tarefas**
- **Adicionar itens a uma lista de tarefas**
- **Listar os itens de uma lista de tarefas**
- **Remover itens de uma lista de tarefas**
- **Editar um item de uma lista de tarefas**
- **Marcar um item como concluído**

## Arquitetura da AWS

![Diagrama da Arquitetura]([https://url-da-sua-imagem-aws-architecture.png](https://github.com/LeonardoMBarca/to-do-lista-with-API-gateway-lambda-and-dynamodb/blob/main/images/Captura%20de%20tela%202024-06-13%20103805.png?raw=true))

### Componentes da Arquitetura

- **Amazon API Gateway:** Ponto de entrada para o sistema, gerenciando as requisições HTTP e roteando-as para as funções Lambda apropriadas.
- **AWS Lambda:** Serviço de computação serverless que executa o código em resposta a eventos, como as requisições do API Gateway.
- **Amazon DynamoDB:** Banco de dados NoSQL totalmente gerenciado, utilizado para armazenar as listas de tarefas e seus itens.

### Instruções para Implementação

1. **Desenvolvimento da Aplicação**
   - Implemente a aplicação utilizando Python, criando funções Lambda para processar as requisições do API Gateway.

2. **Configuração do DynamoDB**
   - Crie uma tabela no DynamoDB para armazenar as listas de tarefas, utilizando a chave primária adequada (ex.: `taskId`).

3. **Implementação das Funções Lambda**
   - Desenvolva as funções Lambda necessárias para cada operação CRUD, configurando permissões para acessar o DynamoDB.

4. **Configuração do API Gateway**
   - Configure uma nova API REST no Amazon API Gateway, definindo os recursos e métodos necessários para o sistema de gerenciamento de tarefas.

### Recursos Adicionais

- **Documentações da AWS:**
  - [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
  - [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
  - [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)

- **Tutoriais da AWS:**
  - [Getting Started with Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
  - [Getting Started with AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)
  - [Getting Started with Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStartedDynamoDB.html)

## Frontend e Interface Gráfica

O frontend foi desenvolvido utilizando Streamlit em Python. A interface gráfica pode ser acessada [aqui](https://to-do-lista-with-api-gateway-lambda-and-dynamodb-j79y5hsocwqtb.streamlit.app/).

## Estrutura da API REST

A estrutura da API REST segue o seguinte padrão:


## Considerações Finais

Certifique-se de compreender a estrutura de precificação dos serviços da AWS antes de começar a utilizá-los. Nomeie os recursos com seu nome para facilitar a identificação posteriormente.

Para testar as operações da API, recomenda-se o uso de ferramentas como Insomnia.
