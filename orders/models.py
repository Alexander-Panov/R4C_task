from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import Customer
from orders.views import send_email
from robots.models import Robot


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)


# triggred when Robot object is created
@receiver(post_save, sender=Robot)
def new_robot_created(sender, instance: Robot, created: bool, **kwargs):
    if created:
        order = Order.objects.filter(robot_serial=instance.serial).last()
        # There is no order for this robot_serial
        if not order:
            return

        send_email(instance.model, instance.version, order.customer.email)

        # ... Some actions ...

        # Clear database
        order.delete()
        instance.delete()
