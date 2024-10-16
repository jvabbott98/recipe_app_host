from django.urls import path
from .views import home, recipe_list, recipe_detail

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', recipe_list, name='recipes'),
    path('recipe/<int:id>/', recipe_detail, name='recipe_detail'),
]