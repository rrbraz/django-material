from django.urls import re_path, include
from django.views import generic

from . import views


urlpatterns = [
    re_path('^$', generic.RedirectView.as_view(
        url='./departments/'), name="index"),
    re_path('^departments/', include(views.DepartmentViewSet().urls)),
    re_path('^employees/', include(views.EmployeeViewSet().urls)),
]
