from django.contrib.auth import get_user_model
from django.db import models

from .validators import image_size_validator

User = get_user_model()


class Tag(models.Model):
    """
    model Tags
    """

    name = models.CharField(
        verbose_name='Название тега',
        max_length=10,
    )
    slug = models.SlugField(
        'Слаг тэга',
        max_length=20,
        db_index=True
    )
    checkbox_style = models.CharField(
        'цвет тега',
        max_length=15
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    model Ingredient
    """
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        db_index=True
    )
    unit = models.CharField(
        'Единица измерения',
        max_length=20
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


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
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        blank=False,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
        validators=[image_size_validator]
    )
    description = models.TextField(
        verbose_name='Описание рецепта',
        max_length=1000,
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
        max_length=50
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='ингредиент',
        related_name="recipe_ingredient",
        through='Amount',
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

    def __str__(self):
        return self.name

    @property
    def ingredients_list(self):
        return list(self.ingredients.all())

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Amount(models.Model):
    """
    An intermediate model between the "Ingredient" and "Recipe" models,
    shows the quantity of ingredient in a particular recipe.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    units = models.PositiveIntegerField(
        'Количество/объем',
        default=0,
    )

    def __str__(self):
        return str(self.units)

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


class Purchase(models.Model):
    """
    model Purchase
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Покупатель"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Список рецептов",
        related_name="selected_recipes"
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return self.recipe.name
