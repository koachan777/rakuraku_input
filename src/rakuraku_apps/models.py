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

class ShrimpModel(BaseModel):
    family = models.CharField("系統", max_length=64)

    class Meta:
        verbose_name = "系統"
        db_table = "shrimp"


class TankModel(BaseModel):
    name = models.CharField("名前", max_length=64)
    shrimp = models.ForeignKey(
        "ShrimpModel",
        verbose_name="系統",
        blank=False,
        null=False,
        related_name="tank",
        on_delete=models.PROTECT,
    )
    class Meta:
        verbose_name = "水槽"
        db_table = "tank"



class WaterQualityModel(BaseModel):
    date = models.DateField("計測日")
    room_temperature = models.FloatField("室温", null=True, blank=True)
    water_temperature = models.FloatField("水温", null=True, blank=True)
    pH = models.FloatField("ph", null=True, blank=True)
    DO = models.FloatField("DO", null=True, blank=True)
    salinity = models.FloatField("塩分濃度", null=True, blank=True)
    NH4 = models.FloatField("NH4", null=True, blank=True)
    NO2 = models.FloatField("NO2", null=True, blank=True)
    NO3 = models.FloatField("NO3", null=True, blank=True)
    Ca = models.FloatField("Ca", null=True, blank=True)
    Al = models.FloatField("Al", null=True, blank=True)
    Mg = models.FloatField("Mg", null=True, blank=True)
    notes = models.TextField("備考", max_length=512, null=True, blank=True)
    tank = models.ForeignKey(
        "TankModel",
        verbose_name="水槽",
        blank=False,
        null=False,
        related_name="water_quality",
        on_delete=models.CASCADE,
    )
    notify_line = models.BooleanField(default=False)


    class Meta:
        verbose_name = "水質"
        db_table = "water_quality"
        unique_together = ('date', 'tank')

class WaterQualityThresholdModel(BaseModel):
    PARAMETER_CHOICES = [
        ('water_temperature', '水温'),
        ('pH', 'pH'),
        ('DO', 'DO'),
        ('salinity', '塩分濃度'),
        ('NH4', 'NH4'),
        ('NO2', 'NO2'),
        ('NO3', 'NO3'),
        ('Ca', 'Ca'),
        ('Al', 'Al'),
        ('Mg', 'Mg'),
    ]

    parameter = models.CharField("パラメーター", max_length=20, choices=PARAMETER_CHOICES)
    reference_value_threshold_max = models.FloatField("基準の上限値", null=True, blank=True)
    reference_value_threshold_min = models.FloatField("基準の下限値", null=True, blank=True)
    previous_day_threshold = models.FloatField("前日との差異閾値", null=True, blank=True)

    class Meta:
        verbose_name = "水質アラート設定"
        db_table = "water_quality_threshold"

    def __str__(self):
        return self.get_parameter_display()

    @classmethod
    def update_or_create(cls, parameter, reference_value_threshold_max=None, reference_value_threshold_min=None, previous_day_threshold=None):
        threshold, created = cls.objects.update_or_create(
            parameter=parameter,
            defaults={
                'reference_value_threshold_max': reference_value_threshold_max,
                'reference_value_threshold_min': reference_value_threshold_min,
                'previous_day_threshold': previous_day_threshold,
            }
        )
        return threshold