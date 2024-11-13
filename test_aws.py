import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def test_aws_connection():
    try:
        # Test DynamoDB connection
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )
        
        table = dynamodb.Table(os.getenv('DYNAMODB_TABLE'))
        table.put_item(
            Item={
                'timestamp': 'test_timestamp',
                'test_data': 'connection successful'
            }
        )
        
        # Read test item
        response = table.get_item(
            Key={
                'timestamp': 'test_timestamp'
            }
        )
        
        if response.get('Item'):
            print("AWS Connection Test: SUCCESS")
            print("DynamoDB table is accessible and working")
            
            # Clean up test item
            table.delete_item(
                Key={
                    'timestamp': 'test_timestamp'
                }
            )
        
    except Exception as e:
        print("AWS Connection Test: FAILED")
        print(f"Error: {e}")

if __name__ == '__main__':
    test_aws_connection()
