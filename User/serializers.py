#User/serializers.py
from rest_framework import serializers
from .models import User
from .models import Server
from .models import Like

class UserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User        # User 모델 사용
        fields = '__all__'            # 모든 필드 포함

class ServerSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Server        # Server 모델 사용
        fields = '__all__'            # 모든 필드 포함

class LikeSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Like        # Like 모델 사용
        fields = '__all__'            # 모든 필드 포함