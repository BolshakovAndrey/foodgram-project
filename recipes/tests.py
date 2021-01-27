from io import BytesIO
from urllib.parse import urljoin

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .models import Recipe, User


class RecipePageTest(TestCase):

    def setUp(self):
        self.authorized_client = Client()
        self.unauthorized_client = Client()

        # create a test user
        self.user = User.objects.create_user(
            username="test_user",
            email="test@user.com",
            password="test_user_123456"
        )
        self.recipe = Recipe.objects.create(
            title='A good title',
            slug='test_slug',
            description='Content',
            author=self.user,
        )
        # create authorized/unauthorized user
        self.authorized_client.force_login(self.user)
        self.unauthorized_client.logout()
        # self.description = "Description test!"
        self.edit = "Changed text"

    def test_recipe_listing(self):
        self.assertEqual(f'{self.recipe.name}', 'A good title')
        self.assertEqual(f'{self.recipe.author}', 'test_user')
        self.assertEqual(f'{self.recipe.description}', 'Content')

    def test_recipe_list_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'index.html')

    def test_recipe_detail_view(self):
        response = self.client.get(self.recipe.get_absolute_url())
        no_response = self.client.get('/recipe/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'formRecipe.html')

    def urls(self):
        """
        Collects url of pages for testing
        """
        urls = [
            reverse("index"),
            reverse("recipe-detail",
                    kwargs={"username": self.user.username, "pk": 1}), ]
        return urls

    def check_recipe_content(self, url, user, slug, title, description, new_description):
        """
        Checks recipe content, author and title
        """
        self.authorized_client.get(url)
        self.assertEqual(user, self.user)
        self.assertEqual(title, self.title)
        self.assertEqual(slug, self.slug)
        self.assertEqual(description, self.description)
        self.assertEqual(new_description, self.edit)

    def tearDown(self):
        User.objects.filter(
            username="test_user",
            email="test@user.com",
            password="test_user_123456"
        ).delete()
        Recipe.objects.filter(
            description="Test recipe",
            author=self.user
        ).delete()

    def test_new_recipe_authorized_user(self):
        """
        Authorized user can new recipe.
        """
        response = self.authorized_client.get("recipe_create")
        self.assertEqual(response.status_code, 404)
        response = self.authorized_client.post(
            reverse("recipe-create"),
            data={"description": self.description},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recipe.objects.count(), 1)
        self.check_recipe_content(
            "recipe_create", self.user, self.description, self.edit)

    def test_new_recipe_unauthorized_user(self):
        """
        An unauthorized visitor cannot post a recipe (redirects to the login page).
        """
        response = self.unauthorized_client.post(
            reverse("recipe-create"),
            data={"description": self.description, },
            follow=True
        )
        # since it is impossible to add query parameters to reverse,
        # we will collect url
        url = urljoin(reverse("login"), "?next=/recipe_create/")
        self.assertRedirects(response, url)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_new_recipe_location(self):
        """
        After the recipe is published, a new recipe appears on the main page
        of the site (index), on the user"s personal page (profile),
        and on a separate recipe page (recipe_detail).
        """
        self.authorized_client.post(
            reverse("recipe-create"),
            data={"description": self.description},
            follow=True
        )
        for url in self.urls():
            with self.subTest(url=url):
                self.check_recipe_content(url, self.user, self.description, self.edit)

    def test_edit_recipe(self):
        """
        An authorized user can edit his recipe and its content will change on all linked pages.
        """
        recipe = Recipe.objects.create(description=self.description, author=self.user, )
        self.authorized_client.post(
            reverse("recipe-update",
                    kwargs={"username": recipe.author,
                            "pk": recipe.pk}),
            data={"description": self.edit},
            follow=True)
        # In the loop, go over all the url where the changes should be displayed:
        # home page, the authors profile and on the publication page
        for url in self.urls():
            with self.subTest(url=url):
                self.check_recipe_content(url, self.user, self.description, self.edit)

    def test_404(self):
        """
        Check whether the server returns the 404 code if the page is not found.
        """
        response = self.authorized_client.get("/some_trouble_url/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "misc/404.html")

    # def test_cache(self):
    #     """
    #     Checks whether the cache is working correctly.
    #     """
    #     with self.assertNumQueries(3):
    #         response = self.authorized_client.get(reverse("index"))
    #         self.assertEqual(response.status_code, 200)
    #         response = self.authorized_client.get(reverse("index"))
    #         self.assertEqual(response.status_code, 200)

    # def test_image_on_pages(self):
    #     """
    #     Checks that the image recipe is displayed correctly on the main page,
    #     profile page, and recipe page.
    #     """
    #     recipe = Recipe.objects.create(text="Recipe with image",
    #                                    author=self.user)
    #     img = BytesIO(
    #         b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
    #         b'\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
    #     image_name = 'foo_image.gif'
    #     img = SimpleUploadedFile(image_name, img.read(), content_type='image/gif')
    #     response = self.authorized_client.post(
    #         reverse("recipe_update",
    #                 kwargs={"username": self.user.username,
    #                         "pk": recipe.pk}),
    #         data={"description": "Recipe with image",
    #               "image": img}, follow=True)
    #     for url in self.urls():
    #         with self.subTest(url=url):
    #             self.assertEqual(response.status_code, 200)
    #             self.assertContains(response, "test_id")

    # def test_non_image(self):
    #     """
    #     Check the protection against downloading files in non-graphic formats
    #     """
    #     with open("urls.py") as file:
    #         response = self.authorized_client.post(
    #             "new", {"text": "Some text", "image": file}, follow=True)
    #         self.assertNotContains(response, "test_id")

    # def test_entry_appears_feed(self):
    #     """
    #     The new user record appears in the feed of those who subscribe to it
    #     and does not appear in the feed of those who do not subscribe to it.
    #     """
    #     self.recipe = Recipe.objects.create(text="Follow me!",
    #                                     author=self.user)
    #     self.authorized_client.post(reverse("recipe_create"),
    #                                 data={"Follow me!": self.text},
    #                                 follow=True)
    #     self.authorized_client.logout()
    #     follower = User.objects.create_user(username="follower", password="123456")
    #     self.authorized_client.force_login(follower)
    #     # follow
    #     self.authorized_client.get(reverse(
    #         "profile_follow", kwargs={"username": "test_user"}), follow=True)
    #     response_true = self.authorized_client.get(reverse("follow_index"))
    #     self.assertContains(response_true, "Follow me!")
    #     # unfollow
    #     self.authorized_client.get(reverse(
    #         "profile_unfollow", kwargs={"username": "test_user"}), follow=True)
    #     response_false = self.authorized_client.get(reverse("follow_index"))
    #     self.assertNotContains(response_false, "Follow me!")

    # def test_check_follow_auth(self):
    #     """
    #     Checks whether an authorized user can subscribe to others.
    #     """
    #     follower = User.objects.create_user(username="follower", password="12345")
    #     self.authorized_client.post(reverse(
    #         "profile_follow", kwargs={"username": follower.username, }))
    #     follow = Follow.objects.first()
    #     self.assertEqual(Follow.objects.count(), 1)
    #     self.assertEqual(follow.author, follower)
    #     self.assertEqual(follow.user, self.user)

    # def test_check_follow_non_unauth(self):
    #     """
    #     Checks whether an unauthorized user can't subscribe to others.
    #     """
    #     follower = User.objects.create_user(username="follower", password="12345")
    #     self.unauthorized_client.post(
    #         reverse("profile_follow",
    #                 kwargs={"username": follower.username}))
    #     self.assertEqual(follower.following.count(), 0)

    # def test_check_unfollow(self):
    #     """
    #     Checks whether the user can unsubscribe from others.
    #     """
    #     follower = User.objects.create_user(username="follower", password="12345")
    #     Follow.objects.create(user=self.user, author=follower)
    #     self.authorized_client.post(reverse(
    #         "profile_unfollow", kwargs={"username": follower.username, }))
    #     self.assertEqual(follower.following.count(), 0)

    # def test_auth_user_can_comment(self):
    #     """
    #     An authorized user can comment on posts.
    #     """
    #
    #     self.author = User.objects.create(username="leo", password="123456")
    #     self.post = Post.objects.create(text="Test post!", author=self.author)
    #     response = self.authorized_client.post(
    #         reverse("add_comment",
    #                 kwargs={"username": self.author,
    #                         "pk": self.post.pk}),
    #         data={"text": "Test comment",
    #               "author": self.user}, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.comment = Comment.objects.last()
    #     self.assertEqual(Comment.objects.count(), 1)
    #     self.assertEqual(self.comment.text, "Test comment")
    #
    # def test_non_auth_user_can_comment(self):
    #     """
    #     An unauthorized user can't comment on posts.
    #     """
    #     self.author = User.objects.create(username="leo", password="123456")
    #     self.post = Post.objects.create(text="Test post!", author=self.user)
    #     response = self.unauthorized_client.post(
    #         reverse("add_comment",
    #                 kwargs={"username": self.user.username,
    #                         "pk": self.post.pk}),
    #         data={"text": "Test comment",
    #               "author": self.user.id,
    #               "post": self.post.id})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(Comment.objects.count(), 0)
