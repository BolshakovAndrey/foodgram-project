from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from .validators import image_size_validator

User = get_user_model()


class Tag(models.Model):
    """
    model Tags
    """

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'checkbox_style'],
                name='unique_tag'
            )]

    name = models.CharField(
        verbose_name='Название тега',
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name='Слаг тэга',
        max_length=20,
        db_index=True
    )
    checkbox_style = models.CharField(
        verbose_name='цвет тега',
        max_length=20
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    model Ingredient
    """

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
        db_index=True
    )
    unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=20
    )

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    """
    The manager implements filtering by tags
    """

    def filter_by_tags(self, tag):
        if tag:
            queryset = Recipe.objects.filter(
                tag__name__in=tag.split(
                    ',')).distinct()
        else:
            queryset = Recipe.objects.all()
        return queryset


class Recipe(models.Model):
    """
    model Recipe
    """

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipe_authors',
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
        default='static/images/testCardImg.png',
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
        null=True,
        validators=[MinValueValidator(1)]

    )
    slug = models.SlugField(
        verbose_name='Слаг',
        db_index=True,
        null=False,
        max_length=50
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipe_ingredients',
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
        verbose_name='Тэг',
        related_name='recipe_tags'
    )

    recipes = RecipeManager()

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Amount(models.Model):
    """
    An intermediate model between the "Ingredient" and "Recipe" models,
    shows the quantity of ingredient in a particular recipe.
    """

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='amount_recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    units = models.PositiveIntegerField(
        verbose_name='Количество/объем',
        default=0,
    )

    def __str__(self):
        return str(self.units)


class Purchase(models.Model):
    """
    model Purchase
    """

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Покупатель",
        related_name="purchase_users"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Список рецептов",
        related_name="selected_recipes"
    )

    def __str__(self):
        return self.recipe.name


class Follow(models.Model):
    """
    model Follow
    """

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def clean(self):
        if self.author == self.user:
            raise ValidationError(
                'Пользователь не может подписываться сам на себя'
            )

    def __str__(self):
        return f'{self.user.name} подписался на {self.author.name}'


class FavoriteManager(models.Manager):
    """Менеджер модели избранное."""

    def get_favorites(self, user):
        """
        Фукция возвращает QuerySet рецептов добавленных в избранное. Если таких
        рецепров нет возвращает пустой лист.
        """

        try:
            return super().get_queryset().get(
                user=user).recipes.all()
        except ObjectDoesNotExist:
            return []


class Favorite(models.Model):
    """
    model favorite recipes
    """

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            ),
        ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_users',
        verbose_name='Любимый автор'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Любимый рецепт'
    )

    favorite = FavoriteManager()
