from django.db import models
from django.contrib.auth.models import AbstractUser
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

    def __str__(self):
        return self.username

class CheckInCheckOut(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.check_in_time}"

class QRCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    qr_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR Code for {self.user.username}"