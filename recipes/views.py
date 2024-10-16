from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import IngredientSearchForm
from .models import Ingredient, Recipe
import pandas as pd
from .utils import get_chart
from django.db.models import Count


@login_required
def recipe_list(request):
    form = IngredientSearchForm(request.POST or None)
    recipes_df = None
    chart = None

    # Start with an empty queryset
    qs = Recipe.objects.annotate(number_of_ingredients=Count('ingredients'))  # Annotate all recipes

    if request.method == 'POST':
        chart_type = request.POST.get('chart_type')  # Get chart type from POST
        
        # Handle the "View All Recipes" case
        if 'view_all' in request.POST:
            # Use the already annotated queryset for all recipes
            object_list = qs  # All recipes with ingredient counts
        else:
            # Handle search for ingredients
            ingredient_name = request.POST.get('ingredient_name')
            # Filter recipes by ingredient
            qs = qs.filter(ingredients__name__icontains=ingredient_name)  # Filter the annotated queryset
            object_list = qs  # Update object_list to the filtered queryset

        # Create a DataFrame from the annotated queryset for rendering
        recipes_df = pd.DataFrame(object_list.values('name', 'cooking_time', 'difficulty', 'number_of_ingredients'))

        if not recipes_df.empty:  # Check if the DataFrame has any data
            print('recipes_df contents:\n', recipes_df)

            if 'difficulty' in recipes_df.columns:
                difficulty_counts = recipes_df['difficulty'].value_counts().to_list()
                difficulty_labels = recipes_df['difficulty'].value_counts().index.tolist()
            else:
                print("Column 'difficulty' not found in recipes_df")
                difficulty_counts = []
                difficulty_labels = []

            print('difficulty_counts:', difficulty_counts)
            print('difficulty_labels:', difficulty_labels)

            chart = get_chart(chart_type, recipes_df, difficulty_levels=difficulty_labels, difficulty_counts=difficulty_counts)
            recipes_df = recipes_df.to_html()

            print('recipes_df HTML:\n', recipes_df)

    else:
        # If not a POST request, show all recipes
        object_list = qs  # Default to showing all recipes



    context = {
        'form': form,
        'object_list': object_list,
        'recipes_df': recipes_df,
        'chart': chart,
    }

   
    return render(request, 'recipes/main.html', context)

@login_required
def recipe_detail(request, id):
    object = get_object_or_404(Recipe, id=id)
    return render(request, 'recipes/recipe_detail.html', {'object': object})

def home(request):
    return render(request, 'recipes/recipes_home.html')
