from django.http import JsonResponse
from .models import Resource


def index(request):
    resources_list = []
    resources = Resource.objects.all()

    for resource in resources:
        data = {
            "url": resource.url,
            "description": resource.description,
        }
        resources_list.append(data)

    return JsonResponse(resources_list, safe=False)
