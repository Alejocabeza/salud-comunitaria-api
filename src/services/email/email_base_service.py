from fastapi_mail import FastMail, MessageSchema, MessageType
from ...config.email import emailConfig
from fastapi import BackgroundTasks
import asyncio


class EmailBaseService:
    def __init__(self, subject, recipients, body):
        self.subject = subject
        self.recipients = recipients
        self.body = body

    async def send_email_async(self):
        """
        Send email asynchronously
        
        Returns:
            dict: Response indicating email status
        """
        message = MessageSchema(
            subject=self.subject,
            recipients=self.recipients,
            body=self.body,
            subtype=MessageType.html,
        )

        fm = FastMail(emailConfig)
        await fm.send_message(message)
        
        return {"message": "Email sent successfully", "status": "success"}

    def send_email(self):
        """
        Send email synchronously (for backward compatibility)
        
        Returns:
            dict: Response indicating email status
        """
        try:
            # Run the async function in a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.send_email_async())
            loop.close()
            return result
        except Exception as e:
            return {"message": f"Error sending email: {str(e)}", "status": "error"} 