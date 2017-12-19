from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('start/', views.start_new_match, name='start'),
    path('<int:match_id>/detail', views.match_detail, name='detail'),
    path('<int:match_id>/end', views.end_match, name='end'),
]
