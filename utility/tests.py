from django.test import TestCase
from .models import Grant, Project, ProcessLocation


# Create your tests here.
class GrantTestCase(TestCase):
    # formerly Project in field_sites.models
    def setUp(self):
        Grant.objects.create(grant_label="Maine-eDNA", grant_code="e")

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Grant.objects.get(grant_code="e")
        self.assertIs(medna.was_added_recently(), True)


class ProjectTestCase(TestCase):
    # formerly Project in field_sites.models
    def setUp(self):
        # Grant.objects.create(grant_label="Maine-eDNA", grant_code="e")
        grant_name = Grant.objects.filter()[:1].get()
        Project.objects.create(project_label="Community Science", project_code="prj_commsci", grant_name=grant_name)

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Project.objects.get(project_code="prj_commsci")
        self.assertIs(medna.was_added_recently(), True)


class ProcessLocationTestCase(TestCase):
    # formerly Project in field_sites.models
    def setUp(self):
        ProcessLocation.objects.create(process_location_name="CORE",
                                       affiliation="UMaine",
                                       process_location_url="https://www.test.com",
                                       phone_number="999-867-5309",
                                       location_email_address="test@test.com",
                                       point_of_contact_email_address="test@test.com",
                                       point_of_contact_first_name="test first",
                                       point_of_contact_last_name="test last",
                                       location_notes="this is a test")

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = ProcessLocation.objects.get(process_location_name="CORE")
        self.assertIs(medna.was_added_recently(), True)
