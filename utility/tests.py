from django.test import TestCase
from .models import Grant


# Create your tests here.
class GrantTestCase(TestCase):
    # formerly Project in field_sites.models
    def setUp(self):
        Grant.objects.create(grant_label="Maine-eDNA", grant_code="e")

    def test_was_added_recently(self):
        # test if date is added correctly
        medna = Grant.objects.get(grant_code="e")
        self.assertIs(medna.was_added_recently(), False)
