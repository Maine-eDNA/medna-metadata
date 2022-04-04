import django
from django.db.models import F, BLANK_CHOICE_DASH
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.template.response import SimpleTemplateResponse
from django.http import JsonResponse
from django.utils import timezone
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_str as force_text
import json
import sys
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ContactUs, ProcessLocation, Publication, StandardOperatingProcedure, Project, Grant, DefaultSiteCss, CustomUserCss
from .forms import ContactUsForm, ContactUsUpdateForm, PublicationForm, StandardOperatingProcedureForm
from .charts import return_select2_options
import utility.enumerations as utility_enums
import utility.serializers as utility_serializers
import utility.filters as utility_filters
from utility.forms import export_action_form_factory


# Create your views here.
########################################
# UTILITY DEFS                         #
########################################
def get_action_choices(default_choices=BLANK_CHOICE_DASH):
    # Return a list of choices for use in a form object.  Each choice is a
    # tuple (name, description).
    choices = [('export_action_select', 'Export selected'),
               ('export_action_table', 'Export table'), ] + default_choices
    return choices


def export_context(request, export_formats):
    # Return a dictionary of variables to put in the template context for
    # pages with exportable tables
    # export_formats = ['csv', 'xlsx']
    actions_selection_counter = True
    formats = []
    if export_formats:
        formats.append(('', '---'))
        for i, f in enumerate(export_formats):
            formats.append((f, f))
    export_action_form = export_action_form_factory(formats)

    # Build the action form and populate it with available actions.
    action_form = export_action_form(auto_id=None)
    action_form.fields['action'].choices = get_action_choices()

    return {
        'actions_selection_counter': actions_selection_counter,
        # 'format_form':format_form,
        'action_form': action_form,
    }


class BasePopupMixin(object):
    # Copyright (c) 2015 Jonas Haag <jonas@lophus.org>, James Pic <jamespic@gmail.com>.
    # Base mixin for generic views classes that handles the case of the view
    # being opened in a popup window.
    # Don't call this directly, use some of the subclasses instead.
    # .. versionadded:: 2.0.0
    #   Factored from the original ``PopupMixin`` class.
    def is_popup(self):
        return self.request.GET.get(IS_POPUP_VAR, False)

    def form_valid(self, form):
        if self.is_popup():
            # If this view is only used with addanother, never as a standalone,
            # then the user may not have set a success url, which causes an
            # ImproperlyConfigured error. (We never use the success url for the
            # addanother popup case anyways, since we always directly close the
            # popup window.)
            self.success_url = '/'
        response = super(BasePopupMixin, self).form_valid(form)
        if self.is_popup():
            return self.respond_script(self.object)
        else:
            return response

    def respond_script(self, created_obj):
        ctx = {
            'action': self.POPUP_ACTION,
            'value': str(self._get_created_obj_pk(created_obj)),
            'obj': str(self.label_from_instance(created_obj)),
            'new_value': str(self._get_created_obj_pk(created_obj))
        }
        if django.VERSION >= (1, 10):
            ctx = {'popup_response_data': json.dumps(ctx)}
        return SimpleTemplateResponse('admin/popup_response.html', ctx)

    def _get_created_obj_pk(self, created_obj):
        pk_name = created_obj._meta.pk.attname
        return created_obj.serializable_value(pk_name)

    def label_from_instance(self, related_instance):
        # Copyright (c) 2015 Jonas Haag <jonas@lophus.org>, James Pic <jamespic@gmail.com>.
        # Return the label to show in the 'main form' for the
        # newly created object.
        # Overwrite this to customize the label that is being shown.
        return force_text(related_instance)


class CreatePopupMixin(BasePopupMixin):
    # Copyright (c) 2015 Jonas Haag <jonas@lophus.org>, James Pic <jamespic@gmail.com>.
    # Mixin for :class:`~django.views.generic.edit.CreateView` classes that
    # handles the case of the view being opened in an add-another popup window.
    # .. versionchanged:: 2.0.0
    #    This used to be called ``PopupMixin`` and has been renamed with the
    #    introduction of edit-related buttons and :class:`UpdatePopupMixin`.
    POPUP_ACTION = 'add'


