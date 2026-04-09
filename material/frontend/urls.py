from django.urls import include, re_path
from . import modules


urlpatterns = [
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'', include(modules.urls)),
]
