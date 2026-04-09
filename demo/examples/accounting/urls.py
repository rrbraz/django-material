from django.urls import re_path
from django.views import generic


urlpatterns = [
    re_path('^$', generic.TemplateView.as_view(template_name="accounting/index.html"), name="index"),
]
