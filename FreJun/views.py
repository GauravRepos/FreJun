from django.http import JsonResponse
from django.http.response import HttpResponse


def index(request):
    context = '{"response": "Server is running"}'
    return HttpResponse(context)

def health(request):
    context = '{"response": "I am 0K"}'
    return HttpResponse(context)

