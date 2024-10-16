from django.test import TestCase
from .models import Cuisine

class CuisineModelTest(TestCase):
    def setUpTestData():
        Cuisine.objects.create(name = 'Dessert')
    
    def test_cuisine_name_label(self):
        cuisine = Cuisine.objects.get(id=1)

        field_label = cuisine._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_cuisine_name_length(self):
        cuisine = Cuisine.objects.get(id=1)
        max_length = cuisine._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)
