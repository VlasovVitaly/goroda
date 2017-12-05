from django.conf.urls import url

from . import views

app_name = 'game'

urlpatterns = [
    url(r'^start[/]+$', views.start_new_match, name='start'),
]
