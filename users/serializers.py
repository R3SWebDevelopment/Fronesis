from versatileimagefield.serializers import VersatileImageFieldSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from drum.links.models import Profile
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # avatar = VersatileImageFieldSerializer(
    #     sizes='userprofile_avatar'
    # )
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']


    def get_avatar(self, obj):
        avatar = obj.avatar
        if obj.avatar:
            return{
                'full_size': obj.avatar.url,
                'medium_square_crop': obj.avatar.crop['280x280'].url,
                'small_square_crop': obj.avatar.crop['50x50'].url,
                'thumbnail': obj.avatar.crop['280x280'].url,
            }
        else:
            return{
                'full_size': 'http://eadb.org/wp-content/uploads/2015/08/profile-placeholder.jpg',
                'medium_square_crop': 'http://eadb.org/wp-content/uploads/2015/08/profile-placeholder.jpg',
                'small_square_crop': 'http://eadb.org/wp-content/uploads/2015/08/profile-placeholder.jpg',
                'thumbnail': 'http://eadb.org/wp-content/uploads/2015/08/profile-placeholder.jpg',
            }



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