class UpdatePopupMixin(BasePopupMixin):
    # Copyright (c) 2015 Jonas Haag <jonas@lophus.org>, James Pic <jamespic@gmail.com>.
    # Mixin for :class:`~django.views.generic.edit.UpdateView` classes that
    # handles the case of the view being opened in an edit-related popup window.
    # .. versionadded:: 2.0.0
    POPUP_ACTION = 'change'


########################################
# FRONTEND REQUESTS                    #
########################################
@login_required(login_url='dashboard_login')
def get_project_options(request):
    grant = request.GET.get('id')
    qs = Project.objects.filter(grant_names=grant).order_by('project_label').annotate(text=F('project_label'))
    qs_json = return_select2_options(qs)
    return JsonResponse(data={'results': qs_json})


@login_required(login_url='dashboard_login')
def contact_us_list(request):
    contactus_list = ContactUs.objects.only('id', 'full_name', 'contact_email', 'contact_context', 'replied', 'replied_context', 'replied_datetime', )
    replied_count = ContactUs.objects.filter(replied='yes').count()
    return contactus_list, replied_count


########################################
# FRONTEND PRIVATE VIEWS               #
########################################
class PublicationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Publication
    form_class = PublicationForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-kit/publication-update.html'
    permission_required = ('utility.update_publication', 'utility.view_publication', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_publication'
        context['page_title'] = 'Publication'
        context['page_subtitle'] = 'Peer-reviewed content'
        context['form_header'] = 'Update Publication'
        context['form_subheader'] = 'Fill and submit.'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_publications')


class PublicationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'utility.add_publication'
    model = Publication
    form_class = PublicationForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-kit/publication-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_publication'
        context['page_title'] = 'Publication'
        context['page_subtitle'] = 'Peer-reviewed content'
        context['form_header'] = 'Add Publication'
        context['form_subheader'] = 'Fill and submit.'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_publications')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class StandardOperatingProcedureTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/publications.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        sop_type = self.kwargs['sop_type']
        context['segment'] = 'view_standardoperatingprocedure'
        context['page_title'] = 'Standard Operating Procedures'
        context['page_subtitle'] = 'SOPs'
        context['pub_list'] = StandardOperatingProcedure.objects.prefetch_related('created_by').filter(sop_type=sop_type).order_by('pk')
        return context


class StandardOperatingProcedureUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = StandardOperatingProcedure
    form_class = StandardOperatingProcedureForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-kit/standardoperatingprocedure-update.html'
    permission_required = ('utility.update_standardoperatingprocedure', 'utility.view_standardoperatingprocedure', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_standardoperatingprocedure'
        context['page_title'] = 'Standard Operating Procedures'
        context['page_subtitle'] = 'SOPs'
        context['form_header'] = 'Update SOP'
        context['form_subheader'] = 'Fill and submit.'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_standardoperatingprocedure')


class StandardOperatingProcedureCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'utility.add_standardoperatingprocedure'
    model = StandardOperatingProcedure
    form_class = StandardOperatingProcedureForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-kit/standardoperatingprocedure-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_standardoperatingprocedure'
        context['page_title'] = 'Standard Operating Procedures'
        context['page_subtitle'] = 'SOPs'
        context['form_header'] = 'Update SOP'
        context['form_subheader'] = 'Fill and submit.'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_standardoperatingprocedure')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class ContactUsUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactUs
    form_class = ContactUsUpdateForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_contactus'
        context['page_title'] = 'Contact Us'
        return context

    def get_initial(self):
        initial = super(ContactUsUpdateView, self).get_initial()
        initial['replied_datetime'] = timezone.now()
        return initial

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('detail_contactus', kwargs={'pk': self.object.pk})


class ContactUsDetailView(LoginRequiredMixin, DetailView):
    model = ContactUs
    template_name = 'home/django-material-dashboard/contact-us-detail.html'
    fields = ['full_name', 'contact_email', 'contact_context', 'replied_context', 'replied_datetime', ]

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'detail_contactus'
        context['page_title'] = 'Contact Us'
        return context


########################################
# FRONTEND PUBLIC VIEWS                #
########################################
class AccountExpiredTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/account-expired.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'accountexpired'
        context['page_title'] = 'Account Expired'
        return context


class AboutUsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/about-us.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'aboutus'
        context['page_title'] = 'About Us'
        return context


class ProjectsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/projects.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_projects'
        context['page_title'] = 'Projects'
        context['project_list'] = Project.objects.prefetch_related('created_by', 'grant_names').order_by('pk')
        return context


class PublicationTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/publications.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_publications'
        context['page_title'] = 'Publications'
        context['page_subtitle'] = 'Peer-reviewed content'
        context['pub_list'] = Publication.objects.prefetch_related('created_by', 'project_names', 'publication_authors').order_by('pk')
        return context


class ProjectSurveyTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    template_name = 'home/django-material-kit/project-detail.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Project Surveys'
        context['segment'] = 'projectsurvey'
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        # context['markers'] = json.loads(serialize('geojson', FieldSurvey.objects.prefetch_related('project_ids').filter(project_ids=self.project).only('geom', 'survey_datetime', 'site_name')))
        context['project'] = self.project
        return context


class MetadataStandardsTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    template_name = 'home/django-material-kit/metadata-standards.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Metadata Standards'
        context['segment'] = 'metadatastandards'


class ContactUsCreateView(CreateView):
    # public template, to make private add LoginRequiredMixin
    model = ContactUs
    form_class = ContactUsForm
    template_name = 'home/django-material-kit/contact-us.html'
    # success_url = reverse_lazy('contact_us_received') # placed in urls.py

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us'
        context['segment'] = 'contactus'
        context['form_header'] = 'Contact Us'
        context['form_subheader'] = 'For further questions, please fill out and submit this form.'
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
         # It should return an HttpResponse.
        if self.request.user.is_authenticated:
            # if logged in, add current user to created_by
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            # form.send_email()
        return super().form_valid(form)


class ContactUsReceivedTemplateView(TemplateView):
    # public template, to make private add LoginRequiredMixin
    template_name = 'home/django-material-kit/contact-us-received.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us'
        context['segment'] = 'contactus'
        return context


########################################
# SERIALIZER VIEWS                     #
########################################
class GrantViewSet(viewsets.ModelViewSet):
    # formerly Project in field_site.models
    serializer_class = utility_serializers.GrantSerializer
    queryset = Grant.objects.prefetch_related('created_by')
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email']
    filterset_class = utility_filters.GrantSerializerFilter
    swagger_tags = ['utility']


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = utility_serializers.ProjectSerializer
    queryset = Project.objects.prefetch_related('created_by', 'grant_names')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'grant_name__grant_code']
    filterset_class = utility_filters.ProjectSerializerFilter
    swagger_tags = ['utility']


class PublicationViewSet(viewsets.ModelViewSet):
    serializer_class = utility_serializers.PublicationSerializer
    queryset = Project.objects.prefetch_related('created_by', 'project_names', 'publication_authors', )
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'grant_name__grant_code']
    filterset_class = utility_filters.PublicationSerializerFilter
    swagger_tags = ['utility']


class StandardOperatingProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = utility_serializers.StandardOperatingProcedureSerializer
    queryset = StandardOperatingProcedure.objects.prefetch_related('created_by', )
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'grant_name__grant_code']
    filterset_class = utility_filters.StandardOperatingProcedureSerializerFilter
    swagger_tags = ['utility']


class ProcessLocationViewSet(viewsets.ModelViewSet):
    serializer_class = utility_serializers.ProcessLocationSerializer
    queryset = ProcessLocation.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'process_location_name_slug']
    filterset_class = utility_filters.ProcessLocationSerializerFilter
    swagger_tags = ['utility']


class ContactUsViewSet(viewsets.ModelViewSet):
    serializer_class = utility_serializers.ContactUsSerializer
    queryset = ContactUs.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['created_by__email', 'process_location_name_slug']
    filterset_class = utility_filters.ContactUsSerializerFilter
    swagger_tags = ['utility']


class DefaultSiteCssViewSet(viewsets.ModelViewSet):
    serializer_class = utility_serializers.DefaultSiteCssSerializer
    queryset = DefaultSiteCss.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['default_css_label', 'created_by__email', 'created_datetime']
    filterset_class = utility_filters.DefaultSiteCssSerializerFilter
    swagger_tags = ['utility']


class CustomUserCssViewSet(viewsets.ModelViewSet):
    serializer_class = utility_serializers.CustomUserCssSerializer
    queryset = CustomUserCss.objects.prefetch_related('created_by',)
    filter_backends = [filters.DjangoFilterBackend]
    # filterset_fields = ['custom_css_label', 'created_by__email', 'created_datetime']
    filterset_class = utility_filters.CustomUserCssSerializerFilter
    swagger_tags = ['utility']


