from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django import forms
from .models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            User.objects.get(username=self._user)
        except User.DoesNotExist:
            raise forms.ValidationError(u'Access is limited!')

        self.cleaned_data = super(AskForm, self).clean()
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        if not title or not text:
            raise forms.ValidationError(u'Validation Error!')

        return self.cleaned_data

    def save(self):
        self.cleaned_data['author'] = self._user
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

        try:
            User.objects.get(username=self._user)
        except User.DoesNotExist:
            raise forms.ValidationError(u'Access is limited!')

        return self.cleaned_data

    def save(self):
        self.cleaned_data['author'] = self._user
        self.cleaned_data['question'] = get_object_or_404(
            Question,
            pk=self.cleaned_data['question']
        )
        answer = Answer(**self.cleaned_data)
        answer.save()

        return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self._username = self.cleaned_data['username']
        self._email = self.cleaned_data['email']
        self._password = self.cleaned_data['password']

    def clean(self):
        if not self._sername:
            raise forms.ValidationError(u'Please enter a username')
        if not self._email:
            raise forms.ValidationError(u'Please enter a email')
        if not self._password:
            raise forms.ValidationError(u'Please enter a password')

        return self.cleaned_data

    def save(self):
        # try:
        #     User.objects.get(username=username)
        # except User.DoesNotExist:
        #     raise forms.ValidationError(u'User is in database')
        try:
            user = User.objects.create(username=self._username,
                                       email=self._email,
                                       password=self._password)
        except User.DoesNotExist:
            raise forms.ValidationError(u'Ooops...')
        self.cleaned_data['user'] = user

        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not username:
            raise forms.ValidationError(u'Please enter a username')
        if not password:
            raise forms.ValidationError(u'Please enter a password')

        return self.cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(u'User does not in database')
        self.cleaned_data['user'] = user

        return self.cleaned_data
