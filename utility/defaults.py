from sample_labels.models import SampleType
from utility.models import ProcessLocation
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone


def now_plus_max():
    # maximum possible datetime
    now = timezone.now()
    max_date = now + datetime.timedelta(days=999999)
    return max_date


def current_year():
    return datetime.date.today().year


def year_choices():
    return [(r, r) for r in range(2018, datetime.date.today().year+1)]


def slug_date_format(date):
    # so that date format can be changed in one spot
    date_fmt = date
    return date_fmt.strftime('%Y%m%d_%H%M%S')


def get_sentinel_user():
    # if user is deleted, fill with 'deleted' username
    return get_user_model().objects.get_or_create(email='deleted@user.com')[0]


def get_default_user():
    return get_user_model().objects.get_or_create(email='default@user.com')[0]


def get_default_sample_type():
    return SampleType.objects.get_or_create(sample_type_code='fs',
                                            defaults={'sample_type_label': "Field Sample"})[0]


def get_default_process_location():
    return ProcessLocation.objects.get_or_create(process_location_name='eDNA Laboratory (UMaine CORE)',
                                                 defaults={'affiliation': 'University of Maine',
                                                           'process_location_url': 'https://umaine.edu/core/biotechnology/',
                                                           'phone_number': '+12075812591',
                                                           'location_email_address': 'um.core@maine.edu',
                                                           'point_of_contact_email_address': 'geneva.york@maine.edu',
                                                           'point_of_contact_first_name': 'Geneva',
                                                           'point_of_contact_last_name': 'York',
                                                           'location_notes': ''})[0]
