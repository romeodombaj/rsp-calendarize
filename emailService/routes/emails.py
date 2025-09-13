from fastapi import APIRouter, HTTPException
from db import email_log_table
from uuid import uuid4
from models import InputEmailSend, EmailLog
from datetime import datetime
import aiohttp

import os
from dotenv import load_dotenv
load_dotenv()



router = APIRouter(prefix="/emails", tags=["emails"])

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

@router.post("/send")
async def send_email(emailData: InputEmailSend):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{USER_SERVICE_URL}/users/{emailData.user_id}") as response:
                response.raise_for_status()
                user = await response.json()

                if not user:
                    raise HTTPException(status_code=404, detail=str(e))  


        email_id = str(uuid4())
        email = user.get("email")  

        #SIMULACIJA slanja
        print("Email Sent Successfully")
        print(f"To email: {email}")
        print(f"Message: {emailData.body}")
        print(f"Email Id: {email_id}")
        

        log_id = str(uuid4())

        log_row = EmailLog(
            id = log_id,
            email_id = email_id,
            status = "sent",
            email = email ,
            referenceId = emailData.referenceId,
            referenceType = emailData.referenceType,
            createdAt = datetime.now()
        )

        log_dict = log_row.model_dump()
        log_dict["createdAt"] = log_row.createdAt.isoformat() 

        email_log_table.put_item(Item=log_dict)    
        
        return

    except Exception as e:
        print(e)
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))



