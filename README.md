# Task Management System - Serverless Architecture on AWS

This project implements a task management system using serverless architecture on AWS, integrating services such as Amazon API Gateway, AWS Lambda, and Amazon DynamoDB. The system offers a REST API to perform CRUD (Create, Read, Update, Delete) operations on task lists and their associated items.

## Challenge and Objective

### Challenge Context

You've been hired by Tech Solutions to develop and implement the AWS infrastructure for a task management system. The project requires the use of best cloud architecture practices to ensure scalability and efficiency.

### Objective

The objective of this challenge is to create a serverless application on AWS that utilizes Amazon API Gateway to expose RESTful endpoints, AWS Lambda to process business logic, and Amazon DynamoDB to store task data and its associated items.

## API Features

The API offers the following functionalities:

- **List all task lists**
- **Get a specific task list**
- **Create a new task list**
- **Edit an existing task list**
- **Delete a task list**
- **Add items to a task list**
- **List items in a task list**
- **Remove items from a task list**
- **Edit an item in a task list**
- **Mark an item as completed**

## AWS Architecture

![Architecture Diagram](https://github.com/LeonardoMBarca/to-do-lista-with-API-gateway-lambda-and-dynamodb/blob/main/images/Captura%20de%20tela%202024-06-13%20103805.png?raw=true)

### Architecture Components

- **Amazon API Gateway:** Entry point for the system, managing HTTP requests and routing them to appropriate Lambda functions.
- **AWS Lambda:** Serverless compute service that executes code in response to events, such as API Gateway requests.
- **Amazon DynamoDB:** Fully managed NoSQL database used to store task lists and their items.

### Implementation Instructions

1. **Application Development**
   - Implement the application using Python, creating Lambda functions to process API Gateway requests.

2. **DynamoDB Configuration**
   - Create a table in DynamoDB to store task lists, using the appropriate primary key (e.g., `taskId`).

3. **Lambda Function Implementation**
   - Develop the necessary Lambda functions for each CRUD operation, configuring permissions to access DynamoDB.

4. **API Gateway Configuration**
   - Configure a new REST API in Amazon API Gateway, defining the necessary resources and methods for the task management system.

### Additional Resources

- **AWS Documentation:**
  - [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
  - [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
  - [Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)

- **AWS Tutorials:**
  - [Getting Started with Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
  - [Getting Started with AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)
  - [Getting Started with Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStartedDynamoDB.html)

## Frontend and GUI

The frontend was developed using Streamlit in Python.

## REST API Structure

![Architecture Diagram](https://github.com/LeonardoMBarca/to-do-lista-with-API-gateway-lambda-and-dynamodb/blob/main/images/Captura%20de%20tela%202024-06-13%20111132.png?raw=true)

## Final Considerations

Make sure to understand the pricing structure of AWS services before starting to use them. Name resources with your name for easier identification later.

To test API operations, tools like Insomnia are recommended.
