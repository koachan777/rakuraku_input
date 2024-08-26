from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, account_id, password, **extra_fields):
        user = self.model(account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            account_id=account_id,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, account_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            account_id=account_id,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):

    account_id = models.CharField(
        verbose_name=_("account_id"),
        unique=True,
        max_length=10
    )
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuser"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created_at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated_at"),
        auto_now=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'account_id'  # ログイン時、ユーザー名の代わりにaccount_idを使用
    REQUIRED_FIELDS = []  # スーパーユーザー作成時に必要なフィールドはなし

    def __str__(self):
        return self.account_id

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = "rakuraku_apps"

class TankModel(BaseModel):
    name = models.CharField("名前", max_length=64)
    
    class Meta:
        verbose_name = "水槽"
        db_table = "tank"

class WaterQualityModel(BaseModel):
    date = models.DateField("計測日")
    room_temperature = models.IntegerField("室温", null=True)
    water_temperature = models.IntegerField("水温", null=True)
    pH = models.IntegerField("ph", null=True)
    DO = models.IntegerField("DO", null=True)
    salinity = models.IntegerField("塩分濃度", null=True)
    NH4 = models.IntegerField("NH4", null=True)
    NO2 = models.IntegerField("NO2", null=True)
    NO3 = models.IntegerField("NO3", null=True)
    Ca = models.IntegerField("Ca", null=True)
    Al = models.IntegerField("Al", null=True)
    Mg = models.IntegerField("Mg", null=True)
    notes = models.TextField("備考", max_length=512, null=True, blank=True)
    tank = models.ForeignKey(
        "TankModel",
        verbose_name="水槽",
        blank=False,
        null=False,
        related_name="water_quality",
        on_delete=models.PROTECT,
    )
    class Meta:
        verbose_name = "水質"
        db_table = "water_quality"

class AlertModel(BaseModel):
    alert_range = models.IntegerField("警告範囲", null=True)
    water_quality= models.ForeignKey(
        "WaterQualityModel",
        verbose_name="水質",
        blank=False,
        null=False,
        related_name="alert_range",
        on_delete=models.PROTECT,
    )
    class Meta:
        verbose_name = "警告範囲"
        db_table = "alert_range"