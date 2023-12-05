from django.conf import settings
from django.core.mail import send_mail, EmailMessage



def send_account_activation_mail(email, email_token):
    subject = "Your account needs to be verified."
    from_email = settings.EMAIL_HOST_USER
    message = f"Click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}"
    
    send_mail(subject, message, from_email, [email])


def send_order_mail(email, invoice_path):
    subject = "Order Confirmation"
    from_email = settings.EMAIL_HOST_USER
    message = f"Your order has been placed successfuly.\nPlease check attechment of your order invoice"

    print('EMAIL OBJECT CREATE')
    email_send = EmailMessage(subject, message, from_email, [email])
    email_send.attach_file(invoice_path)
    email_send.send()
    print('EMAIL HAS BEEN SENT')