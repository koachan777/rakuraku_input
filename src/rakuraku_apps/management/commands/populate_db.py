import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from rakuraku_apps.models import User, TankModel, WaterQualityModel, ShrimpModel
from rakuraku_apps.models import WaterQualityThresholdModel

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def add_arguments(self, parser):
        # parser.add_argument('--users', type=int, help='Number of users to create')
        parser.add_argument('--tanks', type=int, help='Number of tanks to create')
        parser.add_argument('--wq', type=int, help='Number of water quality records to create')
        parser.add_argument('--init_thresholds', action='store_true', help='Populate water quality thresholds')

    def handle(self, *args, **kwargs):
        # user_count = kwargs.get('users')
        tank_count = kwargs.get('tanks')
        water_quality_count = kwargs.get('wq')
        populate_thresholds = kwargs.get('init_thresholds')

        # if user_count is not None:
        #     self.populate_users(user_count)
        if tank_count is not None:
            self.populate_tanks(tank_count)
        if water_quality_count is not None:
            self.populate_water_quality(water_quality_count)
        if populate_thresholds is not None:
            self.populate_water_quality_threshold()

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
                        water_temperature=round(random.uniform(27.5, 29.5), 1),
                        pH=round(random.uniform(7.6, 8.5), 2),
                        DO=round(random.uniform(6.0, 12.0), 1),
                        salinity=round(random.uniform(1.9, 2.3), 2),
                        NH4=round(random.uniform(0.0, 6.0), 1),
                        NO2=round(random.uniform(1.3, 2.8), 1),
                        NO3=round(random.uniform(12, 24), 1),
                        Ca=round(random.uniform(270, 312), 0),
                        Al=round(random.uniform(175, 205), 0),
                        Mg=round(random.uniform(680, 810), 0),
                        notes=f'Test data {i}日目',
                        tank_id=tank_id
                    )
                    
    def populate_water_quality_threshold(self):
        
        
        thresholds = [
            {'parameter': 'water_temperature', 'reference_value_threshold_min': 28, 'reference_value_threshold_max': 29, 'reference_value_threshold_range': None, 'previous_day_threshold': 0.5},
            {'parameter': 'pH', 'reference_value_threshold_min': 7.9, 'reference_value_threshold_max': 8.2, 'reference_value_threshold_range': None, 'previous_day_threshold': 1},
            {'parameter': 'DO', 'reference_value_threshold_min': 6, 'reference_value_threshold_max': None, 'reference_value_threshold_range': 5, 'previous_day_threshold': 1},
            {'parameter': 'salinity', 'reference_value_threshold_min': 2.0, 'reference_value_threshold_max': 2.0, 'reference_value_threshold_range': 0.5, 'previous_day_threshold': 0.3},
            {'parameter': 'NH4', 'reference_value_threshold_min': 0, 'reference_value_threshold_max': 5, 'reference_value_threshold_range': None, 'previous_day_threshold': 2},
            {'parameter': 'NO2', 'reference_value_threshold_min': 1.5, 'reference_value_threshold_max': 2.5, 'reference_value_threshold_range': None, 'previous_day_threshold': 1},
            {'parameter': 'NO3', 'reference_value_threshold_min': 15, 'reference_value_threshold_max': 20, 'reference_value_threshold_range': None, 'previous_day_threshold': 3},
            {'parameter': 'Ca', 'reference_value_threshold_min': 280, 'reference_value_threshold_max': 300, 'reference_value_threshold_range': None, 'previous_day_threshold': 30},
            {'parameter': 'Al', 'reference_value_threshold_min': 180, 'reference_value_threshold_max': 200, 'reference_value_threshold_range': None, 'previous_day_threshold': 10},
            {'parameter': 'Mg', 'reference_value_threshold_min': 700, 'reference_value_threshold_max': 800, 'reference_value_threshold_range': None, 'previous_day_threshold': 50},
        ]

        for threshold in thresholds:
            WaterQualityThresholdModel.objects.update_or_create(
                parameter=threshold['parameter'],
                defaults={
                    'reference_value_threshold_min': threshold['reference_value_threshold_min'],
                    'reference_value_threshold_max': threshold['reference_value_threshold_max'],
                    'reference_value_threshold_range': threshold['reference_value_threshold_range'],
                    'previous_day_threshold': threshold['previous_day_threshold'],
                    'created_at': timezone.now(),
                    'modified_at': timezone.now(),
                }
            )
            
            
            
