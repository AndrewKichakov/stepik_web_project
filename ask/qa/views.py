from django.http import HttpResponse
from django.shortcuts import render


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def index(request):
    return render(request, 'qa/index.html')
