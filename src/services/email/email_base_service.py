from fastapi_mail import FastMail, MessageSchema
from ...config.email import emailConfig
from fastapi import BackgroundTasks


class EmailBaseService:
    def __init__(self, subject, recipients, body):
        self.subject = subject
        self.recipients = recipients
        self.body = body

    def send_email(self):
        message = MessageSchema(
            subject=self.subject,
            recipients=self.recipients,
            body=self.body,
            subtype="html",
        )

        fm = FastMail(emailConfig)

        background_tasks = BackgroundTasks()
        background_tasks.add_task(fm.send_message, message)

        return {"message": "Email sent successfully", "status": "success"}
