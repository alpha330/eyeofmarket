from celery import Celery
from mail_templated import EmailMessage
from django.core.mail import send_mail

# TASKS FOR CELERY TO SEND BROOKER REDIS
app = Celery('accounts.tasks', broker='redis://redis-emarket:6379/1')

@app.task
def sendEmail(template,context,from_email,recipient_list):
    task_email = EmailMessage(
            template,
            context,
            from_email,
            recipient_list,
            
        )
    return task_email.send()