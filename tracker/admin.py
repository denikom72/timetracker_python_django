from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, Right, ManagedRole, CustomUser, CheckInCheckOut, QRCode

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (('Roles', {'fields': ('roles',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Roles', {'fields': ('roles',)}),)

admin.site.register(Role)
admin.site.register(Right)
admin.site.register(ManagedRole)
admin.site.register(CheckInCheckOut)
admin.site.register(QRCode)