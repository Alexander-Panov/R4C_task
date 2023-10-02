import json

from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from robots.models import Robot


# Create your views here.
@csrf_exempt
def APIView(request):
    if request.method == "GET":
        data = serializers.serialize("json", Robot.objects.all())
        return JsonResponse(json.loads(data), safe=False)

    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        serial = f"{body['model']}-{body['version']}"
        newrecord = Robot(**body, serial=serial)
        try:  # validation
            newrecord.full_clean()
        except ValidationError as exception:
            return JsonResponse({'error': 'Data validation failed', 'message': exception.message_dict}, status=400)
        else:
            newrecord.save()
            data = json.loads(serializers.serialize('json', [newrecord]))
            return JsonResponse(data, safe=False)


