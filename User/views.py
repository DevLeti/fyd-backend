#view.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Server, Like, Tag
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, ServerSerializer, CreateServerSerializer, PutServerSerializer,LikeSerializer, CreateLikeSerializer, TagSerializer, CreateTagSerializer, RegisterSerializer
from rest_framework import status
from django.http import Http404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([])
    serializer_class = RegisterSerializer
class UserListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        queryset = User.objects.all()
        print(queryset)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # def post(self, request):
    #     # request.data는 사용자의 입력 데이터
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid(): #유효성 검사
    #         serializer.save() # 저장
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ServerListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        queryset = Server.objects.all()
        print(queryset)
        serializer = ServerSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = CreateServerSerializer(data=request.data)

        if serializer.is_valid(): #유효성 검사
            serializer.validated_data['user_id'] = request.user # user 추가
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_object(self, pk):
        try:
            return Server.objects.get(pk=pk)
        except Server.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        server = self.get_object(pk)
        serializer = ServerSerializer(server)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        server = self.get_object(pk)
        serializer = PutServerSerializer(server, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user_id'] = request.user # user 추가
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        server = self.get_object(pk)
        server.delete()  
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        queryset = Tag.objects.all()
        print(queryset)
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = CreateTagSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.validated_data["user_id"] = request.user
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    # def get_object(self, pk):
    #     try:
    #         return Tag.objects.get(pk=pk)
    #     except Tag.DoesNotExist:
    #         raise Http404
    
    def get(self, request, server_id, format=None):
        tag = Tag.objects.filter(server_id=server_id)
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     tag = self.get_object(pk)
    #     serializer = TagSerializer(tag, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, server_id, format=None):
        tag_name = request.data["tag_name"]
        tag = Tag.objects.filter(server_id=server_id, tag_name=tag_name)
        if len(tag) != 0: #존재하지 않음
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class LikeListAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        queryset = Like.objects.all()
        print(queryset)
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = CreateLikeSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.validated_data['user_id'] = request.user
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = request.user
        server_id = request.data['server_id']
        like = Like.objects.filter(user_id=user_id, server_id=server_id)
        # like = Like.objects.get(data=request.data)
        if len(like) != 0:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
class LikeDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            raise Http404
    
    # pk의 like 리스트를 넘겨줌
    def get(self, request, pk, format=None):
        like = Like.objects.filter(server_id=pk)
        serializer = LikeSerializer(like, many=True)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     like = self.get_object(pk)
    #     serializer = LikeSerializer(like, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer