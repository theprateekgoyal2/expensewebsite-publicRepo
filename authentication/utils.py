from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.core.mail import EmailMessage
import threading

# Define an email sending function

# These works in development! 
# def send_verification_mail(email, email_body):
#     subject = "Activate your account"
#     message = email_body
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     print(recipient_list)
#     # Send the email using a separate thread
#     email_thread = threading.Thread(target=send_mail, args=(subject, message, from_email, recipient_list))
#     email_thread.start()
#     print(email)
#     print("Email sent")

# def send_reset_link(email, email_body):
#     subject = "Password reset instructions"
#     message = email_body
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]

#     # Send the email using a separate thread
#     email_thread = threading.Thread(target=send_mail, args=(subject, message, from_email, recipient_list))
#     email_thread.start()

#     print("Email sent")


# These works in the production
def send_verification_mail(email, email_body):
    subject = "Activate your account"
    message = email_body
    print("sending email")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    print("email sent")

def send_reset_link(email, email_body):
    subject = "Password reset instructions"
    message = email_body
    print("sending email")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    print("email sent")

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))
    
token_generator=AppTokenGenerator()