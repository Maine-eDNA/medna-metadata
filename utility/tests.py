from django.test import TestCase
from .models import ContactUs, Fund, Project, Publication, ProcessLocation, StandardOperatingProcedure, DefaultSiteCss, CustomUserCss
from utility.enumerations import SopTypes
from users.tests import UsersManagersTests
from users.models import CustomUser
# from django.contrib.auth import get_user_model


# Create your tests here.
class FundTestCase(TestCase):
    # formerly Project in field_site.models
    def setUp(self):
        Fund.objects.get_or_create(fund_code='e', defaults={'fund_label': 'Maine-eDNA',
                                                              'fund_description': 'test description'})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Fund.objects.get(fund_code='e')
        self.assertIs(medna.was_added_recently(), True)


class ProjectTestCase(TestCase):
    # formerly Project in field_site.models
    def setUp(self):
        manytomany_list = []
        fund_test = FundTestCase()
        fund_test.setUp()
        fund_name = Fund.objects.filter()[:1].get()
        manytomany_list.append(fund_name)
        project, created = Project.objects.get_or_create(project_code='prj_commsci',
                                                         defaults={'project_label': 'Community Science',
                                                                   'project_description': 'test description',
                                                                   'project_goals': 'test questions'})
        project.fund_names.set(manytomany_list, clear=True)

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Project.objects.get(project_code='prj_commsci')
        self.assertIs(medna.was_added_recently(), True)


class PublicationTestCase(TestCase):
    # formerly Project in field_site.models
    def setUp(self):
        manytomany_prj_list = []
        manytomany_usr_list = []
        project_test = ProjectTestCase()
        project_test.setUp()
        project_name = Project.objects.filter()[:1].get()
        manytomany_prj_list.append(project_name)
        user_test = UsersManagersTests()
        user_test.setUp()
        user_name = CustomUser.objects.filter()[:1].get()
        manytomany_usr_list.append(user_name)
        publication, created = Publication.objects.get_or_create(publication_title='the title of the publication',
                                                                 defaults={'publication_url': 'https://www.doi.com'})
        publication.project_names.set(manytomany_prj_list, clear=True)
        publication.publication_authors.set(manytomany_usr_list, clear=True)

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Publication.objects.get(publication_title='the title of the publication')
        self.assertIs(medna.was_added_recently(), True)


class StandardOperatingProcedureTestCase(TestCase):
    # formerly Project in field_site.models
    def setUp(self):
        StandardOperatingProcedure.objects.get_or_create(sop_title='test sop',
                                                         defaults={
                                                             'sop_url': 'https://www.test.com',
                                                             'sop_type': SopTypes.WETLAB})

    def test_was_added_recently(self):
        # test if date is added correctly
        sop = StandardOperatingProcedure.objects.get(sop_title='test sop')
        self.assertIs(sop.was_added_recently(), True)


class ProcessLocationTestCase(TestCase):
    # formerly Project in field_site.models
    def setUp(self):
        ProcessLocation.objects.get_or_create(process_location_name='CORE',
                                              defaults={
                                                  'affiliation': 'UMaine',
                                                  'process_location_url': 'https://www.test.com',
                                                  'phone_number': '999-867-5309',
                                                  'location_email_address': 'test@test.com',
                                                  'point_of_contact_email_address': 'test@test.com',
                                                  'point_of_contact_first_name': 'test first',
                                                  'point_of_contact_last_name': 'test last',
                                                  'location_notes': 'this is a test'})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = ProcessLocation.objects.get(process_location_name='CORE')
        self.assertIs(medna.was_added_recently(), True)


class ContactUsTestCase(TestCase):
    # formerly Project in field_site.models
    def setUp(self):
        ContactUs.objects.get_or_create(full_name='test person',
                                        defaults={
                                            'contact_email': 'test@test.com',
                                            'contact_context': 'test first',
                                        })

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = ContactUs.objects.get(full_name='test person')
        self.assertIs(medna.was_added_recently(), True)


