
############## FOR EMAIL #############################################
from django.core.mail import send_mail


def mailIt(body, to_email = "jalanikshit1@gmail.com", title = "CHEFFY"):
    send_mail(title, body, 'dummydjango1@gmail.com', [to_email])
#######################################################################
