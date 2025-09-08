import boto3

dydb = boto3.resource(
    'dynamodb',
    endpoint_url="http://localhost:8000", 
    region_name="us-east-1",               
    aws_access_key_id="key",       
    aws_secret_access_key="key"  
)


booking_table = dydb.Table("bookings")


