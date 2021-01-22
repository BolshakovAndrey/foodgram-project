from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Recipe


class RecipeTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.recipe = Recipe.objects.create(
            title='A good title',
            description='Nice description content',
            author=self.user,
        )

    def test_string_representation(self):
        recipe = Recipe(title='A sample title')
        self.assertEqual(str(recipe), recipe.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), '/recipe/1/')

    def test_recipe_content(self):
        self.assertEqual(f'{self.recipe.title}', 'A good title')
        self.assertEqual(f'{self.recipe.author}', 'testuser')
        self.assertEqual(f'{self.recipe.description}', 'Nice description content')

    def test_recipe_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice description content')
        self.assertTemplateUsed(response, 'home.html')

    def test_recipe_detail_view(self):
        response = self.client.get('/recipe/1/')
        no_response = self.client.get('/recipe/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'formChangeRecipe.html')

    def test_recipe_create_view(self):
        response = self.client.recipe(reverse('recipe_create'), {
            'title': 'New title',
            'description': 'New text',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_recipe_update_view(self):
        response = self.client.recipe(reverse('recipe_update', args='1'), {
            'title': 'Updated title',
            'description': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)

    def test_recipe_delete_view(self):
        response = self.client.recipe(
            reverse('recipe_delete', args='1'))
        self.assertEqual(response.status_code, 302)
