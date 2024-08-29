import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from rakuraku_apps.models import User, TankModel, WaterQualityModel
from rakuraku_apps.models import ShrimpModel

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def add_arguments(self, parser):
        # parser.add_argument('--users', type=int, help='Number of users to create')
        parser.add_argument('--tanks', type=int, help='Number of tanks to create')
        parser.add_argument('--wq', type=int, help='Number of water quality records to create')

    def handle(self, *args, **kwargs):
        # user_count = kwargs.get('users')
        tank_count = kwargs.get('tanks')
        water_quality_count = kwargs.get('wq')

        # if user_count is not None:
        #     self.populate_users(user_count)
        if tank_count is not None:
            self.populate_tanks(tank_count)
        if water_quality_count is not None:
            self.populate_water_quality(water_quality_count)

    # def populate_users(self, count = 0):
    #     for _ in range(count):
    #         User.objects.create(
    #             account_id=f'user_{random.randint(1000, 9999)}',
    #             password='password',
    #             is_active=True,
    #             is_staff=False,
    #             is_superuser=False
    #         )

    def populate_tanks(self, count = 0):
        shrimp_ids = list(ShrimpModel.objects.values_list('id', flat=True))
        for _ in range(count):
            number_of_tanks = 4
            for number_of_tank in range(number_of_tanks):
                TankModel.objects.create(
                    name=f'{_+4}-{number_of_tank+1}',
                    shrimp_id=random.choice(shrimp_ids)  # 有効なShrimpModelのIDをランダムに選択
                )

    def populate_water_quality(self, count):
        tank_ids = TankModel.objects.values_list('id', flat=True)
        for i in range(count):
            for tank_id in tank_ids:
                date = timezone.now().date() + timezone.timedelta(days=i)
                # 重複チェック
                if not WaterQualityModel.objects.filter(date=date, tank_id=tank_id).exists():
                    WaterQualityModel.objects.create(
                        date=date,
                        room_temperature=round(random.uniform(15.0, 30.0), 1),
                        water_temperature=round(random.uniform(15.0, 30.0), 1),
                        pH=round(random.uniform(6.0, 8.0), 1),
                        DO=round(random.uniform(5.0, 10.0), 1),
                        salinity=round(random.uniform(0.0, 14.0), 1),
                        NH4=round(random.uniform(0.0, 1.0), 1),
                        NO2=round(random.uniform(0.0, 1.0), 1),
                        NO3=round(random.uniform(0.0, 50.0), 1),
                        Ca=round(random.uniform(0.0, 14.0), 1),
                        Al=round(random.uniform(0.0, 14.0), 1),
                        Mg=round(random.uniform(0.0, 14.0), 1),
                        notes=f'Test data {i}日目',
                        tank_id=tank_id
                    )