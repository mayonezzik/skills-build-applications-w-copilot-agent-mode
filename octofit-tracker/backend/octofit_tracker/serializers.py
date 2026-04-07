from rest_framework import serializers
from .models import User, Team, Activity, Workout, Leaderboard

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'team']

class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Activity
        fields = ['id', 'user', 'type', 'duration', 'distance', 'timestamp']

class WorkoutSerializer(serializers.ModelSerializer):
    suggested_by = UserSerializer(read_only=True)
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'suggested_by']

class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'points']
