from django.test import TestCase
from .models import Ingredient

class IngredientModelTest(TestCase):
    def setUpTestData():
        Ingredient.objects.create(name = 'Tomatoes')
    
    def test_ingredient_name_label(self):
        ingredient = Ingredient.objects.get(id=1)

        field_label = ingredient._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_ingredient_name_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)
