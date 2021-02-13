import factory
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import resolve, reverse

from recipes.models import (Amount, Favorite, Follow, Ingredient, Recipe, Tag,
                            User)
from users.forms import UserCreationForm
from users.views import SignUp


class TestUserProfile(TestCase):

    def test_user_creation(self):
        """
        Тестирование создания профиля для зарегистрированного пользователя/суперпользователя
        """
        User = get_user_model()
        user = User.objects.create_user(
            username='test_profile',
            email='testmail@email.com',
            password='password_test'
        )
        self.assertEqual(user.username, 'test_profile')
        self.assertEqual(user.email, 'testmail@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='password_test'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupPageTests(TestCase):
    """
    Тестирование страницы регистрации
    """

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Регистрация')
        self.assertNotContains(
            self.response, 'I should not be on the page.')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/auth/signup/')
        self.assertEqual(
            view.func.__name__,
            SignUp.as_view().__name__
        )


def _create_recipe(author, name, tag):
    products = [Ingredient.objects.create(
        name=f'testIng{i}', unit=i) for i in range(2)]
    recipe = Recipe(
        author=author,
        name=name,
        description='test test test',
        slug='testtesttest',
        image='static/images/testCardImg.png',
        cook_time=5)
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
    password = '12345Test'
    first_name = 'Test user first_name'


def _create_user(**kwargs):
    user = UserFactory.create(**kwargs)
    user.save()
    return user


def _create_unauth_user(**kwargs):
    unauth_user = UserFactory.create(**kwargs).logout()
    unauth_user.save()
    return unauth_user

    return unauth_user


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
        html = f'class="nav__link link">Войти'
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
        html = f'class="nav__link link">Создать рецепт'
        self.assertIn(
            html, response.content.decode(),
            msg=('У залогиненного юзера в шапке должен быть пункт'
                 ' Создать рецепт'))
        counter = 'id="counter"'
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
                                  password='12345Another',
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
                                  password='12345Another',
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


class TestTagFilter(TestCase):
    """
    Тесты для фильтрации по тегам.
    Проверяет работу фильтров по тегам на главной странице,
    странице профиля и избранного.
    """

    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        self.client.force_login(self.user)
        tag1 = Tag.objects.create(name='завтрак', slug='breakfast',
                                  checkbox_style='orange')
        tag2 = Tag.objects.create(name='обед', slug='lunch',
                                  checkbox_style='green')
        for i in range(15):
            if i % 2 == 0:
                _create_recipe(self.user, f'recipe {i}', tag2)
            else:
                _create_recipe(self.user, f'recipe {i}', tag1)

    def test_filter(self):
        urls = [
            f'{reverse("index")}?tag=lunch',
            f'{reverse("index")}?tag=lunch&page=2',
            f'{reverse("author", args=[self.user.id])}?tag=lunch',
            f'{reverse("author", args=[self.user.id])}?tag=lunch&page=2',
        ]
        tag = 'card__item"><span class="badge badge_style_orange">завтрак'
        for url in urls:
            resp = self.client.get(url)
            self.assertNotIn(
                tag, resp.content.decode(),
                msg=('Фильтры по тегам должны работать правильно на'
                     f'{resp.request["PATH_INFO"]}, а также при пагинации'))
        self.client.force_login(self.user)
        for i in range(1, 3):
            self.client.post(
                reverse('favorites'), data={'id': f'{i}'},
                content_type='application/json')
        resp = self.client.get(f'{reverse("favorites")}?tag=lunch')
        self.assertNotIn(
            tag, resp.content.decode(),
            msg='Фильтры должны правильно работать на странице с избранным')


class TestFollowPage(TestCase):
    """
    Тесты страницы подписок.
    Для авторизованного пользователя проверяется, что страница доступна и что
    на странице присутствует автор добавленный в подписки.
    """

    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        self.user2 = _create_user(username='Another test user',
                                  email='another@test.test',
                                  password='12345Another',
                                  first_name='Another test user first_name')
        tag = Tag.objects.create(name='завтрак', slug='breakfast')
        self.recipe = _create_recipe(self.user, 'Test recipe', tag)
        Follow.objects.create(user=self.user2, author=self.user)

    def test_auth_user(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('subscriptions'), follow=True)
        self.assertEqual(
            response.status_code, 200,
            msg='Страница подписок доступна авторизованному юзеру')
        self.assertIn(
            'Test user first_name', response.content.decode(),
            msg='На странице подписок должен быть добавленный автор')


class TestFollowButton(TestCase):
    """
    Тесты страницы подписки.
    Для авторизованного пользователя проверяется, что страница доступна и что
    добавление и удаление подписки на автора происходит корректно.
    """

    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        self.user2 = _create_user(username='Another test user',
                                  email='another@test.test',
                                  password='12345Another',
                                  first_name='Another test user first_name')

        self.data = {'id': f'{self.user2.id}'}

    def test_auth_user_add(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_subscription'), data=self.data,
            content_type='application/json', follow=True)
        data_incoming = response.json()
        self.assertIsInstance(data_incoming, dict,
                              msg='Проверьте, что на запрос приходит словарь')
        self.assertIn('success', data_incoming,
                      msg='Проверьте, что словарь содержит ключ "success"')
        self.assertEqual(data_incoming['success'], True,
                         msg='При добавлении в подписки значение ключа = True')
        self.assertTrue(Follow.objects.filter(
            user=self.user, author=self.user2).exists(),
                        msg='Должна создаваться соответствующая запись в бд')
        repeat_response = self.client.post(
            reverse('add_subscription'), data=self.data,
            content_type='application/json', follow=True)
        data_incoming_2 = repeat_response.json()
        self.assertEqual(
            data_incoming_2['success'], False,
            msg='При попытке повторно добавить в подписки success = False')
        self.assertEqual(Follow.objects.filter(
            user=self.user, author=self.user2).count(), 1,
                         msg='Не должна создаваться повторная запись в бд')

    def test_auth_user_delete(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('subscriptions'), data=self.data,
            content_type='application/json', follow=True)
        del_response = self.client.delete(
            reverse('remove_subscriptions', args=[self.user2.id]),
            content_type='application/json', follow=True)
        data_incoming = del_response.json()
        self.assertIsInstance(data_incoming, dict,
                              msg='На запрос должен приходить словарь')
        self.assertIn('success', data_incoming,
                      msg='Словарь должен содержать ключ "success"')
        self.assertEqual(data_incoming['success'], True,
                         msg='При удалении из подписок значение ключа = True')
        self.assertFalse(Follow.objects.filter(
            user=self.user, author=self.user2).exists(),
                         msg='Должна удаляться соответствующая запись в бд')


class TestFavoriteButton(TestCase):
    """
    Тесты страницы избранное.
    Для авторизованного пользователя проверяется, что страница доступна и что
    добавление и удаление рецепта происходит корректно.
    """

    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        tag = Tag.objects.create(name='завтрак', slug='breakfast')
        self.recipe = _create_recipe(self.user, 'Cool recipe', tag)
        self.data = {'id': f'{self.recipe.id}'}

    def test_auth_user_add(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('add_favorite'), data=self.data,
            content_type='application/json', follow=True)
        data_incoming = response.json()
        self.assertIsInstance(data_incoming, dict,
                              msg='На запрос должен приходить словарь')
        self.assertIn('success', data_incoming,
                      msg='Словарь должен содержать ключ "success"')
        self.assertEqual(data_incoming['success'], True,
                         msg='При добавлении в избранное success = True')
        self.assertTrue(Favorite.favorite.get(
            user=self.user, recipe=self.recipe.id),
            msg='Должна создаваться соответствующая запись в бд')

        repeat_response = self.client.post(
            reverse('add_favorite'), data=self.data,
            content_type='application/json', follow=True)
        data_incoming_2 = repeat_response.json()
        self.assertEqual(
            data_incoming_2['success'], False,
            msg='При попытке повторно добавить '
                'в избранное success = False')

    def test_auth_user_delete(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse('favorites'), data=self.data,
            content_type='application/json', follow=True)
        del_response = self.client.delete(
            reverse('remove_favorites', args=[self.recipe.id]),
            content_type='application/json', follow=True)
        data_incoming = del_response.json()
        self.assertIsInstance(data_incoming, dict,
                              msg='На запрос должен приходить словарь')
        self.assertIn('success', data_incoming,
                      msg='Словарь должен содержать ключ "success"')
        self.assertEqual(data_incoming['success'], True,
                         msg='При удалении из избранного success = True')
        self.assertFalse(Favorite.favorite.filter(
            recipe=self.recipe, user=self.user).exists(),
                         msg='Должна удаляться соответствующая запись в бд')
