from django.conf import settings
from django.urls import include, re_path
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.shortcuts import render
from django.views import generic, static

try:
    import debug_toolbar
except ImportError:
    debug_toolbar = None

from formtools.wizard.views import SessionWizardView
from material.frontend import urls as frontend_urls

from . import forms, widget_forms, admin_forms


def index_view(request):
    context = {
        'login': forms.LoginForm(),
        'registration': forms.RegistrationForm(),
        'checkout': forms.CheckoutForm(),
        'order': forms.OrderForm(),
        'comment': forms.CommentForm(),
        'bank': forms.BankForm(),
    }
    return render(request, 'index.html', context)


class Wizard(SessionWizardView):
    form_list = [forms.WizardForm1, forms.WizardForm2]

    def done(self, form_list, **kwargs):
        return render(self.request, 'formtools/wizard/wizard_done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })


class WidgetFormView(generic.FormView):
    template_name = 'widgets_demo.html'

    def form_valid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


class AdminFormView(generic.FormView):
    template_name = 'admin_demo.html'

    @classmethod
    def as_view(cls, *args, **kwargs):
        return login_required(super().as_view(*args, **kwargs))

    def form_valid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


urlpatterns = [
    re_path(r'^$', index_view),

    # demo
    re_path(r'^demo/login/$', generic.FormView.as_view(
        form_class=forms.LoginForm, success_url='/demo/login/', template_name="demo.html")),
    re_path(r'^demo/registration/$', generic.FormView.as_view(
        form_class=forms.RegistrationForm, success_url='/demo/registration/', template_name="demo.html")),
    re_path(r'^demo/contact/$', generic.FormView.as_view(
        form_class=forms.ContactForm, success_url='/demo/contact/', template_name="demo.html")),
    re_path(r'^demo/order/$', generic.FormView.as_view(
        form_class=forms.OrderForm, success_url='/demo/order/', template_name="demo.html")),
    re_path(r'^demo/checkout/$', generic.FormView.as_view(
        form_class=forms.CheckoutForm, success_url='/demo/checkout/', template_name="demo.html")),
    re_path(r'^demo/comment/$', generic.FormView.as_view(
        form_class=forms.CommentForm, success_url='/demo/comment/', template_name="demo.html")),
    re_path(r'^demo/bank/$', generic.FormView.as_view(
        form_class=forms.BankForm, success_url='/demo/bank/', template_name="demo.html")),
    re_path(r'^demo/wizard/$', Wizard.as_view()),
    re_path(r'^foundation/basic/', generic.RedirectView.as_view(url='/?cache=no', permanent=False)),

    # core widgets test
    re_path(r'^demo/widget/$', generic.RedirectView.as_view(url='/demo/widget/boolean/', permanent=False)),
    re_path(r'^demo/widget/boolean/$', WidgetFormView.as_view(form_class=widget_forms.BooleanFieldForm)),
    re_path(r'^demo/widget/char/$', WidgetFormView.as_view(form_class=widget_forms.CharFieldForm)),
    re_path(r'^demo/widget/choice/$', WidgetFormView.as_view(form_class=widget_forms.ChoiceFieldForm)),
    re_path(r'^demo/widget/date/$', WidgetFormView.as_view(form_class=widget_forms.DateFieldForm)),
    re_path(r'^demo/widget/datetime/$', WidgetFormView.as_view(form_class=widget_forms.DateTimeFieldForm)),
    re_path(r'^demo/widget/decimal/$', WidgetFormView.as_view(form_class=widget_forms.DecimalFieldForm)),
    re_path(r'^demo/widget/duration/$', WidgetFormView.as_view(form_class=widget_forms.DurationFieldForm)),
    re_path(r'^demo/widget/email/$', WidgetFormView.as_view(form_class=widget_forms.EmailFieldForm)),
    re_path(r'^demo/widget/file/$', WidgetFormView.as_view(form_class=widget_forms.FileFieldForm)),
    re_path(r'^demo/widget/filepath/$', WidgetFormView.as_view(form_class=widget_forms.FilePathFieldForm)),
    re_path(r'^demo/widget/float/$', WidgetFormView.as_view(form_class=widget_forms.FloatFieldForm)),
    re_path(r'^demo/widget/image/$', WidgetFormView.as_view(form_class=widget_forms.ImageFieldForm)),
    re_path(r'^demo/widget/integer/$', WidgetFormView.as_view(form_class=widget_forms.IntegerFieldForm)),
    re_path(r'^demo/widget/ipaddress/$', WidgetFormView.as_view(form_class=widget_forms.GenericIPAddressFieldForm)),
    re_path(r'^demo/widget/multiplechoice/$', WidgetFormView.as_view(form_class=widget_forms.MultipleChoiceFieldForm)),
    re_path(r'^demo/widget/nullbolean/$', WidgetFormView.as_view(form_class=widget_forms.NullBooleanFieldForm)),
    re_path(r'^demo/widget/regex/$', WidgetFormView.as_view(form_class=widget_forms.RegexFieldForm)),
    re_path(r'^demo/widget/slug/$', WidgetFormView.as_view(form_class=widget_forms.SlugFieldForm)),
    re_path(r'^demo/widget/time/$', WidgetFormView.as_view(form_class=widget_forms.TimeFieldForm)),
    re_path(r'^demo/widget/url/$', WidgetFormView.as_view(form_class=widget_forms.URLFieldForm)),
    re_path(r'^demo/widget/uuid/$', WidgetFormView.as_view(form_class=widget_forms.UUIDField)),
    re_path(r'^demo/widget/combo/$', WidgetFormView.as_view(form_class=widget_forms.ComboFieldForm)),
    re_path(r'^demo/widget/splitdatetime/$', WidgetFormView.as_view(form_class=widget_forms.SplitDateTimeFieldForm)),
    re_path(r'^demo/widget/modelchoice/$', WidgetFormView.as_view(form_class=widget_forms.ModelChoiceFieldForm)),
    re_path(r'^demo/widget/modelmultichoice/$', WidgetFormView.as_view(form_class=widget_forms.ModelMultipleChoiceFieldForm)),

    re_path(r'^demo/widget/password/$', WidgetFormView.as_view(form_class=widget_forms.PasswordInputForm)),
    re_path(r'^demo/widget/hidden/$', WidgetFormView.as_view(form_class=widget_forms.HiddenInputForm)),
    re_path(r'^demo/widget/textarea/$', WidgetFormView.as_view(form_class=widget_forms.TextareaForm)),
    re_path(r'^demo/widget/radioselect/$', WidgetFormView.as_view(form_class=widget_forms.RadioSelectForm)),
    re_path(r'^demo/widget/checkboxmultiple/$', WidgetFormView.as_view(
        form_class=widget_forms.CheckboxSelectMultipleForm)),
    re_path(r'^demo/widget/fileinput/$', WidgetFormView.as_view(form_class=widget_forms.FileInputForm)),
    re_path(r'^demo/widget/splithiddendatetime/$', WidgetFormView.as_view(
        form_class=widget_forms.SplitHiddenDateTimeWidgetForm)),
    re_path(r'^demo/widget/selectdate/$', WidgetFormView.as_view(form_class=widget_forms.SelectDateWidgetForm)),

    # admin widgets test
    re_path(r'^demo/widget/admin/$', generic.RedirectView.as_view(
        url='/demo/widget/admin/filteredselectmultiple/', permanent=False)),
    re_path(r'^demo/widget/admin/filteredselectmultiple/$', AdminFormView.as_view(
        form_class=admin_forms.FilteredSelectMultipleForm)),
    re_path(r'^demo/widget/admin/admindatewidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminDateWidgetForm)),
    re_path(r'^demo/widget/admin/admintimewidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminTimeWidgetForm)),
    re_path(r'^demo/widget/admin/adminsplitdatetime/$', AdminFormView.as_view(
        form_class=admin_forms.AdminSplitDateTimeForm)),
    re_path(r'^demo/widget/admin/adminradioselect/$', AdminFormView.as_view(
        form_class=admin_forms.AdminRadioSelectForm)),
    re_path(r'^demo/widget/admin/adminfilewidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminFileWidgetForm)),
    re_path(r'^demo/widget/admin/foreignkeyrawidwidget/$', AdminFormView.as_view(
        form_class=admin_forms.ForeignKeyRawIdWidgetForm)),
    re_path(r'^demo/widget/admin/manytomanyrawidwidget/$', AdminFormView.as_view(
        form_class=admin_forms.ManyToManyRawIdWidgetForm)),
    re_path(r'^demo/widget/admin/relatedfieldwidgetwrapper/$', AdminFormView.as_view(
        form_class=admin_forms.RelatedFieldWidgetWrapperForm)),
    re_path(r'^demo/widget/admin/admintextareawidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminTextareaWidgetForm)),
    re_path(r'^demo/widget/admin/admintextinputwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminTextInputWidgetForm)),
    re_path(r'^demo/widget/admin/adminemailfield/$', AdminFormView.as_view(
        form_class=admin_forms.AdminEmailFieldForm)),
    re_path(r'^demo/widget/admin/adminurlfieldwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminURLFieldWidgetForm)),
    re_path(r'^demo/widget/admin/adminintegerfieldwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminIntegerFieldWidgetForm)),
    re_path(r'^demo/widget/admin/adminbigintegerfieldwidget/$', AdminFormView.as_view(
        form_class=admin_forms.AdminBigIntegerFieldWidgetForm)),

    # frontend
    re_path(r'^frontend/$', generic.RedirectView.as_view(url='/frontend/accounting/', permanent=False), name="index"),
    re_path(r'', include(frontend_urls)),
]

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
]

if 'material.frontend' not in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r'^admin/', admin.site.urls)]

if debug_toolbar:
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]

if 'django.contrib.flatpages' in settings.INSTALLED_APPS:
    from django.contrib.flatpages import views
    urlpatterns += [re_path(r'^(?P<url>.*/)$', views.flatpage)]
