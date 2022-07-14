from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

from .forms import AnswerForm, AskForm
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
            form = AnswerForm(request.POST, initial={'question': question.id})
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
        if form.is_valid():
            question = form.save()
            url = question.get_url()

            return HttpResponseRedirect(url)
    else:
        form = AskForm()

    return render(request, 'qa/ask.html', {'form': form})
