from celery import shared_task

@shared_task
def send_email(email_object, *args, **kwargs):
    print(email_object)
    # return "SENT"

# send_email.delay("This is a test email", *args, **kwargs)