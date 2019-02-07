import os
import json
import boto3


DynamodbTableName = os.environ['DYNAMODB_TABLE_NAME']


def on_connect(event, context):
    boto3.client('dynamodb').put_item(
        TableName=DynamodbTableName,
        Item={
            'connection_id': {'S': event['requestContext']['connectionId']}
        }
    )
    return {
        'statusCode': 200,
        'body': 'Connected.'
    }


def on_disconnect(event, context):
    boto3.client('dynamodb').delete_item(
        TableName=DynamodbTableName,
        Key={
            'connection_id': {'S': event['requestContext']['connectionId']}
        }
    )
    return {
        'statusCode': 200,
        'body': 'Disconnected.'
    }


def send_message(event, context):
    endpoint_url = 'https://' + event['requestContext']['domainName'] + '/' + event['requestContext']['stage']
    client_api = boto3.client(
        service_name='apigatewaymanagementapi',
        endpoint_url=endpoint_url)

    connections = boto3.client('dynamodb').scan(TableName=DynamodbTableName)
    for conn in connections['Items']:
        client_api.post_to_connection(
            ConnectionId=conn['connection_id']['S'],
            Data=json.loads(event["body"])['data'].encode())
    return {
        'statusCode': 200,
        'body': 'Data sent.'
    }
