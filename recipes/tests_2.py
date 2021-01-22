from django.contrib.auth import get_user_model
from django.test import TestCase, Client

import factory
from django.urls import reverse

User = get_user_model()


class UserFactory(factory.Factory):
    """
    Описываем класс для создания пользователей через библиотеку Factory Boy
    """

    class Meta:
        model = User

    username = 'test_profile',
    email = 'testmail@email.com',
    password = 'password_test'
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
        response = self.client.get(reverse('index_view'))
        self.assertEqual(
            response.status_code, 200,
            msg='Главная страница должна быть доступна')
        html = f'<a href="{reverse("login")}" class="nav__link link">Войти'
        self.assertIn(
            html, response.content.decode(),
            msg='У неавторизованного юзера в шапке должен быть пункт Войти')
        html = f'<a href="{reverse("recipe_new_view")}"' \
               f' class="nav__link link">Создать рецепт'
        self.assertNotIn(
            html, response.content.decode(),
            msg=('У неавторизованного юзера в шапке не должно быть'
                 ' пункта Создать рецепт'))

    def test_auth_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('index_view'))
        html = f'<a href="{reverse("login")}" class="nav__link link">Войти'
        self.assertNotIn(
            html, response.content.decode(),
            msg='У авторизованного юзера в шапке не должно быть пункта Войти')
        html = 'class="nav__link link">Изменить пароль'
        self.assertIn(
            html, response.content.decode(),
            msg='У залогиненного юзера в шапке должен быть пункт смены пароля')
        html = f'<a href="{reverse("recipe_new_view")}"' \
               f' class="nav__link link">Создать рецепт'
        self.assertIn(
            html, response.content.decode(),
            msg=('У залогиненного юзера в шапке должен быть пункт'
                 ' Создать рецепт'))
        counter = 'nav__badge" id="counter">'
        self.assertIn(
            counter, response.content.decode(),
            msg='У авторизованного юзера в шапке должен быть счетчик покупок')
