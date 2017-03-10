from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from drum.links.models import Profile
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__280x280'),
            ('medium_square_crop', 'crop__280x280'),
            ('small_square_crop', 'crop__50x50')
        ]
    )

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']


class ProfileSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['userprofile']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'profile'
        ]
        read_only_fields = ['email']
