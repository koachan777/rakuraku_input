from django.contrib import admin
from .models import TankModel, User, WaterQualityModel

class UserAdmin(admin.ModelAdmin):
    list_display = ("account_id", "is_superuser")
    readonly_fields = ('created_at', 'updated_at')
    ordering = ("-updated_at",)

    fieldsets = (
        (None, {"fields": ("account_id", "password", "is_active", "created_at", "updated_at")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "user_permissions")}),
    )

admin.site.register(User, UserAdmin)  # Userモデルを登録
admin.site.register(TankModel)  # Userモデルを登録
admin.site.register(WaterQualityModel)
