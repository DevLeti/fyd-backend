#User/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Server
from .models import Tag
from .models import Like

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User        # User 모델 사용
        fields = '__all__'            # 모든 필드 포함

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'
        # fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            # 'first_name': {'required': True},
            # 'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            # email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class ServerSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Server        # Server 모델 사용
        fields = '__all__'            # 모든 필드 포함

class CreateServerSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Server        # Server 모델 사용
        fields = ('server_id', 'server_name','server_url', 'server_description')            # 모든 필드 포함

class PutServerSerializer(serializers.ModelSerializer):
    class Meta :
        model = Server        # Server 모델 사용
        fields = ('server_id', 'server_name','server_url', 'server_description')            # 모든 필드 포함

class TagSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Tag        # Tag 모델 사용
        fields = '__all__'            # 모든 필드 포함

class CreateTagSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Tag        # Tag 모델 사용
        fields = ('id', 'server_id', 'tag_name')

class LikeSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Like        # Like 모델 사용
        fields = '__all__'            # 모든 필드 포함

class CreateLikeSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Like        # Tag 모델 사용
        fields = ('id', 'server_id')

# TODO: Server id를 통해서 like와 tag 정보까지 불러오기
class ServerLikeTagSerializer(serializers.ModelSerializer):
    like = LikeSerializer()
    tag = TagSerializer()
    class Meta:
        model = Server
        fields = ["server_id","user_id","server_name","server_url","server_description","like","tag"]

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token