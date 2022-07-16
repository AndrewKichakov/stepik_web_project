import base64

from django.contrib.auth import login, logout
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

from .forms import AnswerForm, AskForm, LoginForm, SignupForm
from .models import Question, Answer


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def paginate(request, qs, baseurl='/'):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10

    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, limit)
    paginator.baseurl = baseurl

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator(paginator.num_pages)

    return page, paginator


def index(request):
    print(request.user)
    try:
        new_questions = Question.objects.new()
    except Question.DoesNotExist:
        raise Http404
    page, paginator = paginate(request, new_questions, '/?page=')

    return render(request, 'qa/index.html', {'page': page,
                                             'paginator': paginator,
                                             'questions': page.object_list})


def popular(request):
    try:
        popular_questions = Question.objects.popular()
    except Question.DoesNotExist:
        raise Http404
    page, paginator = paginate(request, popular_questions, '/popular/?page=')

    return render(request, 'qa/popular.html', {'page': page,
                                               'paginator': paginator,
                                               'questions': page.object_list})


def question(request, id):
    if id:
        try:
            question = Question.objects.get(pk=id)
        except Question.DoesNotExist:
            raise Http404

        try:
            answers = Answer.objects.filter(question=question)
        except Answer.DoesNotExist:
            raise Http404

        if request.method == 'POST':
            form = AnswerForm(request.POST,
                              initial={'question': question.id})
            form._user = request.user
            if form.is_valid():
                question = form.save()
        else:
            form = AnswerForm(initial={'question': question.id})

        return render(request, 'qa/question.html', {'question': question,
                                                    'answers': answers,
                                                    'form': form})

    return Http404


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            question = form.save()
            url = question.get_url()

            return HttpResponseRedirect(url)
    else:
        form = AskForm()

    return render(request, 'qa/ask.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.cleaned_data['user']
            login(request, user)

            return do_sessionid(username, password)
    else:
        form = LoginForm()

    return render(request, 'qa/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.cleaned_data['user']
            login(request, user)

            return do_sessionid(username, password)
    else:
        form = SignupForm()

    return render(request, 'qa/signup.html', {'form': form})


def do_sessionid(username, password):
    sessionid = base64.b64encode(username+password)
    if sessionid:
        response = HttpResponseRedirect('/')
        response.set_cookie('sessionid', sessionid)

        return response


def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/')
