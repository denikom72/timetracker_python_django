from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Role, Right, ManagedRole, CheckInCheckOut, QRCode, TimeEntryLog
from django.utils import timezone
from datetime import timedelta

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
        self.admin_user = CustomUser.objects.create_superuser(username='admin', password='password')

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
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_time_history_view_authenticated(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('time_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/time_history.html')

    def test_time_history_view_unauthenticated(self):
        response = self.client.get(reverse('time_history'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('time_history')}")

    def test_export_monthly_timesheet_admin(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('export_monthly_timesheet'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_export_monthly_timesheet_non_admin(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('export_monthly_timesheet'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_add_time_entry_admin(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('add_time_entry'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/add_time_entry.html')

    def test_add_time_entry_non_admin(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('add_time_entry'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

class ManagerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.manager_role = Role.objects.create(name='manager')
        self.employee_role = Role.objects.create(name='employee')
        self.manager_user = CustomUser.objects.create_user(username='manager', password='password')
        self.manager_user.roles.add(self.manager_role)
        self.employee_user = CustomUser.objects.create_user(username='employee', password='password')
        self.employee_user.roles.add(self.employee_role)
        ManagedRole.objects.create(manager_role=self.manager_role, managed_role=self.employee_role)
        self.entry = CheckInCheckOut.objects.create(
            user=self.employee_user,
            check_in_time=timezone.now() - timedelta(hours=2),
            check_out_time=timezone.now()
        )

    def test_team_timesheet_manager(self):
        self.client.login(username='manager', password='password')
        response = self.client.get(reverse('team_timesheet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/team_timesheet.html')

    def test_team_timesheet_non_manager(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('team_timesheet'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_view_user_timesheet_manager(self):
        self.client.login(username='manager', password='password')
        response = self.client.get(reverse('view_user_timesheet', args=[self.employee_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/view_user_timesheet.html')

    def test_edit_time_entry_manager(self):
        self.client.login(username='manager', password='password')
        response = self.client.get(reverse('edit_time_entry', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/edit_time_entry.html')

    def test_edit_time_entry_post_manager(self):
        self.client.login(username='manager', password='password')
        new_check_in_time = (timezone.now() - timedelta(hours=3)).replace(second=0, microsecond=0)
        response = self.client.post(reverse('edit_time_entry', args=[self.entry.id]), {
            'check_in_time': new_check_in_time.strftime('%Y-%m-%dT%H:%M'),
            'check_out_time': self.entry.check_out_time.strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_user_timesheet', args=[self.employee_user.id]))
        self.entry.refresh_from_db()
        self.assertAlmostEqual(self.entry.check_in_time, new_check_in_time, delta=timedelta(seconds=1))
        self.assertTrue(TimeEntryLog.objects.filter(entry=self.entry).exists())