########################################
# GENERIC CHOICE SERIALIZERS           #
########################################
# https://stackoverflow.com/questions/62935570/what-is-the-best-way-for-connecting-django-models-choice-fields-with-react-js-se
# enum serializers to return choices
class YesNoChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.YesNo:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class SopTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.SopTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


########################################
# CHOICE SERIALIZERS - UNITS           #
########################################
class TempUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.TempUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class MeasureUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.MeasureUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class VolUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.VolUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class ConcentrationUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.ConcentrationUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class PhiXConcentrationUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.PhiXConcentrationUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class PcrUnitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.PcrUnits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


########################################
# CHOICE SERIALIZERS - FIELD_SURVEY    #
########################################
class WindSpeedsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.WindSpeeds:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CloudCoversChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.CloudCovers:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class PrecipTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.PrecipTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class TurbidTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.TurbidTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class EnvoMaterialsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.EnvoMaterials:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class MeasureModesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.MeasureModes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class EnvInstrumentsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.EnvInstruments:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class YsiModelsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.YsiModels:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class BottomSubstratesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.BottomSubstrates:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class WaterCollectionModesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.WaterCollectionModes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CollectionTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.CollectionTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class FilterLocationsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.FilterLocations:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class ControlTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.ControlTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class FilterMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.FilterMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class FilterTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.FilterTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CoreMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.CoreMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class SubCoreMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.SubCoreMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


########################################
# CHOICE SERIALIZERS - WET_LAB         #
########################################
class TargetGenesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.TargetGenes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class SubFragmentsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.SubFragments:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class PcrTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.PcrTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class LibLayoutsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.LibLayouts:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class LibPrepTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.LibPrepTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class LibPrepKitsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.LibPrepKits:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class SeqMethodsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.SeqMethods:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class InvestigationTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.InvestigationTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


##########################################
# CHOICE SERIALIZERS - FREEZER_INVENTORY #
##########################################
class InvStatusChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.InvStatus:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class InvLocStatusChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.InvLocStatus:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class InvTypesChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.InvTypes:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


class CheckoutActionsChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.CheckoutActions:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)


# BIOINFORMATICS CHOICES
class QualityChecksChoicesViewSet(viewsets.ViewSet):
    swagger_tags = ['choices']
    permission_classes = [IsAuthenticated, ]

    def list(self, request, format=None):
        choices = []
        for choice in utility_enums.QualityChecks:
            choices.append(choice.value)
        initial_data = {'choices': choices}
        return Response(initial_data, status=status.HTTP_200_OK)

# migrated to db model
# class EnvMeasurementsChoicesViewSet(viewsets.ViewSet):
#     swagger_tags = ['choices']
#
#     def list(self, request, format=None):
#         choices = []
#         for choice in EnvMeasurements:
#             choices.append(choice.value)
#         initial_data = {'choices': choices}
#         return Response(initial_data, status=status.HTTP_200_OK)
