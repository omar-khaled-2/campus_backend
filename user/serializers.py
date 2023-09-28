from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User,Student
from django.contrib.auth.password_validation import validate_password




class EmailExistsValidator:
    def __call__(self, value):
        is_exist = User.objects.filter(email = value).exists()
        if not is_exist:
            raise serializers.ValidationError('Email does not exist.')
    
class EmailUniqueValidator:
    def __call__(self, value):
        is_exist = User.objects.filter(email = value).exists()
        if is_exist:
            raise serializers.ValidationError('Duplicate email. Try a different one')
    

class CertainLengthValidator:
    def __init__(self,length):
        self.length = length
    def __call__(self, value):
        if(len(value) != self.length):
            raise serializers.ValidationError("This field length must be %s" % self.length)

class EmailSerilizer(serializers.Serializer):
    email = serializers.EmailField(validators = [EmailUniqueValidator()])


class NameSerilizer(serializers.Serializer):
    first_name = serializers.CharField(min_length = 3,max_length = 10)
    last_name = serializers.CharField(min_length = 3,max_length = 10)

class UserSerializer(NameSerilizer):
    id = serializers.IntegerField()
    profile_pic = serializers.ImageField()



class SignInSerilizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class SignUpSerilizer(NameSerilizer):
    academic_id = serializers.CharField(
        validators=[
            CertainLengthValidator(8),
            UniqueValidator(queryset=Student.objects.all(),message="Uh-oh! The academic_id is already taken ,please contact with admin")
        ]
    )

    password = serializers.CharField()
    email = serializers.EmailField(
        validators = [
            UniqueValidator(queryset=User.objects.all(),message="Looks like this email is already in use")
            ]
        )

    def validate_password(self, value):
        validate_password(value)
        return value
    

    


           

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(validators = [EmailExistsValidator()])


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        validate_password(value)
        return value

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()



class OTPSerilizer(serializers.Serializer):
    exp = serializers.DateTimeField()

class ChangeProfilePicSerializer(serializers.Serializer):
    profile_pic = serializers.ImageField()