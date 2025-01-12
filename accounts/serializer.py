import re
from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name','password', 'confirm_password')

    def validate_password(self, value):
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Password must contain at least 8 characters, including uppercase, lowercase letters, numbers, and special characters.')
        return value
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password':'Password and Confirm Password must be the same.'})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.is_active:
                raise serializers.ValidationError({'email':'Please verify your email to login.'})
            elif not user.check_password(password):
                raise serializers.ValidationError({'password':'Incorrect password.'})
        else:
            raise serializers.ValidationError({'email':'User with this email does not exist. please register first.'})
        return data
    
class GetRefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate_new_password(self, value):
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Password must contain at least 8 characters, including uppercase, lowercase letters, numbers, and special characters.')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError({'new_password':'New Password and Old Password must not be the same.'})
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'new_password':'New Password and Confirm New Password must be the same.'})
        return attrs