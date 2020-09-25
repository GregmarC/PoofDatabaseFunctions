import json
import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

#Boto3 DynamoDB CLIENT and NOT Table Resource (caused confusion )
def get_featured_item(keyword):
    response = dynamodb.scan(
        TableName="featured_items",
        FilterExpression="contains(keywords, :keyword)",
        ExpressionAttributeValues={
            ":keyword": {"S": f'{keyword}'}
        }
    )
    print(response)

    
def format_response(text,code):
    return {
        'statusCode': code,
        'body': json.dumps(text)
    }
    
    
def lambda_handler(event, context):
    try:
        #somehow the body is an
        if isinstance(event["body"],str):
            event["body"] = json.loads(event["body"])
            
        keyword = event.get("body", {}).get("keyword", None)
        if keyword is not None:
            print(f'The keyword entered: {keyword}')
            get_featured_item(keyword)
            return format_response("Success", 200)
                
                
    except Exception as e:
        print(str(e))
        return format_response(f'Failed with error {str(e)}', 500)