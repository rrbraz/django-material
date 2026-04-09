from django.urls import re_path, include
from django.views import generic

from . import views

urlpatterns = [
    re_path('^$', generic.RedirectView.as_view(url='./city/'), name="index"),
    re_path('^city/', include(views.CityViewSet().urls)),
    re_path('^continent/', include(views.ContinentViewSet().urls)),
    re_path('^country/', include(views.CountryViewSet().urls)),
    re_path('^ocean/', include(views.OceanViewSet().urls)),
    re_path('^sea/', include(views.SeaViewSet().urls)),
]
