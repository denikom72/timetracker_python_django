from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Role, Right, ManagedRole, CheckInCheckOut, QRCode

class UserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.role = Role.objects.create(name='employee')
        self.user.roles.add(self.role)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('password'))
        self.assertEqual(self.user.roles.count(), 1)
        self.assertEqual(self.user.roles.first().name, 'employee')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

class RoleModelTest(TestCase):
    def test_role_creation(self):
        role = Role.objects.create(name='manager')
        self.assertEqual(role.name, 'manager')

    def test_role_str(self):
        role = Role.objects.create(name='admin')
        self.assertEqual(str(role), 'admin')

class RightModelTest(TestCase):
    def test_right_creation(self):
        right = Right.objects.create(name='create_user')
        self.assertEqual(right.name, 'create_user')

    def test_right_str(self):
        right = Right.objects.create(name='delete_user')
        self.assertEqual(str(right), 'delete_user')

class ManagedRoleModelTest(TestCase):
    def setUp(self):
        self.manager_role = Role.objects.create(name='manager')
        self.employee_role = Role.objects.create(name='employee')
        self.create_right = Right.objects.create(name='create')
        self.managed_role = ManagedRole.objects.create(
            manager_role=self.manager_role,
            managed_role=self.employee_role
        )
        self.managed_role.rights.add(self.create_right)

    def test_managed_role_creation(self):
        self.assertEqual(self.managed_role.manager_role, self.manager_role)
        self.assertEqual(self.managed_role.managed_role, self.employee_role)
        self.assertEqual(self.managed_role.rights.count(), 1)
        self.assertEqual(self.managed_role.rights.first().name, 'create')

    def test_managed_role_str(self):
        self.assertEqual(str(self.managed_role), 'manager can manage employee')

class CheckInCheckOutModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.checkin = CheckInCheckOut.objects.create(user=self.user)

    def test_checkin_creation(self):
        self.assertEqual(self.checkin.user, self.user)
        self.assertIsNone(self.checkin.check_out_time)

    def test_checkin_str(self):
        self.assertIn('testuser', str(self.checkin))

class QRCodeModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.qrcode = QRCode.objects.create(user=self.user)

    def test_qrcode_creation(self):
        self.assertEqual(self.qrcode.user, self.user)
        self.assertIsNotNone(self.qrcode.qr_code)

    def test_qrcode_str(self):
        self.assertEqual(str(self.qrcode), 'QR Code for testuser')

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='password')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/index.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/login.html')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 302) # Redirects on successful login
        self.assertRedirects(response, reverse('index'))

    def test_user_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302) # Redirects on successful logout
        self.assertRedirects(response, reverse('index'))