from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from recipes.models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'name', 'image', 'description', 'tag', 'cook_time'
        )
        widgets = {'tag': forms.CheckboxSelectMultiple(), }


class TagsFilter(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple(),
        to_field_name='slug'
    )