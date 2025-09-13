import boto3
import os
from dotenv import load_dotenv
load_dotenv()

dydb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("DB_URL"), 
    region_name="us-east-1",               
    aws_access_key_id="key",       
    aws_secret_access_key="key"  
)


notifications_table = dydb.Table("notifications")


