from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from djongo import models

from octofit_tracker.models import Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Clear collections
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Users
        tony = User.objects.create_user(username='ironman', email='tony@stark.com', password='pass', first_name='Tony', last_name='Stark', team=marvel)
        steve = User.objects.create_user(username='cap', email='steve@rogers.com', password='pass', first_name='Steve', last_name='Rogers', team=marvel)
        bruce = User.objects.create_user(username='hulk', email='bruce@banner.com', password='pass', first_name='Bruce', last_name='Banner', team=marvel)
        clark = User.objects.create_user(username='superman', email='clark@kent.com', password='pass', first_name='Clark', last_name='Kent', team=dc)
        diana = User.objects.create_user(username='wonderwoman', email='diana@prince.com', password='pass', first_name='Diana', last_name='Prince', team=dc)

        # Activities
        Activity.objects.create(user=tony, type='run', duration=30, distance=5)
        Activity.objects.create(user=steve, type='cycle', duration=60, distance=20)
        Activity.objects.create(user=bruce, type='swim', duration=45, distance=2)
        Activity.objects.create(user=clark, type='fly', duration=120, distance=100)
        Activity.objects.create(user=diana, type='run', duration=50, distance=10)

        # Workouts
        Workout.objects.create(name='Morning Cardio', description='A quick morning run', suggested_by=tony)
        Workout.objects.create(name='Strength Training', description='Weight lifting session', suggested_by=bruce)
        Workout.objects.create(name='Flight Endurance', description='Long distance flying', suggested_by=clark)

        # Leaderboard
        Leaderboard.objects.create(user=tony, points=100)
        Leaderboard.objects.create(user=steve, points=90)
        Leaderboard.objects.create(user=bruce, points=80)
        Leaderboard.objects.create(user=clark, points=120)
        Leaderboard.objects.create(user=diana, points=110)

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.db_conn[User._meta.db_table].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
