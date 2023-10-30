from rest_framework import serializers
from . import models

class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.users
        fields= ('id', 'name', 'email', 'password', 'userId', 'isStudent')