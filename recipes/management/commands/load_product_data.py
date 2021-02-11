import csv

from django.core.management.base import BaseCommand, no_translations

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Load ingredient data to database'

    @no_translations
    def handle(self, *args, **options):
        """
        The function adds ingredients and tags to the database on first deployment
        python manage.py load_product_data
        """

        with open('recipes/fixtures/ingredients.csv') as isfile:
            reader = csv.reader(isfile)
            for row in reader:
                title, unit = row
                Ingredient.objects.get_or_create(title=title, unit=unit)
        Tag.objects.get_or_create(name='Завтрак',
                                  slug='breakfast',
                                  checkbox_style='orange')
        Tag.objects.get_or_create(name='Обед',
                                  slug='lunch',
                                  checkbox_style='green')
        Tag.objects.get_or_create(name='Ужин',
                                  slug='dinner',
                                  checkbox_style='purple')
