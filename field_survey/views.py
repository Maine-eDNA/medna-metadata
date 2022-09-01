from django.db import transaction
from django.db.models import F, Count, Func, Value, CharField, Q
from django.db.models.functions import TruncMonth
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
import json
from django_filters import rest_framework as filters
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from rest_framework import generics
from rest_framework import viewsets
from utility.charts import return_queryset_lists, return_zeros_lists, return_merged_zeros_lists
from utility.views import export_context, CreatePopupMixin, UpdatePopupMixin
from utility.serializers import SerializerExportMixin, CharSerializerExportMixin
from utility.enumerations import CollectionTypes
from sample_label.models import SampleMaterial
import field_survey.filters as fieldsurvey_filters
import field_survey.serializers as fieldsurvey_serializers
from .models import FieldSurvey, FieldCrew, EnvMeasureType, EnvMeasurement, \
    FieldCollection, WaterCollection, SedimentCollection, \
    FieldSample, FilterSample, SubCoreSample, \
    FieldSurveyETL, FieldCrewETL, EnvMeasurementETL, \
    FieldCollectionETL, SampleFilterETL
from .tables import FieldSurveyTable, FieldCrewTable, EnvMeasurementTable, WaterCollectionTable, \
    SedimentCollectionTable, FilterSampleTable, SubCoreSampleTable
from .forms import FieldSurveyForm, FieldCrewForm, EnvMeasurementForm, FieldCollectionForm, WaterCollectionForm, \
    SedimentCollectionForm, FieldSampleForm, FilterSampleForm, SubCoreSampleForm
from django.conf import settings


# Create your views here.
########################################
# FRONTEND REQUESTS                    #
########################################
@permission_required('field_survey.view_fieldsurvey', login_url='dashboard_login')
@login_required(login_url='dashboard_login')
def get_field_survey_geom(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    # https://stackoverflow.com/questions/52025577/how-to-remove-certain-fields-when-doing-serialization-to-a-django-model
    # project = get_object_or_404(Project, pk=pk)
    qs = FieldSurvey.objects.only('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids').prefetch_related('project_ids')
    qs_json = serialize('geojson', qs, fields=('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids'))
    return JsonResponse(json.loads(qs_json))


def get_project_survey_geom(request, pk):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
    # https://leafletjs.com/examples/geojson/
    # https://stackoverflow.com/questions/52025577/how-to-remove-certain-fields-when-doing-serialization-to-a-django-model
    # project = get_object_or_404(Project, pk=pk)
    qs = FieldSurvey.objects.only('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids').prefetch_related('project_ids').filter(project_ids=pk)
    qs_json = serialize('geojson', qs, fields=('survey_global_id', 'geom', 'survey_datetime', 'site_name', 'project_ids'))
    return JsonResponse(json.loads(qs_json))


@login_required(login_url='dashboard_login')
def get_survey_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    # labels, data = return_queryset_lists(FieldSurvey.objects.annotate(survey_date=TruncMonth('survey_datetime')).values('survey_date').order_by('survey_date').annotate(data=Count('pk')).annotate(label=Func(F('survey_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    labels, data = return_queryset_lists(FieldSurvey.objects.annotate(survey_date=TruncMonth('survey_datetime')).values('survey_date').annotate(data=Count('pk')).order_by('survey_date').annotate(label=Func(F('survey_date'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    labels, data = return_zeros_lists(labels, data)
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_survey_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FieldSurvey.objects.exclude(Q(site_id__system__system_label__exact='') | Q(site_id__system__system_label__isnull=True)).annotate(label=F('site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))
    # labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_survey_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    labels, data = return_queryset_lists(FieldSurvey.objects.exclude(Q(site_id__site_id__exact='') | Q(site_id__site_id__isnull=True)).annotate(label=F('site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))
    # labels = ['eLP_O01' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_field_sample_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/38570258/how-to-get-django-queryset-results-with-formatted-datetime-field
    # https://stackoverflow.com/questions/52354104/django-query-set-for-counting-records-each-month
    filter_labels, filter_data = return_queryset_lists(FilterSample.objects.annotate(filter_date=TruncMonth('filter_datetime')).values('filter_date').annotate(data=Count('pk')).annotate(label=Func(F('filter_datetime'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    subcore_labels, subcore_data = return_queryset_lists(SubCoreSample.objects.annotate(subcore_date=TruncMonth('subcore_datetime_start')).values('subcore_date').annotate(data=Count('pk')).annotate(label=Func(F('subcore_datetime_start'), Value('MM/YYYY'), function='to_char', output_field=CharField())))
    fieldsample_labels, fieldsample_data = return_queryset_lists(FieldSample.objects.annotate(label=F('is_extracted')).values('label').annotate(data=Count('pk')).order_by('-label'))
    labels, data_array, = return_merged_zeros_lists([filter_labels, subcore_labels], [filter_data, subcore_data])
    return JsonResponse(data={
        'fieldsample_labels': fieldsample_labels,
        'fieldsample_data': fieldsample_data,
        'count_labels': labels,
        'filter_data': data_array[0],
        'subcore_data': data_array[1],
    })


@login_required(login_url='dashboard_login')
def get_filter_type_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FilterSample.objects.exclude(Q(filter_type__exact='') | Q(filter_type__isnull=True)).annotate(label=F('filter_type')).values('label').annotate(data=Count('pk')).order_by('-label'))
    # labels = ['other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_filter_system_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FilterSample.objects.exclude(Q(field_sample__field_sample_barcode__site_id__system__system_label__exact='') | Q(field_sample__field_sample_barcode__site_id__system__system_label__isnull=True)).annotate(label=F('field_sample__field_sample_barcode__site_id__system__system_label')).values('label').annotate(data=Count('pk')).order_by('-label'))
    # labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


@login_required(login_url='dashboard_login')
def get_filter_site_count_chart(request):
    # https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    # https://stackoverflow.com/questions/31933239/using-annotate-or-extra-to-add-field-of-foreignkey-to-queryset-equivalent-of/31933276#31933276
    labels, data = return_queryset_lists(FilterSample.objects.exclude(Q(field_sample__field_sample_barcode__site_id__site_id__exact='') | Q(field_sample__field_sample_barcode__site_id__site_id__isnull=True)).annotate(label=F('field_sample__field_sample_barcode__site_id__site_id')).values('label').annotate(data=Count('pk')).order_by('-label'))
    # labels = ['Other' if x == '' else x for x in labels]
    return JsonResponse(data={'labels': labels, 'data': data, })


########################################
# FRONTEND VIEWS                       #
########################################
class FieldSurveyFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FieldSurvey
    table_class = FieldSurveyTable
    template_name = 'home/django-material-dashboard/model-filter-list-fieldsurvey.html'
    permission_required = ('field_survey.view_fieldsurvey', )
    export_name = 'fieldsurvey_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.FieldSurveyTableSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_fieldsurvey'
        context['page_title'] = 'Field Survey'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FieldSurveyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'field_survey.add_fieldsurvey'
    model = FieldSurvey
    form_class = FieldSurveyForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-fieldsurvey.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_fieldsurvey'
        context['page_title'] = 'Field Survey'
        return context

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(FieldSurveyCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_fieldsurvey')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FieldSurveyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FieldSurvey
    form_class = FieldSurveyForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-fieldsurvey.html'
    permission_required = ('field_survey.update_fieldsurvey', 'field_survey.view_fieldsurvey', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_fieldsurvey'
        context['page_title'] = 'Field Survey'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_fieldsurvey')


class FieldSurveyPopupCreateView(CreatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'field_survey.add_fieldsurvey'
    model = FieldSurvey
    form_class = FieldSurveyForm
    # fields = ['site_id', 'sample_material', 'sample_type', 'sample_year', 'purpose', 'req_sample_label_num']
    template_name = 'home/django-material-dashboard/model-add-popup-fieldsurvey.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_fieldsurvey'
        context['page_title'] = 'Field Survey'
        return context

    # Sending user object to the form, to verify which fields to display
    def get_form_kwargs(self):
        kwargs = super(FieldSurveyPopupCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FieldSurveyPopupUpdateView(UpdatePopupMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FieldSurvey
    form_class = FieldSurveyForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update-popup-fieldsurvey.html'
    permission_required = ('field_survey.update_fieldsurvey', 'field_survey.view_fieldsurvey', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_fieldsurvey'
        context['page_title'] = 'Field Survey'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class EnvMeasurementFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = EnvMeasurement
    table_class = EnvMeasurementTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_envmeasurement', )
    export_name = 'envmeas_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.EnvMeasurementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_envmeasurement'
        context['page_title'] = 'Environmental Measurement'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class EnvMeasurementCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'field_survey.add_envmeasurement'
    model = EnvMeasurement
    form_class = EnvMeasurementForm
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_envmeasurement'
        context['page_title'] = 'Environmental Measurement'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_envmeasurement')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class EnvMeasurementUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = EnvMeasurement
    form_class = EnvMeasurementForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('field_survey.update_envmeasurement', 'field_survey.view_envmeasurement', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_envmeasurement'
        context['page_title'] = 'Environmental Measurement'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_envmeasurement')


class FieldCrewFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FieldCrew
    table_class = FieldCrewTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_fieldcrew', )
    export_name = 'fieldcrew_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.FieldCrewSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_fieldcrew'
        context['page_title'] = 'Field Crew'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FieldCrewCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # LoginRequiredMixin prevents users who aren’t logged in from accessing the form.
    # If you omit that, you’ll need to handle unauthorized users in form_valid().
    permission_required = 'field_survey.add_fieldcrew'
    model = FieldCrew
    form_class = FieldCrewForm
    template_name = 'home/django-material-dashboard/model-add.html'

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'add_fieldcrew'
        context['page_title'] = 'Field Crew'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('view_fieldcrew')

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


class FieldCrewUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FieldCrew
    form_class = FieldCrewForm
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'
    template_name = 'home/django-material-dashboard/model-update.html'
    permission_required = ('field_survey.update_fieldcrew', 'field_survey.view_fieldcrew', )

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'update_fieldcrew'
        context['page_title'] = 'Field Crew'
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')

    def get_success_url(self):
        # after successfully filling out and submitting a form,
        # show the user the detail view of the label
        return reverse('view_fieldcrew')


class WaterCollectionFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = WaterCollection
    table_class = WaterCollectionTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_watercollection', )
    export_name = 'watercollection_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.WaterCollectionTableSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_watercollection'
        context['page_title'] = 'Water Collection'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


@login_required
@permission_required('field_survey.add_watercollection', login_url='/dashboard/login/')
@transaction.atomic
def water_collection_create_view(request):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    if request.method == 'POST':
        fieldcollection_form = FieldCollectionForm(request.POST, collection_type=CollectionTypes.WATER_SAMPLE)
        watercollection_form = WaterCollectionForm(request.POST)
        if fieldcollection_form.is_valid() and watercollection_form.is_valid():
            fieldcollection = fieldcollection_form.save(commit=False)
            fieldcollection.created_by = request.user
            fieldcollection = fieldcollection_form.save()
            fieldcollection.refresh_from_db()  # This will load the FieldCollection created by the Signal
            watercollection_form = WaterCollectionForm(request.POST, instance=fieldcollection.water_collection)  # Reload the watercollection form with the watercollection instance
            watercollection_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            watercollection = watercollection_form.save(commit=False)
            watercollection.created_by = request.user
            watercollection.save()  # Gracefully save the form
            return redirect('view_watercollection')
    else:
        fieldcollection_form = FieldCollectionForm(collection_type=CollectionTypes.WATER_SAMPLE)
        watercollection_form = WaterCollectionForm()
    return render(request, 'home/django-material-dashboard/model-add-related.html', {
        'parent_form': fieldcollection_form,
        'child_form': watercollection_form,
        'segment': 'add_watercollection',
        'page_title': 'Water Collection'
    })


@login_required
@permission_required('field_survey.update_watercollection', login_url='/dashboard/login/')
@transaction.atomic
def water_collection_update_view(request, pk):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    fieldcollection = get_object_or_404(FieldCollection, pk=pk)
    if request.method == 'POST':
        fieldcollection_form = FieldCollectionForm(request.POST, instance=fieldcollection)
        watercollection_form = WaterCollectionForm(request.POST, instance=fieldcollection.water_collection)
        if fieldcollection_form.is_valid() and watercollection_form.is_valid():
            fieldcollection_form.save()
            watercollection_form.save()
            messages.success(request, _('Your watercollection was successfully updated.'))
            return redirect('view_watercollection')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        fieldcollection_form = FieldCollectionForm(instance=fieldcollection)
        watercollection_form = WaterCollectionForm(instance=fieldcollection.water_collection)
    return render(request, 'home/django-material-dashboard/model-update-related.html', {
        'parent_form': fieldcollection_form,
        'child_form': watercollection_form,
        'segment': 'update_watercollection',
        'page_title': 'Water Collection'
    })


class SedimentCollectionFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = SedimentCollection
    table_class = SedimentCollectionTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_sedimentcollection', )
    export_name = 'sedimentcollection_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.SedimentCollectionTableSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_sedimentcollection'
        context['page_title'] = 'Sediment Collection'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


@login_required
@permission_required('field_survey.add_sedimentcollection', login_url='/dashboard/login/')
@transaction.atomic
def sediment_collection_create_view(request):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    if request.method == 'POST':
        fieldcollection_form = FieldCollectionForm(request.POST, collection_type=CollectionTypes.SED_SAMPLE)
        sedimentcollection_form = SedimentCollectionForm(request.POST)
        if fieldcollection_form.is_valid() and sedimentcollection_form.is_valid():
            fieldcollection = fieldcollection_form.save(commit=False)
            fieldcollection.created_by = request.user
            fieldcollection = fieldcollection_form.save()
            fieldcollection.refresh_from_db()  # This will load the FieldCollection created by the Signal
            sedimentcollection_form = SedimentCollectionForm(request.POST, instance=fieldcollection.sediment_collection)  # Reload the sedimentcollection form with the fieldcollection instance
            sedimentcollection_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            sedimentcollection = sedimentcollection_form.save(commit=False)
            sedimentcollection.created_by = request.user
            sedimentcollection.save()  # Gracefully save the form
            return redirect('view_sedimentcollection')
    else:
        fieldcollection_form = FieldCollectionForm(collection_type=CollectionTypes.SED_SAMPLE)
        sedimentcollection_form = SedimentCollectionForm()
    return render(request, 'home/django-material-dashboard/model-add-related.html', {
        'parent_form': fieldcollection_form,
        'child_form': sedimentcollection_form,
        'segment': 'add_sedimentcollection',
        'page_title': 'Sediment Collection'
    })


@login_required
@permission_required('field_survey.update_sedimentcollection', login_url='/dashboard/login/')
@transaction.atomic
def sediment_collection_update_view(request, pk):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    fieldcollection = get_object_or_404(FieldCollection, pk=pk)
    if request.method == 'POST':
        fieldcollection_form = FieldCollectionForm(request.POST, instance=fieldcollection)
        sedimentcollection_form = SedimentCollectionForm(request.POST, instance=fieldcollection.sediment_collection)
        if fieldcollection_form.is_valid() and sedimentcollection_form.is_valid():
            fieldcollection_form.save()
            sedimentcollection_form.save()
            messages.success(request, _('Your sedimentcollection was successfully updated.'))
            return redirect('view_sedimentcollection')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        fieldcollection_form = FieldCollectionForm(instance=fieldcollection)
        sedimentcollection_form = SedimentCollectionForm(instance=fieldcollection.sediment_collection)
    return render(request, 'home/django-material-dashboard/model-update-related.html', {
        'parent_form': fieldcollection_form,
        'child_form': sedimentcollection_form,
        'segment': 'update_sedimentcollection',
        'page_title': 'Sediment Collection'
    })


class FilterSampleFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = FilterSample
    table_class = FilterSampleTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_fieldsurvey', 'field_survey.view_fieldcrew',
                           'field_survey.view_envmeasurement', 'field_survey.view_fieldcollection',
                           'field_survey.view_watercollection', 'field_survey.view_fieldsample',
                           'field_survey.view_filtersample', )
    export_name = 'filtersample_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.FilterSampleTableSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_filtersample'
        context['page_title'] = 'Filter Sample'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


@login_required
@permission_required('field_survey.add_fieldsample', login_url='/dashboard/login/')
@transaction.atomic
def filter_sample_create_view(request):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    if request.method == 'POST':
        fieldsample_form = FieldSampleForm(request.POST, sample_material=SampleMaterial.objects.get(sample_material_code='w'))
        filtersample_form = FilterSampleForm(request.POST)
        if fieldsample_form.is_valid() and filtersample_form.is_valid():
            fieldsample = fieldsample_form.save(commit=False)
            fieldsample.created_by = request.user
            fieldsample = fieldsample_form.save()
            fieldsample.refresh_from_db()  # This will load the FieldSample created by the Signal
            filtersample_form = FilterSampleForm(request.POST, instance=fieldsample.filter_sample)  # Reload the filtersample form with the fieldsample instance
            filtersample_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            filtersample = filtersample_form.save(commit=False)
            filtersample.created_by = request.user
            filtersample.save()  # Gracefully save the form
            return redirect('view_filtersample')
    else:
        fieldsample_form = FieldSampleForm(sample_material=SampleMaterial.objects.get(sample_material_code='w'))
        filtersample_form = FilterSampleForm()
    return render(request, 'home/django-material-dashboard/model-add-related.html', {
        'parent_form': fieldsample_form,
        'child_form': filtersample_form,
        'segment': 'add_filtersample',
        'page_title': 'Filter Sample'
    })


@login_required
@permission_required('field_survey.update_fieldsample', login_url='/dashboard/login/')
@transaction.atomic
def filter_sample_update_view(request, pk):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    fieldsample = get_object_or_404(FieldSample, pk=pk)
    if request.method == 'POST':
        fieldsample_form = FieldSampleForm(request.POST, instance=fieldsample, pk=pk)
        filtersample_form = FilterSampleForm(request.POST, instance=fieldsample.filter_sample)
        if fieldsample_form.is_valid() and filtersample_form.is_valid():
            fieldsample_form.save()
            filtersample_form.save()
            messages.success(request, _('Your filtersample was successfully updated.'))
            return redirect('view_filtersample')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        fieldsample_form = FieldSampleForm(instance=fieldsample, pk=pk)
        filtersample_form = FilterSampleForm(instance=fieldsample.filter_sample)
    return render(request, 'home/django-material-dashboard/model-update-related.html', {
        'parent_form': fieldsample_form,
        'child_form': filtersample_form,
        'segment': 'update_filtersample',
        'page_title': 'Filter Sample'
    })


class SubCoreSampleFilterView(LoginRequiredMixin, PermissionRequiredMixin, CharSerializerExportMixin, SingleTableMixin, FilterView):
    # permissions - https://stackoverflow.com/questions/9469590/check-permission-inside-a-template-in-django
    # View site filter view with REST serializer and django-tables2
    # export_formats = ['csv','xlsx'] # set in user_sites in default
    model = SubCoreSample
    table_class = SubCoreSampleTable
    template_name = 'home/django-material-dashboard/model-filter-list.html'
    permission_required = ('field_survey.view_fieldsurvey', 'field_survey.view_fieldcrew',
                           'field_survey.view_envmeasurement', 'field_survey.view_fieldcollection',
                           'field_survey.view_watercollection', 'field_survey.view_fieldsample',
                           'field_survey.view_subcoresample', )
    export_name = 'subcoresample_' + str(timezone.now().replace(microsecond=0).isoformat())
    serializer_class = fieldsurvey_serializers.SubCoreSampleTableSerializer
    filter_backends = [filters.DjangoFilterBackend]
    export_formats = settings.EXPORT_FORMATS

    def get_context_data(self, **kwargs):
        # Return the view context data.
        context = super().get_context_data(**kwargs)
        context['segment'] = 'view_subcoresample'
        context['page_title'] = 'SubCore Sample'
        context['export_formats'] = self.export_formats
        context = {**context, **export_context(self.request, self.export_formats)}
        return context

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('main/model-perms-required.html')


@login_required
@permission_required('field_survey.add_fieldsample', login_url='/dashboard/login/')
@transaction.atomic
def subcore_sample_create_view(request):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    if request.method == 'POST':
        fieldsample_form = FieldSampleForm(request.POST, sample_material=SampleMaterial.objects.get(sample_material_code='s'))
        subcore_form = SubCoreSampleForm(request.POST)
        if fieldsample_form.is_valid() and subcore_form.is_valid():
            fieldsample = fieldsample_form.save(commit=False)
            fieldsample.created_by = request.user
            fieldsample = fieldsample_form.save()
            fieldsample.refresh_from_db()  # This will load the FieldSample created by the Signal
            subcore_form = SubCoreSampleForm(request.POST, instance=fieldsample.subcore_sample)  # Reload the subcore form with the fieldsample instance
            subcore_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            subcoresample = subcore_form.save(commit=False)
            subcoresample.created_by = request.user
            subcoresample.save()  # Gracefully save the form
            return redirect('view_subcoresample')
    else:
        fieldsample_form = FieldSampleForm(sample_material=SampleMaterial.objects.get(sample_material_code='s'))
        subcore_form = SubCoreSampleForm()
    return render(request, 'home/django-material-dashboard/model-add-related.html', {
        'parent_form': fieldsample_form,
        'child_form': subcore_form,
        'segment': 'add_subcoresample',
        'page_title': 'SubCore Sample'
    })


@login_required
@permission_required('field_survey.update_fieldsample', login_url='/dashboard/login/')
@transaction.atomic
def subcore_sample_update_view(request, pk):
    # TODO change to class based view to enable popups
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    # https://gist.github.com/vitorfs/cbe877156ba538a20c53c9a1cea29277
    fieldsample = get_object_or_404(FieldSample, pk=pk)
    if request.method == 'POST':
        fieldsample_form = FieldSampleForm(request.POST, instance=fieldsample, pk=pk)
        subcore_form = SubCoreSampleForm(request.POST, instance=fieldsample.subcore_sample)
        if fieldsample_form.is_valid() and subcore_form.is_valid():
            fieldsample_form.save()
            subcore_form.save()
            messages.success(request, _('Your subcore was successfully updated.'))
            return redirect('view_subcoresample')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        fieldsample_form = FieldSampleForm(instance=fieldsample, pk=pk)
        subcore_form = SubCoreSampleForm(instance=fieldsample.subcore_sample)
    return render(request, 'home/django-material-dashboard/model-update-related.html', {
        'parent_form': fieldsample_form,
        'child_form': subcore_form,
        'segment': 'update_subcoresample',
        'page_title': 'SubCore Sample'
    })


########################################
# SERIALIZER VIEWS - POST TRANSFORM    #
########################################
class GeoFieldSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.GeoFieldSurveySerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'qa_editor',
                                                    'core_subcorer', 'water_filterer', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.GeoFieldSurveySerializerFilter
    swagger_tags = ['field survey']


class FieldCrewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCrewSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
    queryset = FieldCrew.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCrewSerializerFilter
    swagger_tags = ['field survey']


class EnvMeasureTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.EnvMeasureTypeSerializer
    queryset = EnvMeasureType.objects.prefetch_related('created_by', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasureTypeSerializerFilter
    swagger_tags = ['field survey']


class EnvMeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.EnvMeasurementSerializer
    queryset = EnvMeasurement.objects.prefetch_related('created_by', 'survey_global_id', 'env_measurement', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasurementSerializerFilter
    swagger_tags = ['field survey']


class FieldCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCollectionSerializer
    queryset = FieldCollection.objects.prefetch_related('created_by', 'survey_global_id', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCollectionSerializerFilter
    swagger_tags = ['field survey']


class WaterCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.WaterCollectionSerializer
    queryset = WaterCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.WaterCollectionSerializerFilter
    swagger_tags = ['field survey']


class SedimentCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.SedimentCollectionSerializer
    queryset = SedimentCollection.objects.prefetch_related('created_by', 'field_collection')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SedimentCollectionSerializerFilter
    swagger_tags = ['field survey']


class FieldSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSampleSerializer
    queryset = FieldSample.objects.prefetch_related('created_by', 'collection_global_id', 'sample_material', 'field_sample_barcode', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSampleSerializerFilter
    swagger_tags = ['field survey']


class FilterSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FilterSampleSerializer
    queryset = FilterSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FilterSampleSerializerFilter
    swagger_tags = ['field survey']


class SubCoreSampleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.SubCoreSampleSerializer
    queryset = SubCoreSample.objects.prefetch_related('created_by', 'field_sample')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SubCoreSampleSerializerFilter
    swagger_tags = ['field survey']


class FieldSurveyEnvsNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSurveyEnvsNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'water_filterer', 'qa_editor', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveyEnvsNestedSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FieldSurveyFiltersNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSurveyFiltersNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'water_filterer', 'qa_editor', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveyFiltersNestedSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


class FieldSurveySubCoresNestedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldSurveySubCoresNestedSerializer
    # https://stackoverflow.com/questions/39669553/django-rest-framework-setting-up-prefetching-for-nested-serializers
    # https://www.django-rest-framework.org/api-guide/relations/
    # queryset = FieldSurvey.objects.prefetch_related('created_by', 'project_ids', 'site_id', 'username', 'supervisor', 'core_subcorer', 'qa_editor', 'record_creator', 'record_editor', )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldSurveySubCoresNestedSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        queryset = FieldSurvey.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)


########################################
# SERIALIZER VIEWS - PRE TRANSFORM     #
########################################
class GeoFieldSurveyETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.GeoFieldSurveyETLSerializer
    queryset = FieldSurveyETL.objects.prefetch_related('created_by')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.GeoFieldSurveyETLSerializerFilter
    swagger_tags = ['field survey']


class FieldCrewETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCrewETLSerializer
    queryset = FieldCrewETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCrewETLSerializerFilter
    swagger_tags = ['field survey']


class EnvMeasurementETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.EnvMeasurementETLSerializer
    queryset = EnvMeasurementETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.EnvMeasurementETLSerializerFilter
    swagger_tags = ['field survey']


class FieldCollectionETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.FieldCollectionETLSerializer
    queryset = FieldCollectionETL.objects.prefetch_related('created_by', 'survey_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.FieldCollectionETLSerializerFilter
    swagger_tags = ['field survey']


class SampleFilterETLViewSet(viewsets.ModelViewSet):
    serializer_class = fieldsurvey_serializers.SampleFilterETLSerializer
    queryset = SampleFilterETL.objects.prefetch_related('created_by', 'collection_global_id')
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.SampleFilterETLSerializerFilter
    swagger_tags = ['field survey']


class DuplicateFilterSampleETLAPIView(generics.ListAPIView):
    serializer_class = fieldsurvey_serializers.SampleFilterETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.DuplicateFilterSampleETLSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        # returns a list of all the duplicate filter barcodes
        # https://stackoverflow.com/questions/31306875/pass-a-custom-queryset-to-serializer-in-django-rest-framework
        # grab barcodes with duplicates
        filter_duplicates = SampleFilterETL.objects.values(
            'filter_barcode'
        ).annotate(filter_barcode_count=Count(
            'filter_barcode'
        )).filter(filter_barcode_count__gt=1)

        dup_filter_records = SampleFilterETL.objects.filter(
            filter_barcode__in=[item['filter_barcode'] for item in filter_duplicates])

        return dup_filter_records


class DuplicateSubCoreSampleETLAPIView(generics.ListAPIView):
    serializer_class = fieldsurvey_serializers.FieldCollectionETLSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = fieldsurvey_filters.DuplicateSubCoreSampleETLSerializerFilter
    swagger_tags = ['field survey']

    def get_queryset(self):
        # returns a list of all the duplicate subcore barcodes
        fields = ('subcore_fname', 'subcore_lname',
                  'subcore_protocol', 'subcore_protocol_other',
                  'subcore_method', 'subcore_method_other', 'subcore_datetime_start', 'subcore_datetime_end',
                  'subcore_min_barcode', 'subcore_max_barcode', 'subcore_number', 'subcore_length',
                  'subcore_diameter', 'subcore_clayer', 'record_creator', 'record_editor')
        # https://stackoverflow.com/questions/31306875/pass-a-custom-queryset-to-serializer-in-django-rest-framework
        # grab barcodes with duplicates
        subcore_duplicates = FieldCollectionETL.objects.values(
            'subcore_min_barcode'
        ).annotate(subcore_min_barcode_count=Count(
            'subcore_min_barcode'
        )).filter(subcore_min_barcode_count__gt=1)

        dup_subcore_records = FieldCollectionETL.objects.filter(
            subcore_min_barcode__in=[item['subcore_min_barcode'] for item in subcore_duplicates]).only(fields)
        # grab subcores with blank barcodes
        # subcore_empty = FieldCollectionETL.objects.filter(collection_type='sed_sample').filter(subcore_min_barcode__exact='')

        return dup_subcore_records
