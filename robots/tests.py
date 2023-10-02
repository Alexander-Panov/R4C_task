import datetime
import json

from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from robots.models import Robot
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime


# Create your tests here.
class RobotAPITest(TestCase):
    def test_post_valide_data(self):
        input_data = [{"model": "R2", "version": "D2", "created": "2022-12-31 23:59:59"},
                      {"model": "13", "version": "XS", "created": "2023-01-01 00:00:00"},
                      {"model": "X5", "version": "LT", "created": "2023-01-01 00:00:01"}, ]

        for i, data in enumerate(input_data, 1):
            response = self.client.post(reverse("robots:api"), json.dumps(data), content_type="application/json")
            self.assertEquals(response.status_code, 200)

            robot_data = {"id": i,
                          "serial": f"{data['model']}-{data['version']}",
                          **data,
                          "created": make_aware(parse_datetime(data['created']))
                          }

            robot_from_db = Robot.objects.get(pk=i)
            self.assertDictEqual(model_to_dict(robot_from_db), robot_data)

    def test_post_invalide_data(self):
        corrupt_data = {"model": "R22", "version": "D2", "created": "2022-12-31 23:59:59"}
        error_json = '''
        {
            "error": "Data validation failed",
            "message": {
                "serial": [
                    "Ensure this value has at most 5 characters (it has 6)."
                ],
                "model": [
                    "Ensure this value has at most 2 characters (it has 3)."
                ]
            }
        }
        '''

        response = self.client.post(reverse("robots:api"), json.dumps(corrupt_data), content_type="application/json")
        self.assertEquals(response.status_code, 400)
        self.assertJSONEqual(response.content.decode("utf-8"), error_json)
