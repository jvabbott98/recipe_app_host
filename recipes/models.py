from django.db import models
from ingredients.models import Ingredient
from authors.models import Author
from cuisines.models import Cuisine
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse


class Recipe(models.Model):
    name = models.CharField(max_length=120)

    # Create one-to-one relationship with the Author model
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    cooking_time = models.IntegerField(help_text='In minutes')

    description = models.TextField(default='No description...')
    directions = models.TextField(default='No directions....')

    # Allows recipe to contain multiple ingredients and cuisine types.
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients')
    cuisine = models.ManyToManyField(Cuisine, related_name='cuisine')


    difficulty = models.CharField(max_length=20, blank=True)

    

    # Calculates difficulty based on cooking time and number of ingredients.
    def calculate_difficulty(self):
        ingredient_count = self.ingredients.count()
        if self.cooking_time < 10:
            if ingredient_count < 4:
                return 'Easy'
            else:
                return 'Medium'
        else:
            if ingredient_count < 4:
                return 'Intermediate'
            else:
                return 'Hard'

    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'id': self.pk})

    def __str__(self):
        return str(self.name)

# Calculates and sets the difficulty upon saving a recipe's information
@receiver(post_save, sender=Recipe)
def set_difficulty(sender, instance, created, **kwargs):
    if created:  
        instance.difficulty = instance.calculate_difficulty()
        instance.save(update_fields=['difficulty']) 