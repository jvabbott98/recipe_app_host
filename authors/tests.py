from django.test import TestCase
from .models import Author

class AuthorModelTest(TestCase):
    def setUpTestData():
        Author.objects.create(name = 'James')
    
    def test_author_name_label(self):
        author = Author.objects.get(id=1)

        field_label = author._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_author_name_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)
