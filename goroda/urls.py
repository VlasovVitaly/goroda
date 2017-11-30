from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from .views import login, logout_then_login
from game.views import start_page


urlpatterns = [
    url(r'^$', start_page, name='index'),
    url(r'^login/$', login.as_view(), name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^game/', include('game.urls', namespace='game')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
