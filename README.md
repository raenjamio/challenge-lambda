Python-Flask - AWS Lambda function to fetch data from a DynamoDB and a relational DB

Create and GetAll for DynamoDB and RDS DB

Create table in DynamoDB and configure environment variables:

 ![dynamoDB](./img/keys.jpg)

URL: */dynamoDb

POST Body: 
{
     "name": "dynamodb3",
     "email": "dynamodb2@gmail.com"	
 }

RDS DB: 

URL: */rds

POST Body:
{
     "name": "dynamodb5",
     "description": "dynamodb5@gmail.com"	
 }


Test:

DynamoDB

 ![dynamoDB](./img/dynamoDB.jpg)
 
GetALL
 ![dynamoDB](./img/dynamoDB2.jpg)

Post
 ![dynamoDB](./img/dynamoDBPost.jpg) 
  

RDS

GetALL
 ![dynamoDB](./img/rdsDBGet.jpg)

Post
 ![dynamoDB](./img/rdsDBPost.jpg) 