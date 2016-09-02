from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Right(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., create, read, update, delete

    def __str__(self):
        return self.name

class ManagedRole(models.Model):
    manager_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='can_manage')
    managed_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='is_managed_by')
    rights = models.ManyToManyField(Right)

    def __str__(self):
        return f"{self.manager_role} can manage {self.managed_role}"

class CustomUser(AbstractUser):
    roles = models.ManyToManyField(Role, blank=True)

    @property
    def is_manager(self):
        manager_roles = ManagedRole.objects.values_list('manager_role', flat=True)
        user_roles = self.roles.all()
        return any(role.id in manager_roles for role in user_roles)

    @property
    def managed_users(self):
        if not self.is_manager:
            return CustomUser.objects.none()

        managed_roles_qs = ManagedRole.objects.filter(manager_role__in=self.roles.all())
        managed_roles_ids = managed_roles_qs.values_list('managed_role_id', flat=True)
        
        return CustomUser.objects.filter(roles__id__in=managed_roles_ids)

    def __str__(self):
        return self.username

class CheckInCheckOut(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.check_out_time:
            return (self.check_out_time - self.check_in_time).total_seconds() / 3600
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.check_in_time}"

class QRCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    qr_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR Code for {self.user.username}"

class TimeEntryLog(models.Model):
    entry = models.ForeignKey(CheckInCheckOut, on_delete=models.CASCADE)
    edited_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)
    old_check_in = models.DateTimeField()
    new_check_in = models.DateTimeField()
    old_check_out = models.DateTimeField(null=True, blank=True)
    new_check_out = models.DateTimeField(null=True, blank=True)