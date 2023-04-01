from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()




class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = User
        fields = ("email",)



class UserRegisterationSerializer(serializers.ModelSerializer):

    """
    Serializer class to serialize registration requests and create a new user.
    """
    phone = serializers.CharField(max_length=11, allow_null=False)
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email','password', 'password2', )
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'], 
        )
        user.set_password(validated_data['password'])
        user.save()

        return user



class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")




class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)




class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password reset endpoint.

    """
    email = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model=User
        fields=['email', 'password']

    def save(self):
        email=self.validated_data['email']
        password=self.validated_data['password']
        #filtering out whethere email is existing or not, if your email is existing then if condition will allow your email
        if User.objects.filter(email=email).exists():
        #if your email is existing get the query of your specific email 
            user=User.objects.get(email=email)
            #then set the new password for your email
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error':'please enter valid crendentials'})