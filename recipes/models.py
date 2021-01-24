from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .validators import image_size_validator

User = get_user_model()


class Tag(models.Model):
    """
    model Tags
    """
    TAGS = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин')
    ]
    tag_options = {
        'breakfast': ['orange', 'Завтрак'],
        'lunch': ['green', 'Обед'],
        'dinner': ['purple', 'Ужин']
    }
    title = models.CharField(
        verbose_name='Название тега',
        max_length=10,
        choices=TAGS,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    @property
    def tag_color(self):
        return self.tag_options[self.title[0]]

    @property
    def tag_name(self):
        return self.tag_options[self.title[1]]

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """
    model Ingredient
    """
    title = models.CharField(
        'Название ингредиента',
        max_length=200,
        db_index=True
    )
    dimension = models.SmallIntegerField(
        'Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('title',)
        constraints = [models.UniqueConstraint(
            fields=['title'],
            name='unique_ingredient')
        ]

    def __str__(self):
        return self.title


class RecipeManager(models.Manager):
    """
    The manager implements sorting by tags.
    """
    def filter_by_tags(self, tag):
        if tag:
            queryset = Recipe.recipes.filter(tag__name__in=tag.split(",")).distinct()
        else:
            queryset = Recipe.recipes.all()
        return queryset


class Recipe(models.Model):
    """
    model Recipe
    """
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipe_author',
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        blank=False,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='media/',
        validators=[image_size_validator]
    )
    description = models.TextField(
        verbose_name='Описание рецепта',
        max_length=400,
        blank=False
    )
    cook_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='в минутах',
        null=True
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        db_index=True,
        null=False,
        unique=True,
        max_length=50
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        verbose_name='ингредиент',
        related_name="recipe_ingredient",
        through='IngredientQuantity',
        through_fields=('recipe', 'ingredient')
    )
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipe_tag'
    )

    recipes = RecipeManager()

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return list(self.tag.all())

    @property
    def ingredients_list(self):
        return list(self.ingredient.all())

    # def get_absolute_url(self):
    #     return reverse('recipe_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientQuantity(models.Model):
    """
    An intermediate model between the "Ingredient" and "Recipe" models,
    shows the quantity of ingredient in a particular recipe.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_quantity'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_quantity'
    )
    quantity = models.PositiveIntegerField(
        'Количество/объем',
        default=0
    )

    def __str__(self):
        return str(self.quantity)

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


class PurchaseManager(models.Manager):
    """
    Interface for models that can make queries to the database
    """

    def get_shopper(self, user):
        try:
            return super().get_queryset().get(user=user)
        except ObjectDoesNotExist:
            purchase = Purchase(user=user)
            purchase.save()
            return purchase

    def get_selected_recipes(self, user):
        return super().get_queryset().get(user=user).recipes.all

    def count_selected_recipes(self, user):
        return super().get_queryset().get(user=user).recipes.count()


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Покупатель"
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Список рецептов",
        related_name="selected_recipes"
    )
    purchase = PurchaseManager()

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return self.recipes.title
