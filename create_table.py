import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

def create_dynamodb_table():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
    )
    
    try:
        table = dynamodb.create_table(
            TableName=os.getenv('DYNAMODB_TABLE'),
            KeySchema=[
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Creating table... Please wait.")
        table.meta.client.get_waiter('table_exists').wait(TableName=os.getenv('DYNAMODB_TABLE'))
        print("Table created successfully!")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists!")
        else:
            print(f"Error creating table: {e}")
            raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

if __name__ == '__main__':
    create_dynamodb_table()
