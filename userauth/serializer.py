from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from userauth.models import UserModel
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=UserModel.objects.all())],
            min_length=5,
            max_length=20
            ),
    password = serializers.CharField(
            required=True,
            max_length=256
            )
    # def validate_password(self, value: str) -> str:
    #     """
    #     Hash value passed by user.

    #     :param value: password of a user
    #     :return: a hashed version of the password
    #     """
    #     return make_password(value)

    class Meta:
        model = UserModel
        fields = ['username','password']
        # read_only_fields = ( ,)

    def create(self, validated_data):
        user = UserModel.objects.create_user(validated_data['username'], validated_data["password"])
        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # assign token 
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # extra fields
        data['username'] = self.user.username
        data['nama'] = self.user.nama
        data['isAdmin'] = self.user.isadmin
        return data

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer