import csv

import factory
from django.test import Client, TestCase
from django.urls import reverse

from recipes.models import Amount, Ingredient, Recipe, Tag, User


def _create_recipe(author, name, tag):
    products = [Ingredient.objects.create(
        name=f'testIng{i}', unit=i) for i in range(2)]
    recipe = Recipe(author=author, name=name,
                    description='test test test', cook_time=5)
    recipe.save()
    recipe.tag.add(tag)
    for product in products:
        ingredient = Amount(
            recipe=recipe, ingredient=product, units=2)
        ingredient.save()
    return recipe


class UserFactory(factory.Factory):
    """
    Описываем класс для создания пользователей через библиотеку Factory Boy
    """

    class Meta:
        model = User

    username = 'Test user'
    email = 'test@test.test'
    password = '12345six'
    first_name = 'Test user first_name'


def _create_user(**kwargs):
    user = UserFactory.create(**kwargs)
    user.save()
    return user


class TestPageHeader(TestCase):
    """
    Тесты для шапки страницы.
    Для неавторизованного пользователя проверяет, что в шапке страницы есть
    меню для авторизации и нет для создания рецепта.
    Для авторизованного пользователя проверяет, что в шапке нет пункта
    авторизации, но есть для изменения пароля, появился пункт создания рецепта
    и счетчик количества рецептов в списке покупок.
    """

    def setUp(self):
        self.client = Client()
        self.user = _create_user()

    def test_not_auth_user(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(
            response.status_code, 200,
            msg='Главная страница должна быть доступна')
        html = f'<a href="{reverse("login")}" class="nav__link link">Войти'
        self.assertIn(
            html, response.content.decode(),
            msg='У неавторизованного юзера в шапке должен быть пункт Войти')
        html = f'<a href="{reverse("new_recipe")}"' \
               f' class="nav__link link">Создать рецепт'
        self.assertNotIn(
            html, response.content.decode(),
            msg=('У неавторизованного юзера в шапке не должно быть'
                 ' пункта Создать рецепт'))

    def test_auth_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        html = f'<a href="{reverse("login")}" class="nav__link link">Войти'
        self.assertNotIn(
            html, response.content.decode(),
            msg='У авторизованного юзера в шапке не должно быть пункта Войти')
        html = 'class="nav__link link">Изменить пароль'
        self.assertIn(
            html, response.content.decode(),
            msg='У залогиненного юзера в шапке должен быть пункт смены пароля')
        html = f'<a href="{reverse("new_recipe")}"' \
               f' class="nav__link link">Создать рецепт'
        self.assertIn(
            html, response.content.decode(),
            msg=('У залогиненного юзера в шапке должен быть пункт'
                 ' Создать рецепт'))
        counter = 'nav__badge" id="counter">'
        self.assertIn(
            counter, response.content.decode(),
            msg='У авторизованного юзера в шапке должен быть счетчик покупок')


class TestAuthorPage(TestCase):
    """
    Тесты для страницы профиля.
    Для неавторизованного пользователя проверяет, что страница доступна и на
    ней нет кнопки подписки.
    Для авторизованного пользователя проверяет, что в своем профиле нет кнопки
    подписке, а на чужом есть.
    """

    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        self.user2 = _create_user(username='Another test user',
                                  email='another@test.test',
                                  password='onetwo34',
                                  first_name='Another test user first_name')

    def test_not_auth_user(self):
        response = self.client.get(
            reverse('author', args=[self.user.id]))
        self.assertEqual(
            response.status_code, 200,
            msg='Неавторизованный юзер может просматривать профиль автора')
        subscribe_btn = '"light-blue button_size_auto" name="subscribe"'
        self.assertNotIn(
            subscribe_btn, response.content.decode(),
            msg=('В профиле для незалогиненного юзера не должно быть'
                 ' кнопки подписки'))

    def test_auth_user(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('author', args=[self.user.id]))
        self.assertEqual(
            response.status_code, 200,
            msg='Авторизованный пользователь может просматривать свой профиль')
        subscribe_btn = 'name="subscribe"'
        self.assertNotIn(
            subscribe_btn, response.content.decode(),
            msg=('В своем профиле для авторизованного юзера не должно'
                 ' быть кнопки подписки'))
        response2 = self.client.get(
            reverse('author', args=[self.user2.id]))

        self.assertIn(
            subscribe_btn, response2.content.decode(),
            msg=('Для авторизованного юзера в профиле другого юзера должна'
                 ' быть кнопка подписки'))


class TestRecipePage(TestCase):
    """
    Тесты страницы отдельного рецепта.
    Для неавторизованного пользователя проверяет, что страница доступна; на
    странице отсутствуют кнопки добавления в избранное, список покупок и
    подписки.
    Для авторизованного пользователя проверяет, что на странице появляются
    кнопки добавления в избранное и список покупок; на странице своего рецепта
    есть кнопка редактирования и нет кнопки добавления в подписки, а на
    странице чужого рецепта появляется кнопка подписки.
    """

    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        self.user2 = _create_user(username='Another test user',
                                  email='another@test.test',
                                  password='onetwo34',
                                  first_name='Another test user first_name')
        tag = Tag.objects.create(name='завтрак', slug='breakfast')
        self.recipe = _create_recipe(self.user, 'Test recipe', tag)
        self.recipe2 = _create_recipe(self.user2, 'Another recipe', tag)

    def test_not_auth_user(self):
        response = self.client.get(
            reverse('recipe', args=[self.recipe.id]))
        self.assertEqual(
            response.status_code, 200,
            msg=('Страница отдельного рецепта должна быть доступна'
                 ' неавторизованному юзеру'))
        elements = [
            ['избранное', 'button_style_none" name="favorites"'],
            ['подписки', 'light-blue button_size_auto" name="subscribe"'],
            ['покупок', 'button_style_blue" name="purchases"']
        ]
        for button, element in elements:
            self.assertNotIn(
                element,
                response.content.decode(),
                msg=(f'Кнопка {button} не должна быть на странице для '
                     'неавторизованного пользователя'))

    def test_auth_user(self):
        self.client.force_login(self.user)
        """Запрос страницы своего рецепта"""

        response1 = self.client.get(
            reverse('recipe', args=[self.recipe.id]))
        self.assertEqual(
            response1.status_code, 200,
            msg=('Страница отдельного рецепта должна быть доступна'
                 ' авторизованному юзеру'))
        elements = [
            ['избранное', 'name="favorites"'],
            ['список покупок', 'name="purchases"']
        ]
        for button, element in elements:
            self.assertIn(
                element, response1.content.decode(),
                msg=(f'Кнопка {button} должна быть на странице для'
                     ' залогиненного юзера'))
        subscibe_btn = 'name="subscribe"'
        self.assertNotIn(
            subscibe_btn, response1.content.decode(),
            msg='На странице своего рецепта не должна быть кнопка подписки')
        self.assertIn(
            'Редактировать рецепт', response1.content.decode(),
            msg='На странице своего рецепта должна быть кнопка редактировать'),
        elements.append(['подписка на автора', 'name="subscribe"'])

        """Запрос на страницу чужого рецепта"""

        response2 = self.client.get(
            reverse('recipe', args=[self.recipe2.id]))
        self.assertEqual(
            response2.status_code, 200,
            msg='Страница чужого рецепта доступна авторизованному юзеру')
        for button, element in elements:
            self.assertIn(element, response2.content.decode(), msg=(
                f'Кнопка {button} должна быть на '
                f'странице для залогиненного юзера'))
        self.assertNotIn(
            'Редактировать рецепт', response2.content.decode(),
            msg=('Кнопка редактирования не должна быть на странице'
                 ' чужого рецепта'))

