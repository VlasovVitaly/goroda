from django.conf import settings
from django.conf.urls import url
from django.contrib import admin

from .views import login, logout_then_login


urlpatterns = [
    url(r'^login/$', login.as_view(), name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
