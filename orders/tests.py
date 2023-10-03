from django.core import mail
from django.test import TestCase
from django.utils import timezone

from customers.models import Customer
from orders.models import Order
from robots.models import Robot


# Create your tests here.

class EmailTest(TestCase):
    def test_send_email_to_customer(self):
        customer_1 = Customer.objects.create(email='customer_1@example.com')
        customer_2 = Customer.objects.create(email='customer_2@example.com')

        Order.objects.create(robot_serial='R2-D2', customer_id=customer_1.id)
        Order.objects.create(robot_serial='13-XS', customer_id=customer_2.id)

        robot = Robot.objects.create(model='R2', version='D2', serial='R2-D2', created=timezone.now())

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the body of the message contains right data.
        self.assertIn(robot.model, mail.outbox[0].body)
        self.assertIn(robot.version, mail.outbox[0].body)

        # Verify right reciever email
        self.assertEqual(mail.outbox[0].to[0], customer_1.email)

    def test_no_send(self):
        customer_1 = Customer.objects.create(email='customer_1@example.com')
        customer_2 = Customer.objects.create(email='customer_2@example.com')

        Order.objects.create(robot_serial='R2-D2', customer_id=customer_1.id)
        Order.objects.create(robot_serial='13-XS', customer_id=customer_2.id)

        robot = Robot.objects.create(model='DR', version='DJ', serial='DR-DJ', created=timezone.now())

        # Test that no message has been sent.
        self.assertEqual(len(mail.outbox), 0)
