from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = (
            'title', 'image', 'description', 'tag', 'cook_time'
        )
        widgets = {'tag': forms.CheckboxSelectMultiple(), }