from django.core.mail import send_mail

message = '''
Добрый день!
Недавно вы интересовались нашим роботом модели {}, версии {}. 
Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
'''

COMPANY_EMAIL = "from@example.com"


def send_email(robot_model: str, robot_version: str, customer_email: str):
    send_mail(
        "Мы собрали робота для вас!",
        message.format(robot_model, robot_version),
        COMPANY_EMAIL,
        [customer_email],
    )
