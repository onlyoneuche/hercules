import jwt
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from organisations.models import Organisation
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta


class TestUsers(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(email='testuser@example.com', password='testpass123',
                                        firstName='Test', lastName='User', phone='1234567890')

    # Unit Tests

    def test_token_expiration(self):
        """
        Check that the token expires at the correct time
        """
        user = User.objects.create_user(email='tests@example.com', password='testpass123', userId='test123', firstName='Test', lastName='User')
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        expected_expiry = timezone.now() + timedelta(minutes=60)
        self.assertAlmostEqual(access_token.payload['exp'], expected_expiry.timestamp(), delta=1)  # Allow 1 second difference

    def test_successful_login(self):
        """
        Check that correct user details are in the token and the response structure is correct
        """
        user = User.objects.create_user(email='tests@example.com', password='testpass123', userId='test123',
                                        firstName='Test', lastName='User', phone='1234567890')

        url = reverse('login')
        response = self.client.post(url, {'email': 'tests@example.com', 'password': 'testpass123'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Login successful')

        data = response.data['data']
        self.assertIn('accessToken', data)
        self.assertIn('user', data)

        user_data = data['user']
        self.assertEqual(user_data['userId'], user.userId)
        self.assertEqual(user_data['firstName'], user.firstName)
        self.assertEqual(user_data['lastName'], user.lastName)
        self.assertEqual(user_data['email'], user.email)
        self.assertEqual(user_data['phone'], user.phone)

        # Decode the access token to verify its payload
        decoded_token = jwt.decode(data['accessToken'], options={"verify_signature": False})

        self.assertEqual(decoded_token['user_id'], user.id)
        self.assertEqual(decoded_token['email'], user.email)
        self.assertEqual(decoded_token['firstName'], user.firstName)
        self.assertEqual(decoded_token['lastName'], user.lastName)

    def test_unsuccessful_login(self):
        """
        Check that the response structure is correct for unsuccessful login
        """
        user = User.objects.create_user(email='tests@example.com', password='testpass123', userId='test123',
                                        firstName='Test', lastName='User', phone='1234567890')

        url = reverse('login')
        response = self.client.post(url, {'email': 'tests@example.com', 'password': 'wrongpass'})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Authentication failed')
        self.assertEqual(response.data['statusCode'], 401)

    def test_register_user_successfully(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "securepass123",
            "phone": "+1234567890"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Registration successful')
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], 'John')

        # Verify default organisation
        user = User.objects.get(email='john@example.com')
        org = Organisation.objects.get(users=user)
        self.assertEqual(org.name, "John's Organisation")

    def test_register_missing_fields(self):
        url = reverse('register')
        data = {
            "userId": "testuser3",
            "firstName": "Alice",
            # Missing lastName
            "email": "alice@example.com",
            # Missing password
            "phone": "+1987654321"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)
        self.assertTrue(any(error['field'] == 'lastName' for error in response.data['errors']))
        self.assertTrue(any(error['field'] == 'password' for error in response.data['errors']))

    def test_register_duplicate_email(self):
        # First, register a user
        url = reverse('register')
        data = {
            "userId": "testuser4",
            "firstName": "Bob",
            "lastName": "Smith",
            "email": "bob@example.com",
            "password": "securepass123",
            "phone": "+1122334455"
        }
        self.client.post(url, data)

        # Try to register another user with the same email
        data['userId'] = 'testuser5'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)
        self.assertTrue(any(error['field'] == 'email' for error in response.data['errors']))

    def test_register_duplicate(self):
        # First, register a user
        url = reverse('register')
        data = {
            "firstName": "Charlie",
            "lastName": "Brown",
            "email": "charlie@example.com",
            "password": "securepass123",
            "phone": "+1555666777"
        }
        res1 = self.client.post(url, data)

        # Try to register another user with the same email
        data['email'] = 'charlie@example.com'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
