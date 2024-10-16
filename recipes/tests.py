from django.test import TestCase
from .models import Recipe, Ingredient
from ingredients.models import Ingredient
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import IngredientSearchForm

User = get_user_model()

class RecipeModelTests(TestCase):
    def test_create_recipe(self):
        recipe = Recipe.objects.create(name="Tea", cooking_time = 5)
        self.assertEqual(recipe.name, "Tea")
        self.assertEqual(recipe.cooking_time, 5)

    def test_retrieve_ingredients_from_recipe(self):
        recipe = Recipe.objects.create(name="Tea", cooking_time = 5)
        ingredient = Ingredient.objects.create(name="Water")

        recipe.ingredients.add(ingredient)

        retrieved_recipe = Recipe.objects.get(name = "Tea")
        self.assertEqual(retrieved_recipe.ingredients.first(), ingredient)

    def test_cooking_time_positive(self):
        recipe = Recipe.objects.create(name="Tea", cooking_time = -10)
        self.assertLess(recipe.cooking_time, 0)  

class RecipeListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
   
        cls.ingredient1 = Ingredient.objects.create(name='Chocolate')
        cls.ingredient2 = Ingredient.objects.create(name='Flour')
        
        cls.recipe1 = Recipe.objects.create(name='Chocolate Cake', cooking_time=30, difficulty='Easy')
        cls.recipe1.ingredients.add(cls.ingredient1, cls.ingredient2)
        
        cls.recipe2 = Recipe.objects.create(name='Chocolate Chip Cookies', cooking_time=25, difficulty='Intermediate')
        cls.recipe2.ingredients.add(cls.ingredient1)

    def test_login_required(self):
        response = self.client.get(reverse('recipes:recipes'))
        self.assertRedirects(response, '/login/?next=/recipes/') 

    def test_search_functionality(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipes:recipes'), {'ingredient_name': 'Chocolate', 'chart_type': '#1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chocolate Cake') 

    def test_pagination(self):
        for i in range(15):
            Recipe.objects.create(name=f'Recipe {i}', cooking_time=10, difficulty='Easy')

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipes:recipes') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe 10')  

class IngredientSearchFormTests(TestCase):

    def test_valid_form(self):
        form_data = {'ingredient_name': 'Chocolate', 'chart_type': '#1'}
        form = IngredientSearchForm(data=form_data)
        self.assertTrue(form.is_valid())  

    def test_invalid_form_empty(self):
        form_data = {}
        form = IngredientSearchForm(data=form_data)
        self.assertFalse(form.is_valid())  
        self.assertIn('ingredient_name', form.errors)  

    def test_ingredient_name_field_max_length(self):
        form_data = {'ingredient_name': 'A' * 256, 'chart_type': '#1'}
        form = IngredientSearchForm(data=form_data)
        self.assertFalse(form.is_valid())  
        self.assertIn('ingredient_name', form.errors)

