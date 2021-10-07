from django.core.mail import message, send_mail
import uuid
from django.conf import settings
def send_forgot_password_mail(email,token):
    
    subject="Your Forget Password Link"
    message=f'Hi ,Click on the link to reset your Password  http://127.0.0.1:8000/changepassword/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True