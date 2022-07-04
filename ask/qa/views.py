from django.http import HttpResponse, HttpResponseNotFound


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def not_found(request):
    return HttpResponseNotFound('Not Found!')
