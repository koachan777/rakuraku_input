from django.core.management.base import BaseCommand
from rakuraku_apps.models import User, TankModel, WaterQualityModel

class Command(BaseCommand):
    help = 'Clear test data from the database'

    def add_arguments(self, parser):
        parser.add_argument('--users', action='store_true', help='Clear user data')
        parser.add_argument('--tanks', action='store_true', help='Clear tank data')
        parser.add_argument('--wq', action='store_true', help='Clear water quality data')

    def handle(self, *args, **kwargs):
        if kwargs['users']:
            self.clear_users()
        if kwargs['tanks']:
            self.clear_tanks()
        if kwargs['wq']:
            self.clear_water_quality()

    def clear_users(self):
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all users'))

    def clear_tanks(self):
        default_tank_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        TankModel.objects.exclude(id__in=default_tank_ids).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all non-default tanks'))
        
    def clear_water_quality(self):
        WaterQualityModel.objects.filter(notes__startswith='Test data').delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all test water quality data'))