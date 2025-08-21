from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    """
        get user profile info and user info together
    """
    first_name = serializers.CharField(source='profile.first_name', read_only=True)
    last_name = serializers.CharField(source='profile.last_name', read_only=True)
    image = serializers.ImageField(source='profile.image', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'created_date', 'first_name', 'last_name', 'image')
        read_only_fields = ('id', 'email', 'created_date')


class RegisterSerializer(serializers.ModelSerializer):
    """
        register: email most be unique
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        label="confirm password",
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    # validate entered password
    def validate_password(self, value):
        validate_password(value)
        return value

    # match validation for entered password and confirm password
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('password and confirm password must match')
        return data

    # create new user by Entered info
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    """
        check user authentication by django default authenticator
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError('invalid email or password')
        if not user.is_active:
            raise serializers.ValidationError('user account is deactivated')

        data['user'] = user
        return data



class ChangePasswordSerializer(serializers.ModelSerializer):
    """
        change password
    """
    old_password = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    """
        validation of entered password
    """
    def validate_password(self, value):
        validate_password(value)
        return value

    """
        match validation for entered password and confirm password 
    """
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('password must match')
        return data

    """
        update model for change old password
    """
    def update(self, instance, validated_data):
        old_password = validated_data.pop('old_password')
        if not instance.check_password(old_password):
            raise serializers.ValidationError({'message': 'invalid old password'})
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
