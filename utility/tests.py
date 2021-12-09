from django.test import TestCase
from .models import Grant, Project, ProcessLocation, DefaultSiteCss, CustomUserCss
from django.contrib.auth import get_user_model


# Create your tests here.
class GrantTestCase(TestCase):
    # formerly Project in field_sites.models
    def setUp(self):
        Grant.objects.get_or_create(grant_code="e", defaults={'grant_label': "Maine-eDNA"})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Grant.objects.get(grant_code="e")
        self.assertIs(medna.was_added_recently(), True)


class ProjectTestCase(TestCase):
    # formerly Project in field_sites.models
    def setUp(self):
        grant_test = GrantTestCase()
        grant_test.setUp()
        grant_name = Grant.objects.filter()[:1].get()
        Project.objects.get_or_create(project_code="prj_commsci", defaults={'project_label': "Community Science", 'grant_name': grant_name})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Project.objects.get(project_code="prj_commsci")
        self.assertIs(medna.was_added_recently(), True)


class ProcessLocationTestCase(TestCase):
    # formerly Project in field_sites.models
    def setUp(self):
        ProcessLocation.objects.get_or_create(process_location_name="CORE",
                                              defaults={
                                                  'affiliation': "UMaine",
                                                  'process_location_url': "https://www.test.com",
                                                  'phone_number': "999-867-5309",
                                                  'location_email_address': "test@test.com",
                                                  'point_of_contact_email_address': "test@test.com",
                                                  'point_of_contact_first_name': "test first",
                                                  'point_of_contact_last_name': "test last",
                                                  'location_notes': "this is a test"})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = ProcessLocation.objects.get(process_location_name="CORE")
        self.assertIs(medna.was_added_recently(), True)


class DefaultSiteCssTestCase(TestCase):
    def setUp(self):
        DefaultSiteCss.objects.get_or_create(default_css_label="default_css_label",
                                             defaults={
                                                 'css_selected_background_color': "css_selected_background_color",
                                                 'css_selected_text_color': "css_selected_text_color",
                                                 'freezer_empty_css_background_color': "freezer_empty_css_background_color",
                                                 'freezer_empty_css_text_color': "freezer_empty_css_text_color",
                                                 'freezer_inuse_css_background_color': "freezer_inuse_css_background_color",
                                                 'freezer_inuse_css_text_color': "freezer_inuse_css_text_color",
                                                 'freezer_empty_rack_css_background_color': "freezer_empty_rack_css_background_color",
                                                 'freezer_empty_rack_css_text_color': "freezer_empty_rack_css_text_color",
                                                 'freezer_inuse_rack_css_background_color': "freezer_inuse_rack_css_background_color",
                                                 'freezer_inuse_rack_css_text_color': "freezer_inuse_rack_css_text_color",
                                                 'freezer_empty_box_css_background_color': "freezer_empty_box_css_background_color",
                                                 'freezer_empty_box_css_text_color': "freezer_empty_box_css_text_color",
                                                 'freezer_inuse_box_css_background_color': "freezer_inuse_box_css_background_color",
                                                 'freezer_inuse_box_css_text_color': "freezer_inuse_box_css_text_color",
                                                 'freezer_empty_inventory_css_background_color': "freezer_empty_inventory_css_background_color",
                                                 'freezer_empty_inventory_css_text_color': "freezer_empty_inventory_css_text_color",
                                                 'freezer_inuse_inventory_css_background_color': "freezer_inuse_inventory_css_background_color",
                                                 'freezer_inuse_inventory_css_text_color': "freezer_inuse_inventory_css_text_color"})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = DefaultSiteCss.objects.get(default_css_label="default_css_label")
        self.assertIs(medna.was_added_recently(), True)


class CustomUserCssTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        CustomUserCss.objects.get_or_create(custom_css_label="custom_css_label",
                                            defaults={
                                                'user': user,
                                                'css_selected_background_color': "css_selected_background_color",
                                                'css_selected_text_color': "css_selected_text_color",
                                                'freezer_empty_css_background_color': "freezer_empty_css_background_color",
                                                'freezer_empty_css_text_color': "freezer_empty_css_text_color",
                                                'freezer_inuse_css_background_color': "freezer_inuse_css_background_color",
                                                'freezer_inuse_css_text_color': "freezer_inuse_css_text_color",
                                                'freezer_empty_rack_css_background_color': "freezer_empty_rack_css_background_color",
                                                'freezer_empty_rack_css_text_color': "freezer_empty_rack_css_text_color",
                                                'freezer_inuse_rack_css_background_color': "freezer_inuse_rack_css_background_color",
                                                'freezer_inuse_rack_css_text_color': "freezer_inuse_rack_css_text_color",
                                                'freezer_empty_box_css_background_color': "freezer_empty_box_css_background_color",
                                                'freezer_empty_box_css_text_color': "freezer_empty_box_css_text_color",
                                                'freezer_inuse_box_css_background_color': "freezer_inuse_box_css_background_color",
                                                'freezer_inuse_box_css_text_color': "freezer_inuse_box_css_text_color",
                                                'freezer_empty_inventory_css_background_color': "freezer_empty_inventory_css_background_color",
                                                'freezer_empty_inventory_css_text_color': "freezer_empty_inventory_css_text_color",
                                                'freezer_inuse_inventory_css_background_color': "freezer_inuse_inventory_css_background_color",
                                                'freezer_inuse_inventory_css_text_color': "freezer_inuse_inventory_css_text_color"})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = CustomUserCss.objects.get(custom_css_label="custom_css_label")
        self.assertIs(medna.was_added_recently(), True)
