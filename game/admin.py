from django.contrib import admin

from .models import City, Match, Turn


admin.site.register(City)
admin.site.register(Match)
admin.site.register(Turn)
