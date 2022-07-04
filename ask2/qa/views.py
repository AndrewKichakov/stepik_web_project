from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator

from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm, LoginForm, SignupForm


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def index(request):
    try:
        page = int(request.GET.get('page'))
    except ValueError:
        page = 1
    except TypeError:
        page = 1

    questions = Question.objects.new()
    paginator = Paginator(questions, 10)
    page = paginator.page(page)

    return render(request, 'index.html',
                  {'title': 'Latest',
                   'paginator': paginator,
                   'questions': page.object_list,
                   'page': page,
                   'user': request.user,
                   'session': request.session, })


def popular(request):
    try:
        page = int(request.GET.get('page'))
    except ValueError:
        page = 1
    except TypeError:
        page = 1

    questions = Question.objects.popular()
    paginator = Paginator(questions, 10)
    page = paginator.page(page)

    return render(request, 'index.html',
                  {'title': 'Popular',
                   'paginator': paginator,
                   'questions': page.object_list,
                   'page': page,
                   'user': request.user,
                   'session': request.session, })


def question(request, r_id):
    try:
        q = Question.objects.get(id=r_id)
    except Question.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            _ = form.save()
            url = q.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': q.id})

    return render(request, 'question.html', {'question': q,
                                             'form': form,
                                             'user': request.user,
                                             'session': request.session, })
