from django.urls import path, include
from django.contrib import admin

from .views import login, logout_then_login
from game.views import start_page


urlpatterns = [
    path('', start_page, name='index'),
    path('login/', login.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('admin/', admin.site.urls),
    path('game/', include('game.urls', namespace='game')),
]
