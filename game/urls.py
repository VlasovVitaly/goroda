from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('start/', views.start_new_match, name='start'),
    path('<int:match_id>/detail', views.match_detail, name='detail'),
]
