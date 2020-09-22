import json
import boto3
from pprint import pprint


dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def get_item(itemId):
    response = dynamodb.get_item(
    TableName="featured_items",
    Key={
        'id': {'N':itemId},
        }
    )
    return response.get("Item", None)
  
    
def format_response(text,code):
    return {
        'statusCode': code,
        'body': json.dumps(text)
    }

def put_featured_item(itemId, title):
    response = dynamodb.put_item(
        TableName="featured_items",
        Item = {
            'id': {'N': itemId },
            'title': {'S': title },
            'click_count': {'N': '1'}
        }
    )
    return response
    
def increment_count(itemId):

    response = dynamodb.update_item(
        TableName="featured_items",
        Key={
        'id': {'N':itemId},
        },
        UpdateExpression="SET click_count = click_count + :val",
        ExpressionAttributeValues={
            ':val': {
                'N': '1'
            }
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def lambda_handler(event, context):
    try:
        #somehow the body is an
        if isinstance(event["body"],str):
            event["body"] = json.loads(event["body"])
            
        itemId = event.get("body", {}).get("itemId", None)
        if itemId is not None:
            print(f'itemId {itemId}')
            item = get_item(itemId)
            print(item)
            if item is None:
                new_response = put_featured_item(itemId, 'test2')
                print("New item created")
                pprint(new_response, sort_dicts=False)
                return format_response("Success", 200)
            else:
                updated_response = increment_count(itemId)
                print("Count increment successfull")
                pprint(updated_response, sort_dicts=False)
                return format_response("Success", 200)
                
                
    except Exception as e:
        print(str(e))
        return format_response(f'Failed with error {str(e)}', 500)

