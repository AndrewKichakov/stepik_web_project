from django.shortcuts import get_object_or_404

from django import forms
from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data = super(AskForm, self).clean()
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        if (not title) or not text:
            raise forms.ValidationError(u'Validation Error!')

        return self.cleaned_data

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()

        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        text = self.cleaned_data['text']
        if 'spam' in text:
            raise forms.ValidationError(u'Validation Error!')

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(
            Question,
            pk=self.cleaned_data['question']
        )
        answer = Answer(**self.cleaned_data)
        answer.save()

        return answer
