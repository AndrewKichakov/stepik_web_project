from django.urls import path
from qa.views import test, index, popular, question


urlpatterns = [
    path('', index, name='index'),
    path('login/', test, name='login'),
    path('signup/', test, name='signup'),
    path('question/<int:id>/', question, name='question'),
    path('ask/', test, name='ask'),
    path('popular/', popular, name='popular'),
    path('new/', test, name='new'),
]
