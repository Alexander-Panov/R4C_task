import random
from faker import Faker
from robots.models import Robot

"""
Generate random data for database
"""

fake = Faker()
models = ('R2', 'K9', '15', 'DJ', 'LA')
versions = ('XS', 'XL', 'D2', 'SD', 'NY')
for i in range(100):
    model = random.choice(models)
    version = random.choice(versions)
    serial = f"{model}-{version}"
    date = fake.date_time_between(start_date='-2w', end_date='now')
    Robot.objects.create(serial=serial, model=model, version=version, created=date)