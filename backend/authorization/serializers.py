
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)   

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        return user
    
    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username, active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("کاربری با این مشخصات پیدا نشد.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("رمز عبور اشتباه است.")

        data["user"] = user
        return data