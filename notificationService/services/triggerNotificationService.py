from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from db import notifications_table
import aiohttp
from boto3.dynamodb.conditions import Attr

load_dotenv()

EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL")

async def check_and_send_notifications():
    now = datetime.now(timezone.utc).isoformat()

    response = notifications_table.scan(
        FilterExpression=Attr("status").eq("scheduled") & Attr("run_time").lte(now)
    )

    for item in response.get('Items', []):

        user_id = item.get("user_id")
        id = item.get("id")

        emailData = {
            "user_id": user_id,
            "body": "Hello user, your appointment is in an hour",
            "referenceId": id,
            "referenceType": "notification"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{EMAIL_SERVICE_URL}/emails/send", json=emailData) as response:
                    response.raise_for_status()

        
            notifications_table.update_item(
                Key={'id': item['id']},
                UpdateExpression="SET #st = :val",
                ExpressionAttributeNames={
                    "#st": "status"
                },
                ExpressionAttributeValues={
                    ":val": "finished"
                }
            )

        except Exception as e:
            print(e)
