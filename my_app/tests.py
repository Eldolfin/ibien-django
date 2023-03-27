from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import SellForm
from .models import Sell, User, UserProfile


class IndexViewTestCase(TestCase):
    def setUp(self):
        """
        This method disables the SECURE_SSL_REDIRECT setting for the test.
        It's needed otherwise the tests will fail.
        """
        settings_manager = override_settings(SECURE_SSL_REDIRECT=False)
        settings_manager.enable()
        self.addCleanup(settings_manager.disable)

    def test_no_items(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_posts_list'], [])

    def test_one_item(self):
        user = User.objects.create(username="test_user", password="123")

        userprofile = UserProfile.objects.create(
            user=user, location="Test Location, Ireland")

        sell = Sell.objects.create(
            name="Test Item", price=100, seller=userprofile,
            description="This is an example item")

        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            [sell],
        )

    def test_ten_items(self):
        num_items = 10

        user = User.objects.create(username="test_user", password="123")

        userprofile = UserProfile.objects.create(
            user=user, location="Test Location, Ireland")

        sells = []
        for i in range(num_items):
            sell = Sell.objects.create(
                name="Test Item", price=100, seller=userprofile,
                description="This is an example item")
            sells.append(sell)

        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            reversed(sells),
        )

    def test_too_many_items(self):
        num_items = 100

        user = User.objects.create(username="test_user", password="123")

        userprofile = UserProfile.objects.create(
            user=user, location="Test Location, Ireland")

        sells = []
        for i in range(num_items):
            sell = Sell.objects.create(
                name="Test Item", price=100, seller=userprofile,
                description="This is an example item")
            sells.append(sell)

        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_posts_list'],
            reversed(sells[-10:]),  # it's only showing the latest 10 items
        )


class SellViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'user', 'user@example.com', 'password')
        self.user_profile = UserProfile.objects.create(
            user=self.user, location='Location')
        self.client.login(username='user', password='password')

        # disable SECURE_SSL_REDIRECT for the tests
        settings_manager = override_settings(SECURE_SSL_REDIRECT=False)
        settings_manager.enable()
        self.addCleanup(settings_manager.disable)

    def test_sell_view(self):
        response = self.client.get(reverse('sell'))
        # Test that the view returns a successful response and the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_app/sell.html')
        # Test that the view contains the SellForm
        self.assertIsInstance(response.context['form'], SellForm)
        # Test that the view creates a Sell object when form is submitted
        data = {'name': 'Sell1', 'price': 10, 'description': 'Description',
                'image': '', 'location': 'Location'}
        response = self.client.post(reverse('sell'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Sell.objects.count(), 1)


class MySellsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'user', 'user@example.com', 'password')
        self.user_profile = UserProfile.objects.create(
            user=self.user, location='Location')
        self.client.login(username='user', password='password')
        # Create 2 Sell objects to test the view
        self.sell1 = Sell.objects.create(
            name='Sell1', price=10, description='Description', seller=self.user_profile)
        self.sell2 = Sell.objects.create(
            name='Sell2', price=10, description='Description', seller=self.user_profile)

        # disable SECURE_SSL_REDIRECT for the tests
        settings_manager = override_settings(SECURE_SSL_REDIRECT=False)
        settings_manager.enable()
        self.addCleanup(settings_manager.disable)

    def test_my_sells_view(self):
        response = self.client.get(reverse('my_sells'))
        # Test that the view returns a successful response and the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_app/sell_list.html')
        # Test that the view returns 2 objects
        self.assertEqual(len(response.context['my_sells_list']), 2)


class EditSellViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.userprofile = UserProfile.objects.create(
            user=self.user, location='Testville')
        self.sell = Sell.objects.create(
            name='Test Item', price=20.0, description='Test description',
            image='default.png', location='Testville', seller=self.userprofile)
        self.url = reverse('edit_sell', kwargs={'pk': self.sell.pk})

        # disable SECURE_SSL_REDIRECT for the tests
        settings_manager = override_settings(SECURE_SSL_REDIRECT=False)
        settings_manager.enable()
        self.addCleanup(settings_manager.disable)

    def test_view_success_status_code(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_view_renders_correct_template(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'my_app/edit_item.html')

    def test_view_returns_404_for_nonexistent_sell(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(
            reverse('edit_sell', kwargs={'pk': self.sell.pk + 1}))
        self.assertEqual(response.status_code, 404)

    def test_view_updates_sell_for_valid_data(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'name': 'Updated Item',
            'price': 25.0,
            'description': 'Updated description',
            'image': '',
        }
        form = SellForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/my_sells/')
        self.sell.refresh_from_db()
        self.assertEqual(self.sell.name, 'Updated Item')
        self.assertEqual(self.sell.price, 25.0)
        self.assertEqual(self.sell.description, 'Updated description')

    def test_view_rejects_sell_for_invalid_data(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'name': '',
            'price': -5.0,
            'description': 'Test description',
            'image': '',
        }
        form = SellForm(data=data)
        self.assertFalse(form.is_valid())
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_app/edit_item.html')
        self.sell.refresh_from_db()
        self.assertEqual(self.sell.name, 'Test Item')
        self.assertEqual(self.sell.price, 20.0)
        self.assertEqual(self.sell.description, 'Test description')

    def test_view_protects_against_redirection_attack(self):
        """
        Test that SellView protects against redirection attacks
        """
        # create a fake URL that tries to redirect the user to an external website
        fake_url = "https://example.com"

        # create a POST request with the fake URL as the redirect URL
        data = {
            'name': 'Test Item',
            'description': 'This is a test item',
            'price': 10,
            'redirect_url': fake_url
        }
        response = self.client.post(self.url, data=data, follow=True)

        # assert that the response is a 200 OK
        self.assertEqual(response.status_code, 200)

        # assert that the response does not contain the fake URL
        self.assertNotContains(response, fake_url)

    def test_sql_injection_prevention(self):
        """
        Test that SellView prevents SQL injection attacks
        """
        # create a malicious SQL injection payload
        sql_injection_payload = "'; DROP TABLE my_app_sell;"

        # create a POST request with the SQL injection payload as the name parameter
        data = {
            'name': sql_injection_payload,
            'description': 'This is a test item',
            'price': 10,
            'location': 'Testville'
        }
        response = self.client.post(reverse('sell'), data=data, follow=True)

        # assert that the sell object was not deleted
        self.assertEqual(Sell.objects.count(), 1)


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            location='Test Location'
        )
        self.sell = Sell.objects.create(
            name='Test Item',
            price=10.0,
            description='Test Description',
            location='Test Location',
            seller=self.user_profile
        )

    def test_user_profile_creation(self):
        self.assertEqual(str(self.user_profile), self.user.username)

    def test_sell_creation(self):
        self.assertEqual(str(self.sell), self.sell.name)
