from django.urls import re_path
from django.views import generic

from . import views


urlpatterns = [
    re_path('^$', generic.RedirectView.as_view(url='./customers/', permanent=False), name="index"),
    re_path('^customers/$', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="leads"),
    re_path('^leads/$', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="leads"),
    re_path('^opportunities/$', generic.TemplateView.as_view(template_name="sales/index.html"),
        name="opportunities"),
    re_path('^shipment/new/$', views.NewShipmentView.as_view(template_name="sales/form.html"),
        name="shipment_new"),
]