class DefaultSiteCssTestCase(TestCase):
    def setUp(self):
        DefaultSiteCss.objects.get_or_create(default_css_label='default_css_label',
                                             defaults={
                                                 'css_selected_background_color': 'css_selected_background_color',
                                                 'css_selected_text_color': 'css_selected_text_color',
                                                 'freezer_empty_css_background_color': 'freezer_empty_css_background_color',
                                                 'freezer_empty_css_text_color': 'freezer_empty_css_text_color',
                                                 'freezer_inuse_css_background_color': 'freezer_inuse_css_background_color',
                                                 'freezer_inuse_css_text_color': 'freezer_inuse_css_text_color',
                                                 'freezer_empty_rack_css_background_color': 'freezer_empty_rack_css_background_color',
                                                 'freezer_empty_rack_css_text_color': 'freezer_empty_rack_css_text_color',
                                                 'freezer_inuse_rack_css_background_color': 'freezer_inuse_rack_css_background_color',
                                                 'freezer_inuse_rack_css_text_color': 'freezer_inuse_rack_css_text_color',
                                                 'freezer_empty_box_css_background_color': 'freezer_empty_box_css_background_color',
                                                 'freezer_empty_box_css_text_color': 'freezer_empty_box_css_text_color',
                                                 'freezer_inuse_box_css_background_color': 'freezer_inuse_box_css_background_color',
                                                 'freezer_inuse_box_css_text_color': 'freezer_inuse_box_css_text_color',
                                                 'freezer_empty_inventory_css_background_color': 'freezer_empty_inventory_css_background_color',
                                                 'freezer_empty_inventory_css_text_color': 'freezer_empty_inventory_css_text_color',
                                                 'freezer_inuse_inventory_css_background_color': 'freezer_inuse_inventory_css_background_color',
                                                 'freezer_inuse_inventory_css_text_color': 'freezer_inuse_inventory_css_text_color'})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = DefaultSiteCss.objects.get(default_css_label='default_css_label')
        self.assertIs(medna.was_added_recently(), True)


class CustomUserCssTestCase(TestCase):
    def setUp(self):
        CustomUserCss.objects.get_or_create(custom_css_label='custom_css_label',
                                            defaults={
                                                'css_selected_background_color': 'css_selected_background_color',
                                                'css_selected_text_color': 'css_selected_text_color',
                                                'freezer_empty_css_background_color': 'freezer_empty_css_background_color',
                                                'freezer_empty_css_text_color': 'freezer_empty_css_text_color',
                                                'freezer_inuse_css_background_color': 'freezer_inuse_css_background_color',
                                                'freezer_inuse_css_text_color': 'freezer_inuse_css_text_color',
                                                'freezer_empty_rack_css_background_color': 'freezer_empty_rack_css_background_color',
                                                'freezer_empty_rack_css_text_color': 'freezer_empty_rack_css_text_color',
                                                'freezer_inuse_rack_css_background_color': 'freezer_inuse_rack_css_background_color',
                                                'freezer_inuse_rack_css_text_color': 'freezer_inuse_rack_css_text_color',
                                                'freezer_empty_box_css_background_color': 'freezer_empty_box_css_background_color',
                                                'freezer_empty_box_css_text_color': 'freezer_empty_box_css_text_color',
                                                'freezer_inuse_box_css_background_color': 'freezer_inuse_box_css_background_color',
                                                'freezer_inuse_box_css_text_color': 'freezer_inuse_box_css_text_color',
                                                'freezer_empty_inventory_css_background_color': 'freezer_empty_inventory_css_background_color',
                                                'freezer_empty_inventory_css_text_color': 'freezer_empty_inventory_css_text_color',
                                                'freezer_inuse_inventory_css_background_color': 'freezer_inuse_inventory_css_background_color',
                                                'freezer_inuse_inventory_css_text_color': 'freezer_inuse_inventory_css_text_color'})

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = CustomUserCss.objects.get(custom_css_label='custom_css_label')
        self.assertIs(medna.was_added_recently(), True)
