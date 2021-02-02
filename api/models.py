from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Follow(models.Model):
    """
    model Follow
    """
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

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscriptions'
            )]


class Favorite(models.Model):
    """
    model favorite recipes
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
