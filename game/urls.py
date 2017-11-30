from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^start[/]+$', views.start_new_match, name='start'),
]
